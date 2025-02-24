import spacy
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class QuestionAnsweringModel:
    """Answer questions based on content using NLP techniques"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            # Load spaCy model
            self.nlp = spacy.load('en_core_web_md')
            self.logger.info("Loaded spaCy model successfully")
        except Exception as e:
            self.logger.error(f"Error loading spaCy model: {str(e)}")
            # Fallback to smaller model if available
            try:
                self.nlp = spacy.load('en_core_web_sm')
                self.logger.info("Loaded fallback spaCy model")
            except:
                self.logger.error("Could not load any spaCy model")
                self.nlp = None
    
    def _preprocess_text(self, text):
        """Clean and preprocess text"""
        # Basic cleaning
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _split_into_chunks(self, text, max_chunk_size=5000):
        """Split text into manageable chunks"""
        # Simple sentence-based chunking
        sentences = [sent.text for sent in self.nlp(text).sents]
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            # Skip very short sentences 
            if len(sentence) < 5:
                continue
                
            if current_size + len(sentence) <= max_chunk_size:
                current_chunk.append(sentence)
                current_size += len(sentence)
            else:
                # Save current chunk and start a new one
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_size = len(sentence)
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks
    
    def _find_most_relevant_chunk(self, question, chunks):
        """Find the most relevant text chunk for the question"""
        if not chunks:
            return "", 0
            
        # Use TF-IDF to vectorize the question and chunks
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # If only one chunk, return it
        if len(chunks) == 1:
            return chunks[0], 1.0
            
        # Vectorize the chunks
        try:
            tfidf_matrix = vectorizer.fit_transform(chunks + [question])
            
            # Get the question vector (last in the matrix)
            question_vector = tfidf_matrix[-1]
            
            # Calculate cosine similarity between question and each chunk
            chunk_vectors = tfidf_matrix[:-1]
            similarities = cosine_similarity(question_vector, chunk_vectors).flatten()
            
            # Get the index of the most similar chunk
            most_similar_idx = np.argmax(similarities)
            
            return chunks[most_similar_idx], similarities[most_similar_idx]
        except Exception as e:
            self.logger.error(f"Error finding relevant chunk: {str(e)}")
            # Fallback to first chunk
            return chunks[0], 0.5
    
    def _extract_answer(self, question, text):
        """Extract the answer from the text based on the question"""
        try:
            # Process the question and text with spaCy
            question_doc = self.nlp(question)
            text_doc = self.nlp(text)
            
            # Check what type of question we're dealing with
            question_tokens = [token.text.lower() for token in question_doc]
            
            # Identify question words and entities
            question_word = None
            for word in ["who", "what", "when", "where", "why", "how"]:
                if word in question_tokens:
                    question_word = word
                    break
            
            # Get named entities in the question
            question_entities = [ent.text for ent in question_doc.ents]
            
            # Find sentences in the text that contain question entities
            relevant_sentences = []
            for sent in text_doc.sents:
                # Score based on question entities
                score = 0
                for ent in question_entities:
                    if ent.lower() in sent.text.lower():
                        score += 1.5
                
                # Also check for keyword matches
                for token in question_doc:
                    if token.is_alpha and not token.is_stop:
                        # Give higher weight to subject and objects in the question
                        if token.dep_ in ['nsubj', 'dobj', 'pobj']:
                            if token.text.lower() in sent.text.lower():
                                score += 1.0
                        # Regular keywords
                        elif token.text.lower() in sent.text.lower():
                            score += 0.5
                
                if score > 0:
                    relevant_sentences.append((sent.text, score))
            
            # Sort by relevance score
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            
            if not relevant_sentences:
                # Fallback to basic keyword matching
                keywords = [token.text.lower() for token in question_doc 
                            if token.is_alpha and not token.is_stop]
                
                best_sentence = None
                best_score = 0
                
                for sent in text_doc.sents:
                    score = 0
                    for keyword in keywords:
                        if keyword in sent.text.lower():
                            score += 1
                    
                    if score > best_score:
                        best_score = score
                        best_sentence = sent.text
                
                if best_sentence:
                    return best_sentence, best_score / len(keywords), best_sentence
            
            # Prepare answer from top relevant sentences
            if relevant_sentences:
                top_sentences = [s[0] for s in relevant_sentences[:2]]
                answer = " ".join(top_sentences)
                confidence = relevant_sentences[0][1] / (len(question_entities) + 2) if question_entities else 0.5
                context = " ".join([s[0] for s in relevant_sentences[:3]])
                
                return answer, min(confidence, 0.95), context
            
            return "I couldn't find a specific answer in the provided content.", 0.1, ""
            
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
        self.logger.info(f"Answering question: {question}")
        
        if not content or not question:
            return "No content available to answer this question.", 0.0, ""
        
        # Preprocess
        question = self._preprocess_text(question)
        content = self._preprocess_text(content)
        
        # Split content into manageable chunks
        chunks = self._split_into_chunks(content)
        
        # Find most relevant chunk
        most_relevant_chunk, chunk_confidence = self._find_most_relevant_chunk(question, chunks)
        
        # Extract answer from the most relevant chunk
        answer, answer_confidence, context = self._extract_answer(question, most_relevant_chunk)
        
        # Combine confidences
        confidence = (chunk_confidence + answer_confidence) / 2
        
        return answer, confidence, context