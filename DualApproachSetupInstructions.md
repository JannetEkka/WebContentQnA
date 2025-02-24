# Dual QA Model Setup Instructions

Follow these steps to set up the Web Content Q&A Tool with both the lightweight and DistilBERT approaches:

## Project Structure Setup

From your project root (`D:\Projects\WebContentQnA`), organize your files as follows:

### Backend Files

1. Copy these files to the project root:
   - `app.py` (Updated version with dual model support)
   - `requirements.txt` (Updated version with optional DistilBERT dependencies)

2. Create/update the services directory:
   ```
   mkdir services (if it doesn't exist)
   ```

3. Inside the services directory, add/update:
   - `__init__.py` (Already there)
   - `extractor.py` (Already there)
   - `processor.py` (Already there)
   - `qa_model.py` (Already there)
   - `qa_model_distilbert.py` (New file for DistilBERT approach)

### Frontend Files

1. Inside the frontend/src directory:
   ```
   cd frontend/src
   mkdir components (if it doesn't exist)
   mkdir services (if it doesn't exist)
   ```

2. Inside the components directory, add/update:
   - `Header.jsx`
   - `UrlInput.jsx`
   - `QuestionInput.jsx` (Updated version with model selection)
   - `Answer.jsx` (Updated version showing model used)

3. Inside the services directory, add/update:
   - `api.js` (Updated version with model selection support)

4. Update the root App.jsx and App.css files

## Installation Steps

### Basic Installation (TF-IDF + spaCy only)

```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate

# Install basic dependencies
pip install Flask==2.3.3 flask-cors==4.0.0 requests==2.31.0 beautifulsoup4==4.12.2 html2text==2020.1.16 python-dotenv==1.0.0 lxml==4.9.3 nltk==3.8.1 scikit-learn>=1.0.0 spacy>=3.5.0

# Download spaCy model
python -m spacy download en_core_web_md
# Or for the smaller model:
# python -m spacy download en_core_web_sm
```

### Optional DistilBERT Installation

```bash
# Install PyTorch and Transformers for DistilBERT support
pip install torch==2.2.0+cpu transformers==4.35.0 --find-links https://download.pytorch.org/whl/torch_stable.html
```

Note: With DistilBERT, the application will require approximately 2GB more RAM. The app will work without DistilBERT, but will only offer the basic TF-IDF + spaCy model option.

## Running the Application

1. Start the backend:
   ```bash
   # From the project root
   python app.py
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm start
   ```

3. Access the application at: http://localhost:3000

## Verifying Installation

To verify that both models are working:

1. When the application loads, extract content from a URL
2. In Step 2, you should see two model options (if DistilBERT was installed correctly):
   - TF-IDF + spaCy
   - DistilBERT

If you only see the TF-IDF + spaCy option, check the console logs for any errors related to loading the DistilBERT model.