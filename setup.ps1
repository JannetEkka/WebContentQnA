# Create project structure
mkdir -p web-content-qa-tool/frontend/src/components
mkdir -p web-content-qa-tool/frontend/src/services
mkdir -p web-content-qa-tool/services

# Navigate to project folder
cd web-content-qa-tool

# Set up backend
python -m venv venv
./venv/Scripts/Activate.ps1  # For PowerShell
# source venv/bin/activate  # For Bash

# Install basic backend dependencies
pip install Flask==2.3.3 flask-cors==4.0.0 requests==2.31.0 beautifulsoup4==4.12.2 html2text==2020.1.16 python-dotenv==1.0.0 lxml==4.9.3 nltk==3.8.1 scikit-learn>=1.3.0 spacy>=3.5.0

# Download spaCy model (choose one)
python -m spacy download en_core_web_md
# python -m spacy download en_core_web_sm  # Smaller alternative

# Optional: Install DistilBERT dependencies
# pip install torch==2.2.0+cpu transformers==4.35.0 --find-links https://download.pytorch.org/whl/torch_stable.html

# Set up frontend
cd frontend
npm init -y
npm install react react-dom react-bootstrap bootstrap@5.3.3 axios react-bootstrap-icons
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event react-scripts web-vitals

# Add start script to package.json
# "scripts": {
#   "start": "react-scripts start",
#   "build": "react-scripts build",
#   "test": "react-scripts test",
#   "eject": "react-scripts eject"
# }

# Start the application (in two separate terminals)
# Terminal 1 (Backend):
cd web-content-qa-tool
./venv/Scripts/Activate.ps1  # For PowerShell
python app.py

# Terminal 2 (Frontend):
cd web-content-qa-tool/frontend
npm start