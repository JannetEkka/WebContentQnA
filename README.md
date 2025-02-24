# Web Content Q&A Tool

## Overview
A web-based tool that allows users to enter one or more URLs, extract content from those pages, and ask questions based on the extracted information. The tool provides concise, accurate answers using only the ingested content without relying on general knowledge.

Built with:
- React (frontend)
- Flask (backend API)
- HuggingFace DistilBERT (question answering model)

## Getting Started
### Prerequisites
- Node.js (v16 or higher) for frontend
- Python 3.8+ for backend
- NPM or Yarn
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/web-content-qa-tool.git

# Navigate to the project directory
cd web-content-qa-tool

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

## Usage
### Running Locally
```bash
# Start the backend server (from the backend directory)
cd backend
python app.py

# Start the frontend development server (from the frontend directory)
cd frontend
npm start

# Open your browser and navigate to
http://localhost:3000
```

### How to Use
1. Enter one or more URLs in the input field
2. Click "Extract Content" to ingest the information
3. Ask questions in the query box about the extracted content
4. View the answers based solely on the ingested information

## Features
- URL content extraction and processing
- Natural language question answering based on extracted content
- User-friendly, minimal interface
- Real-time content ingestion and retrieval
- Support for multiple URLs

## Project Structure
```
web-content-qa-tool/
├── frontend/                  # React frontend
│   ├── public/                # Static assets
│   ├── src/                   # Source code
│   │   ├── components/        # React components
│   │   │   ├── Header.jsx     # App header
│   │   │   ├── UrlInput.jsx   # URL input component
│   │   │   ├── QuestionInput.jsx # Question input component
│   │   │   └── Answer.jsx     # Answer display component
│   │   ├── services/          # Service layer
│   │   │   └── api.js         # API client for backend communication
│   │   ├── utils/             # Utility functions
│   │   ├── App.jsx            # Main application component
│   │   ├── index.jsx          # Entry point
│   │   └── styles/            # CSS/styling files
│   ├── package.json           # Frontend dependencies and scripts
│   └── .gitignore             # Frontend-specific gitignore
├── backend/                   # Flask backend
│   ├── app.py                 # Main Flask application
│   ├── services/              # Backend services
│   │   ├── extractor.py       # URL content extraction service
│   │   ├── processor.py       # Content processing logic
│   │   └── qa_model.py        # DistilBERT question answering logic
│   ├── utils/                 # Utility functions
│   ├── requirements.txt       # Python dependencies
│   └── .gitignore             # Backend-specific gitignore
├── tests/                     # Test files
├── .gitignore                 # Global gitignore file
├── README.md                  # This file
└── LICENSE                    # License information
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
Jannet Akanksha Ekka - jannetekka96@gmail.com