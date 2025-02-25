import logging
import re
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text  # Required for BERT preprocessing
from sklearn.metrics.pairwise import cosine_similarity

class TensorFlowQuestionAnsweringModel:
    """Answer questions based on content using TensorFlow and Universal Sentence Encoder"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        try:
            # Set lower memory growth - helps on systems with limited GPU memory
            gpus = tf.config.experimental.list_physical_devices('GPU')
            if gpus:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                self.logger.info(f"Using GPU: {gpus}")
            else:
                self.logger.info("Using CPU for TensorFlow")
            
            # Load Universal Sentence Encoder (much lighter than BERT-based models)
            # There are two options:
            # 1. Universal Sentence Encoder (smaller, faster)
            # self.model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
            # 2. Multilingual Universal Sentence Encoder (slightly larger, supports multiple languages)
            self.model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
            
            self.model = hub.load(self.model_url)
            self.logger.info(f"Loaded TensorFlow model: Universal Sentence Encoder")
        except Exception as e:
            self.logger.error(f"Error loading TensorFlow model: {str(e)}")
            raise e
    
    def _preprocess_text(self, text):
        """Clean and preprocess text"""
        # Basic cleaning
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _get_embeddings(self, texts):
        """Generate embeddings for texts using the Universal Sentence Encoder"""
        # Make sure texts is a list
        if isinstance(texts, str):
            texts = [texts]
        
        # Generate embeddings
        embeddings = self.model(texts)
        
        return embeddings.numpy()
    
    def _split_into_sentences(self, text):
        """Split text into sentences for processing"""
        # Simple sentence splitting using regex
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _chunk_sentences(self, sentences, chunk_size=3):
        """Group sentences into chunks for processing"""
        chunks = []
        for i in range(0, len(sentences), chunk_size):
            chunk = " ".join(sentences[i:i+chunk_size])
            chunks.append(chunk)
        return chunks
    
    def _find_most_relevant_chunks(self, question, chunks, top_k=3):
        """Find the most relevant text chunks for the question"""
        if not chunks:
            return [], []
            
        # If only one chunk, return it
        if len(chunks) == 1:
            return chunks, [1.0]
        
        try:
            # Get embeddings for question and chunks
            question_embedding = self._get_embeddings([question])
            chunk_embeddings = self._get_embeddings(chunks)
            
            # Calculate cosine similarities
            similarities = cosine_similarity(question_embedding, chunk_embeddings)[0]
            
            # Get top-k chunk indices and scores
            top_k = min(top_k, len(chunks))
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            top_scores = [similarities[i] for i in top_indices]
            
            # Get the top chunks
            top_chunks = [chunks[i] for i in top_indices]
            
            return top_chunks, top_scores
            
        except Exception as e:
            self.logger.error(f"Error finding relevant chunks: {str(e)}")
            # Fallback to first chunk
            return [chunks[0]], [0.5]
    
    def _extract_answer(self, question, top_chunks, top_scores):
        """Extract the answer from the most relevant chunks"""
        try:
            if not top_chunks:
                return "I couldn't find relevant information in the provided content.", 0.1, ""
            
            # Split chunks into sentences for more granular matching
            all_sentences = []
            for chunk in top_chunks:
                sentences = self._split_into_sentences(chunk)
                all_sentences.extend(sentences)
            
            if not all_sentences:
                return top_chunks[0], top_scores[0], top_chunks[0]
            
            # Get embeddings for question and sentences
            question_embedding = self._get_embeddings([question])
            sentence_embeddings = self._get_embeddings(all_sentences)
            
            # Calculate similarities
            similarities = cosine_similarity(question_embedding, sentence_embeddings)[0]
            
            # Get top-5 sentence indices
            top_k = min(5, len(all_sentences))
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            top_values = [similarities[i] for i in top_indices]
            
            # Get the top sentences
            top_sentences = [all_sentences[i] for i in top_indices]
            
            # Construct answer from top sentences (max 3)
            answer_sentences = top_sentences[:3]
            answer = " ".join(answer_sentences)
            
            # Calculate confidence based on similarity scores
            confidence = top_values[0] if top_values else 0.5
            
            # Provide wider context
            context_sentences = top_sentences
            context = " ".join(context_sentences)
            
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
        self.logger.info(f"Answering question using TensorFlow USE: {question}")
        
        if not content or not question:
            return "No content available to answer this question.", 0.0, ""
        
        # Preprocess
        question = self._preprocess_text(question)
        content = self._preprocess_text(content)
        
        # Split content into sentences and then chunks
        sentences = self._split_into_sentences(content)
        chunks = self._chunk_sentences(sentences)
        
        # Find most relevant chunks
        top_chunks, top_scores = self._find_most_relevant_chunks(question, chunks)
        
        # Extract answer from the most relevant chunks
        answer, confidence, context = self._extract_answer(question, top_chunks, top_scores)
        
        return answer, confidence, context