# Save this as test_distilbert.py in your project root
import logging
import sys
import os

# Add the backend directory to the path so we can import services
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')
sys.path.insert(0, backend_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Try to import the DistilBERT model
    logger.info("Attempting to import DistilBERTQuestionAnsweringModel...")
    from services.qa_model_distilbert import DistilBERTQuestionAnsweringModel
    
    # Try to initialize the model
    logger.info("Attempting to initialize DistilBERTQuestionAnsweringModel...")
    distilbert_model = DistilBERTQuestionAnsweringModel()
    
    # Test if model is working
    logger.info("Testing the model with a sample question...")
    sample_content = "Claude is an AI assistant created by Anthropic. It was designed to be helpful, harmless, and honest."
    sample_question = "Who created Claude?"
    
    answer, confidence, context = distilbert_model.answer_question(sample_question, sample_content)
    
    logger.info(f"Answer: {answer}")
    logger.info(f"Confidence: {confidence}")
    logger.info(f"Context: {context}")
    
    logger.info("DistilBERT is working correctly!")
    
except ImportError as e:
    logger.error(f"ImportError: {str(e)}")
    logger.error("Failed to import DistilBERTQuestionAnsweringModel. Make sure transformers and torch are installed.")
    
except Exception as e:
    logger.error(f"Error: {str(e)}")
    logger.error("Failed to initialize or use DistilBERTQuestionAnsweringModel.")