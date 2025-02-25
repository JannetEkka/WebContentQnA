import nltk
import re
import string
import logging
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class NLTKQuestionAnsweringModel:
    """Answer questions based on content using NLTK and advanced NLP techniques"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.logger.info("Initialized NLTK Advanced QA Model")
    
    def _preprocess_text(self, text):
        """Clean and preprocess text"""
        # Basic cleaning
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        # Remove punctuation
        text = "".join([char for char in text if char not in string.punctuation])
        return text
    
    def _tokenize_and_lemmatize(self, text):
        """Tokenize and lemmatize text"""
        words = word_tokenize(text)
        # Remove stopwords and lemmatize
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        return words
    
    def _extract_key_terms(self, question):
        """Extract key terms from the question"""
        processed_q = self._preprocess_text(question)
        tokens = self._tokenize_and_lemmatize(processed_q)
        
        # Identify question type
        q_words = ['what', 'when', 'where', 'who', 'why', 'how', 'which']
        q_type = None
        for word in q_words:
            if word in processed_q.split():
                q_type = word
                break
        
        # Filter out question words
        key_terms = [term for term in tokens if term not in q_words]
        
        return key_terms, q_type
    
    def _split_into_sentences(self, text):
        """Split text into sentences for processing"""
        sentences = sent_tokenize(text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def _score_sentences(self, sentences, key_terms, q_type):
        """Score sentences based on key terms and question type"""
        sentence_scores = []
        
        for sentence in sentences:
            score = 0
            processed_s = self._preprocess_text(sentence)
            s_tokens = self._tokenize_and_lemmatize(processed_s)
            
            # Score based on key term matches
            for term in key_terms:
                if term in s_tokens:
                    score += 2  # Higher weight for exact matches
            
            # Adjust score based on sentence length (penalize very short or very long)
            length = len(s_tokens)
            if 5 <= length <= 25:
                score += 1
            elif length > 25:
                score -= 1
                
            # Boost sentences with potential entities if question asks for them
            if q_type in ['who', 'where', 'when']:
                # Simple entity detection (could be improved with NER)
                if any(word[0].isupper() for word in sentence.split()):
                    score += 1
                # Date/time indicators for 'when' questions
                if q_type == 'when' and any(re.search(r'\d{4}|\bday\b|\bmonth\b|\byear\b|\bdate\b|\btime\b', sentence.lower())):
                    score += 1.5
                # Location indicators for 'where' questions
                if q_type == 'where' and any(re.search(r'\bin\b|\bat\b|\bnear\b|\blocation\b|\bplace\b|\bcountry\b|\bcity\b', sentence.lower())):
                    score += 1.5
            
            sentence_scores.append((sentence, score))
        
        # Sort by score in descending order
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        return sentence_scores
    
    def _find_most_relevant_chunks(self, question, text):
        """Split text into chunks and find most relevant ones"""
        sentences = self._split_into_sentences(text)
        
        if not sentences:
            return [], 0
        
        key_terms, q_type = self._extract_key_terms(question)
        
        # For short text, just use all sentences
        if len(sentences) <= 10:
            return sentences, 0.7
            
        # Score all sentences
        scored_sentences = self._score_sentences(sentences, key_terms, q_type)
        
        # Use TF-IDF to find semantic similarity between question and sentences
        try:
            # Create a corpus with the question and all sentences
            corpus = [question] + [s[0] for s in scored_sentences]
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            # Calculate cosine similarity between question and each sentence
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            # Combine TF-IDF similarity with our custom scoring
            for i, (sent, score) in enumerate(scored_sentences):
                scored_sentences[i] = (sent, score + (similarities[i] * 3))  # Weight TF-IDF higher
                
            # Re-sort after adding TF-IDF scores
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            
            # Take top 5 sentences or fewer
            top_sentences = [s[0] for s in scored_sentences[:5]]
            avg_score = sum([s[1] for s in scored_sentences[:5]]) / len(scored_sentences[:5]) if scored_sentences else 0
            confidence = min(avg_score / 10, 0.95)  # Normalize to 0-1 range
            
            return top_sentences, confidence
            
        except Exception as e:
            self.logger.error(f"Error in TF-IDF processing: {str(e)}")
            # Fallback to basic scoring
            top_sentences = [s[0] for s in scored_sentences[:5]]
            return top_sentences, 0.5
    
    def _extract_answer(self, question, relevant_sentences):
        """Extract and format the answer from relevant sentences"""
        if not relevant_sentences:
            return "I couldn't find information related to your question in the provided content.", 0.1, ""
        
        key_terms, q_type = self._extract_key_terms(question)
        
        # For factoid questions, prefer shortest complete sentence with answer
        if q_type in ['who', 'what', 'when', 'where', 'which']:
            # Sort by length but keep only sentences with high term overlap
            candidate_sentences = []
            for sentence in relevant_sentences:
                s_tokens = self._tokenize_and_lemmatize(self._preprocess_text(sentence))
                overlap = sum(1 for term in key_terms if term in s_tokens)
                if overlap >= len(key_terms) * 0.5:  # At least 50% of terms match
                    candidate_sentences.append((sentence, len(sentence)))
            
            # If we have good candidates, sort by length and take shortest
            if candidate_sentences:
                candidate_sentences.sort(key=lambda x: x[1])
                answer = candidate_sentences[0][0]
                confidence = 0.8
                context = ' '.join(relevant_sentences)
                return answer, confidence, context
        
        # For 'why' and 'how' questions or if no good factoid candidate, return top 2 sentences
        answer = ' '.join(relevant_sentences[:2])
        context = ' '.join(relevant_sentences)
        confidence = 0.7 if len(relevant_sentences) >= 2 else 0.5
        
        return answer, confidence, context
    
    def answer_question(self, question, content):
        """
        Answer a question based on the content
        
        Args:
            question (str): Question to answer
            content (str): Content to search for answers
            
        Returns:
            tuple: (answer, confidence, context)
        """
        self.logger.info(f"Answering question using NLTK: {question}")
        
        if not content or not question:
            return "No content available to answer this question.", 0.0, ""
        
        # Find relevant sentences
        relevant_chunks, chunk_confidence = self._find_most_relevant_chunks(question, content)
        
        # Extract the answer
        answer, answer_confidence, context = self._extract_answer(question, relevant_chunks)
        
        # Combine confidences
        confidence = (chunk_confidence + answer_confidence) / 2
        
        return answer, confidence, context