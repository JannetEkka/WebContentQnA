import logging
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import numpy as np
import re

class DistilBERTQuestionAnsweringModel:
    """Answer questions based on content using DistilBERT"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.logger.info(f"Using device: {self.device}")
        
        try:
            # Load model and tokenizer
            self.model_name = "distilbert-base-cased-distilled-squad"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.logger.info(f"Loaded DistilBERT model: {self.model_name}")
        except Exception as e:
            self.logger.error(f"Error loading DistilBERT model: {str(e)}")
            raise e
    
    def _preprocess_text(self, text):
        """Clean and preprocess text"""
        # Basic cleaning
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _split_into_chunks(self, text, max_chunk_size=512):
        """Split text into chunks that fit within BERT's max token limit"""
        # Split into paragraphs
        paragraphs = text.split("\n\n")
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Rough estimate of tokens (words + some extra for tokenization)
            para_length = len(para.split())
            
            if current_length + para_length <= max_chunk_size:
                current_chunk.append(para)
                current_length += para_length
            else:
                # Save current chunk and start a new one
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [para]
                current_length = para_length
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks
    
    def _find_most_relevant_chunk(self, question, chunks):
        """Find the most relevant text chunk for the question using DistilBERT embeddings"""
        if not chunks:
            self.logger.warning("No chunks to process!")
            return "", 0
            
        # If only one chunk, return it
        if len(chunks) == 1:
            self.logger.info(f"Only one chunk available, returning it (length: {len(chunks[0])})")
            return chunks[0], 1.0
    
        self.logger.info(f"Finding most relevant chunk among {len(chunks)} chunks for question: '{question}'")
            
        try:
            # Tokenize question
            question_tokens = self.tokenizer(question, return_tensors="pt")
            question_tokens = {k: v.to(self.device) for k, v in question_tokens.items()}
            
            # Get question embedding (use last hidden state's [CLS] token)
            with torch.no_grad():
                question_outputs = self.model(**question_tokens, output_hidden_states=True)
                question_embedding = question_outputs.hidden_states[-1][0, 0, :].cpu().numpy()
            
            # Get embeddings for each chunk
            chunk_scores = []
            for chunk in chunks:
                self.logger.debug(f"Processing chunk {i+1}/{len(chunks)} (length: {len(chunk)})")
                chunk_tokens = self.tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512)
                chunk_tokens = {k: v.to(self.device) for k, v in chunk_tokens.items()}
                
                with torch.no_grad():
                    chunk_outputs = self.model(**chunk_tokens, output_hidden_states=True)
                    chunk_embedding = chunk_outputs.hidden_states[-1][0, 0, :].cpu().numpy()
                
                # Calculate cosine similarity
                similarity = np.dot(question_embedding, chunk_embedding) / (
                    np.linalg.norm(question_embedding) * np.linalg.norm(chunk_embedding)
                )
                chunk_scores.append(similarity)
                self.logger.debug(f"Chunk {i+1} similarity score: {similarity:.4f}")
            
            # Get the index of the most similar chunk
            most_similar_idx = np.argmax(chunk_scores)

            self.logger.info(f"Selected chunk {most_similar_idx+1}/{len(chunks)} with score: {chunk_scores[most_similar_idx]:.4f}")
            self.logger.info(f"Selected chunk preview: '{chunks[most_similar_idx][:100]}...'")
            
            return chunks[most_similar_idx], chunk_scores[most_similar_idx]
            
        except Exception as e:
            self.logger.error(f"Error finding relevant chunk: {str(e)}")
            # Fallback to first chunk
            return chunks[0], 0.5
    
    def _extract_answer(self, question, text):
        """Extract the answer from the text based on the question using DistilBERT"""
        try:
            self.logger.info(f"Extracting answer for question: '{question}'")
            self.logger.info(f"Text length: {len(text)}")
            # Tokenize question and text
            inputs = self.tokenizer(
                question, 
                text, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Log tokenization info
            self.logger.debug(f"Tokenized input length: {len(inputs['input_ids'][0])}")
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get start and end logits
            start_logits = outputs.start_logits
            end_logits = outputs.end_logits
            
            # Get the most likely start and end positions
            start_idx = torch.argmax(start_logits).item()
            end_idx = torch.argmax(end_logits).item()

            self.logger.debug(f"Raw start_idx: {start_idx}, end_idx: {end_idx}")
            
            # Handle case where end is before start
            if end_idx < start_idx:
                # Find next best end position
                self.logger.warning(f"End index {end_idx} is before start index {start_idx}, finding next best end position")
                end_logits[0, start_idx] = -100
                end_idx = torch.argmax(end_logits).item()
                self.logger.debug(f"Updated end_idx: {end_idx}")
            
            # Convert token positions to character positions
            input_ids = inputs["input_ids"][0].tolist()
            tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
            
            self.logger.debug(f"Token span ({start_idx}, {end_idx}): {tokens[max(0, start_idx-5):start_idx]} [START] {tokens[start_idx:end_idx+1]} [END] {tokens[end_idx+1:min(len(tokens), end_idx+6)]}")

            # Extract answer
            answer_tokens = tokens[start_idx:end_idx+1]
            answer = self.tokenizer.convert_tokens_to_string(answer_tokens)
            
            # Calculate confidence
            confidence = (torch.softmax(start_logits, dim=1)[0, start_idx].item() + 
                          torch.softmax(end_logits, dim=1)[0, end_idx].item()) / 2
            
            # Log extracted answer details
            self.logger.info(f"Extracted raw answer: '{answer}'")
            self.logger.info(f"Confidence score: {confidence:.4f}")
            
            # Extract context (tokens around the answer)
            context_start = max(0, start_idx - 10)
            context_end = min(len(tokens), end_idx + 10)
            context_tokens = tokens[context_start:context_end]
            context = self.tokenizer.convert_tokens_to_string(context_tokens)
            
            self.logger.info(f"Context: '{context}'")

            # If answer is empty or just punctuation/whitespace
            if not answer.strip() or answer.strip() in ".,;:!?-":
                self.logger.warning("Answer is empty or just punctuation, returning fallback message")
                return "I couldn't find a specific answer in the provided content.", 0.1, ""
            
            return answer, confidence, context
            
        except Exception as e:
            self.logger.error(f"Error extracting answer: {str(e)}")
            return "Error processing the question.", 0.0, ""
    
    def answer_question(self, question, content):
        """
        Answer a question based on the content
        
        Args:
            question (str): Question to answer
            content (str): Content to search for answers
            
        Returns:
            tuple: (answer, confidence, context)
        """
        self.logger.info(f"====== NEW QUESTION ======")
        self.logger.info(f"Answering question using DistilBERT: {question}")
        
        if not content or not question:
            self.logger.warning("No content or question provided")
            return "No content available to answer this question.", 0.0, ""
        
        # Preprocess
        question = self._preprocess_text(question)
        content = self._preprocess_text(content)

        self.logger.info(f"Content length after preprocessing: {len(content)}")
        
        # Split content into manageable chunks
        chunks = self._split_into_chunks(content)
        self.logger.info(f"Split content into {len(chunks)} chunks")
        
        # Find most relevant chunk
        most_relevant_chunk, chunk_confidence = self._find_most_relevant_chunk(question, chunks)
        
        # Extract answer from the most relevant chunk
        answer, answer_confidence, context = self._extract_answer(question, most_relevant_chunk)
        
        # Combine confidences
        confidence = (chunk_confidence + answer_confidence) / 2

        self.logger.info(f"Final answer: '{answer}'")
        self.logger.info(f"Final confidence: {confidence:.4f}")
        self.logger.info(f"====== END QUESTION ======")
        
        return answer, confidence, context