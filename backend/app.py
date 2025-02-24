from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from services.extractor import ContentExtractor
from services.processor import ContentProcessor
from services.qa_model import QuestionAnsweringModel

# Optional import of DistilBERT model
try:
    from services.qa_model_distilbert import DistilBERTQuestionAnsweringModel
    DISTILBERT_AVAILABLE = True
except ImportError:
    DISTILBERT_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
extractor = ContentExtractor()
processor = ContentProcessor()
qa_model = QuestionAnsweringModel()

# Initialize DistilBERT model if available
distilbert_model = None
if DISTILBERT_AVAILABLE:
    try:
        distilbert_model = DistilBERTQuestionAnsweringModel()
        logger.info("DistilBERT model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize DistilBERT model: {str(e)}")
        distilbert_model = None

# In-memory content store (in a real app, consider using a database)
extracted_content = {}

@app.route('/api/extract', methods=['POST'])
def extract_content():
    """Extract content from URLs"""
    try:
        data = request.json
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({"error": "No URLs provided"}), 400
        
        logger.info(f"Extracting content from {len(urls)} URLs")
        
        # Process each URL
        all_content = ""
        for url in urls:
            try:
                # Extract content
                content = extractor.extract(url)
                
                # Process content
                processed_content = processor.process(content)
                
                # Add to combined content
                all_content += f"\n\n--- Content from {url} ---\n\n{processed_content}"
                
                # Store content for this URL
                extracted_content[url] = processed_content
                
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
                return jsonify({"error": f"Error processing {url}: {str(e)}"}), 500
        
        # Create a summary
        summary = processor.summarize(all_content)
        
        return jsonify({
            "message": "Content extracted successfully",
            "content": all_content,
            "summary": summary,
            "url_count": len(urls)
        })
        
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

@app.route('/api/answer', methods=['POST'])
def answer_question():
    """Answer a question based on extracted content"""
    try:
        data = request.json
        question = data.get('question', '')
        urls = data.get('urls', [])
        model_type = data.get('model_type', 'default')  # 'default' or 'distilbert'
        
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        if not urls:
            return jsonify({"error": "No URLs provided"}), 400
        
        logger.info(f"Answering question using {model_type} model: {question}")
        
        # Check if distilbert is requested but not available
        if model_type == 'distilbert' and not distilbert_model:
            logger.warning("DistilBERT model requested but not available, falling back to default model")
            model_type = 'default'
        
        # Combine content from all URLs
        combined_content = ""
        for url in urls:
            if url in extracted_content:
                combined_content += f"\n\n{extracted_content[url]}"
            else:
                logger.warning(f"Content for {url} not found in cache")
        
        if not combined_content:
            # If no content in cache, extract it now (fallback)
            for url in urls:
                try:
                    content = extractor.extract(url)
                    processed_content = processor.process(content)
                    combined_content += f"\n\n{processed_content}"
                    extracted_content[url] = processed_content
                except Exception as e:
                    logger.error(f"Error extracting content from {url}: {str(e)}")
        
        # Get answer based on selected model
        if model_type == 'distilbert' and distilbert_model:
            answer, confidence, context = distilbert_model.answer_question(question, combined_content)
            model_used = 'distilbert'
        else:
            answer, confidence, context = qa_model.answer_question(question, combined_content)
            model_used = 'default'
        
        return jsonify({
            "answer": answer,
            "confidence": confidence,
            "context": context,
            "model_used": model_used
        })
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({"error": f"Failed to answer question: {str(e)}"}), 500

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Get available QA models"""
    models = {
        "default": {
            "name": "TF-IDF + spaCy",
            "description": "Lightweight model using TF-IDF and spaCy for efficient question answering",
            "available": True
        },
        "distilbert": {
            "name": "DistilBERT",
            "description": "HuggingFace's DistilBERT model fine-tuned for question answering",
            "available": distilbert_model is not None
        }
    }
    
    return jsonify({
        "models": models,
        "default": "default"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)