# Web Content Q&A Tool

A web-based tool that allows users to enter one or more URLs, extract content from those pages, and ask questions based on the extracted information. The tool provides concise, accurate answers using only the ingested content.

## Features

- URL content extraction and processing
- Natural language question answering based on extracted content
- Support for multiple QA models:
  - Lightweight TF-IDF + spaCy approach (default)
  - HuggingFace DistilBERT (optional)
- User-friendly, minimal interface
- Real-time content ingestion and retrieval
- Support for multiple URLs
- Confidence scoring for answers

## Technologies Used

- **Frontend**: React, Bootstrap, Axios
- **Backend**: Flask, Python
- **NLP Options**: 
  - Basic: spaCy, scikit-learn (TF-IDF)
  - Advanced: HuggingFace Transformers (DistilBERT)

## Installation

### Prerequisites

- Python 3.8+ (with pip)
- Node.js and npm
- Git (optional)

### Setup

1. **Clone or download this repository**

```bash
git clone <repository-url>
cd web-content-qa-tool
```

2. **Set up the backend**

```bash
# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install basic backend dependencies
pip install Flask==2.3.3 flask-cors==4.0.0 requests==2.31.0 beautifulsoup4==4.12.2 html2text==2020.1.16 python-dotenv==1.0.0 lxml==4.9.3 nltk==3.8.1 scikit-learn>=1.0.0 spacy>=3.5.0

# Download spaCy model
python -m spacy download en_core_web_md
# If the above fails due to space/memory constraints, you can use the smaller model:
# python -m spacy download en_core_web_sm
```

3. **(Optional) Install DistilBERT dependencies**

```bash
# Only run this if you want to use the DistilBERT model
pip install torch==2.2.0+cpu transformers==4.35.0 --find-links https://download.pytorch.org/whl/torch_stable.html
```

4. **Set up the frontend**

```bash
# Navigate to the frontend directory
cd frontend

# Install frontend dependencies
npm install
```

## Running the Application

1. **Start the backend server**

```bash
# Make sure your virtual environment is activated
# From the project root directory
python app.py
```

The Flask server will start on http://localhost:5000

2. **Start the frontend development server**

In a new terminal:

```bash
# Navigate to the frontend directory
cd frontend

# Start the development server
npm start
```

The React application will start and open in your browser at http://localhost:3000

## How to Use

1. Enter one or more URLs in the input field and click "Add" for each URL
2. Click "Extract Content" to process the web pages
3. Once content is extracted, enter your question in the query box
4. (Optional) Select the QA model you want to use:
   - TF-IDF + spaCy (faster, lightweight)
   - DistilBERT (more accurate, requires more resources)
5. Click "Get Answer" to receive a response based on the extracted content
6. View the answer along with its confidence score and the model used

## QA Model Comparison

### TF-IDF + spaCy (Default)
- **Pros**: Fast, lightweight, works on systems with limited resources
- **Cons**: Less accurate for complex questions
- **Best for**: Simple factual questions, systems with limited memory

### DistilBERT
- **Pros**: More accurate, better understanding of context and semantics
- **Cons**: Requires more memory and processing power, slower response time
- **Best for**: Complex questions, nuanced understanding, when accuracy is critical

## Project Structure

```
web-content-qa-tool/
├── backend/
│   ├── services/                      # Backend services
│   │   ├── __init__.py
│   │   ├── extractor.py               # URL content extraction service
│   │   ├── processor.py               # Content processing logic
│   │   ├── qa_model.py                # TF-IDF question answering logic
│   │   └── qa_model_distilbert.py     # DistilBERT question answering logic (optional)
│   ├── utils/
│   ├── requirements.txt                # Python dependencies
│   ├── package.json
│   ├── package-lock.json
│   └── .gitignore
│   
├── frontend/                          # React frontend
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── UrlInput.jsx
│   │   │   ├── QuestionInput.jsx
│   │   │   ├── QuestionHistory.jsx
│   │   │   └── Answer.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── App.css
│   │   ├── App.jsx
│   │   ├── App.test.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── .gitignore
│   ├── package-lock.json
│   └── package.json
│   └── README.md
│   
├── node_modules/
│   
├── tests/
│   ├── .gitignore
│   ├── app.py
│   ├── basic_requirements.txt
│   ├── DualApproachSetupInstructions.md
│   ├── LICENSE
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── test_distilbert.py

``` 

## Limitations

- The tool only answers questions based on the content it extracts from the provided URLs
- Text extraction may not be perfect for all websites, especially those with complex layouts
- The lightweight model (TF-IDF + spaCy) may struggle with complex or nuanced questions
- Some websites may block web scraping attempts
- The DistilBERT model requires significant memory resources and may not work on systems with limited RAM

## Performance Considerations

- For systems with limited resources (< 4GB available RAM), use only the lightweight model
- The first query using DistilBERT will be slower as the model needs to load into memory
- Extracting content from multiple complex webpages may require additional memory
- For faster performance, limit the number of URLs processed simultaneously

## Troubleshooting

- If you encounter CORS issues, make sure both the backend and frontend are running
- If content extraction fails, check if the website allows scraping or try a different URL
- For spaCy model issues, try using the smaller 'en_core_web_sm' model if memory is constrained
- If DistilBERT fails to load, ensure you have at least 4GB of free RAM
- Check the console logs for specific error messages if the application isn't working correctly

## Future Enhancements

- Add caching for extracted content to improve performance
- Implement more advanced text extraction for complex websites
- Add support for PDF and other document formats
- Implement pagination for handling very large content
- Add user authentication and saved question history

## License

This project is licensed under the MIT License - see the LICENSE file for details.