import re
import nltk
from nltk.tokenize import sent_tokenize
import logging

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ContentProcessor:
    """Process and clean extracted content"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process(self, content):
        """
        Process and clean the extracted content
        
        Args:
            content (str): Raw content extracted from URL
            
        Returns:
            str: Processed content
        """
        self.logger.info("Processing content")
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', content)
        
        # Remove markdown syntax
        processed = re.sub(r'##+', '', processed)  # Remove heading markers
        processed = re.sub(r'\*\*|\*', '', processed)  # Remove bold/italic markers
        processed = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', processed)  # Replace links with just the text
        processed = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', processed)  # Remove images
        processed = re.sub(r'```[^`]*```', '', processed)  # Remove code blocks
        
        # Remove URLs
        processed = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', processed)
        
        # Replace multiple newlines with a single one
        processed = re.sub(r'\n+', '\n', processed)
        
        # Remove any remaining special characters
        processed = re.sub(r'[^\w\s\.\,\;\:\-\'\"\?\!]', ' ', processed)
        
        # Final cleanup of extra spaces
        processed = re.sub(r'\s+', ' ', processed).strip()
        
        return processed
    
    def summarize(self, content, max_sentences=5):
        """
        Create a brief summary of the content
        
        Args:
            content (str): Processed content
            max_sentences (int): Maximum number of sentences to include
            
        Returns:
            str: Summary of the content
        """
        try:
            # Split into sentences
            sentences = sent_tokenize(content)
            
            # Take first few sentences as summary
            summary_sentences = sentences[:max_sentences]
            summary = ' '.join(summary_sentences)
            
            # Truncate if too long
            if len(summary) > 500:
                summary = summary[:497] + '...'
                
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating summary: {str(e)}")
            # Return truncated content if summarization fails
            return content[:500] + '...' if len(content) > 500 else content