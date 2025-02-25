import React, { useState, useEffect } from 'react';
import { Form, Button, Card, ToggleButtonGroup, ToggleButton } from 'react-bootstrap';
import axios from 'axios';

const QuestionInput = ({ 
  question, 
  setQuestion, 
  setAnswer, 
  setLoading, 
  setError,
  urls,
  addToHistory
}) => {
  const [selectedModel, setSelectedModel] = useState('default');
  const [availableModels, setAvailableModels] = useState({});

  useEffect(() => {
    // Fetch available models when component mounts
    const fetchModels = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/models');
        setAvailableModels(response.data.models);
        setSelectedModel(response.data.default);
      } catch (error) {
        console.error('Error fetching models:', error);
        // Fallback to default model if API call fails
        setAvailableModels({
          default: {
            name: 'TF-IDF + spaCy',
            description: 'Lightweight model using TF-IDF and spaCy',
            available: true
          }
        });
      }
    };

    fetchModels();
  }, []);

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleModelChange = (val) => {
    setSelectedModel(val);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (question.trim() === '') {
      setError('Please enter a question');
      setTimeout(() => setError(''), 3000);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/answer', { 
        question,
        urls,
        model_type: selectedModel
      });
      
      const answerData = {
        question,
        answer: response.data.answer,
        confidence: response.data.confidence,
        context: response.data.context,
        model_used: response.data.model_used,
        timestamp: new Date().toISOString()
      };
      
      setAnswer(answerData);
      
      // Add to question history
      addToHistory({
        question,
        timestamp: new Date().toISOString(),
        model: response.data.model_used
      });
    } catch (error) {
      console.error('Error getting answer:', error);
      setError(error.response?.data?.error || 'Failed to get answer');
    } finally {
      setLoading(false);
    }
  };

  // Helper function to get button variant based on model type
  const getModelButtonVariant = (modelKey) => {
    switch(modelKey) {
      case 'tensorflow': 
        return 'outline-primary';
      case 'nltk-advanced': 
        return 'outline-success';
      case 'distilbert': 
        return 'outline-info';
      default:
        return 'outline-secondary';
    }
  };

  return (
    <Card className="shadow-sm">
      <Card.Body>
        <Card.Title>Step 2: Ask a Question</Card.Title>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Your Question</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              placeholder="Enter your question about the extracted content"
              value={question}
              onChange={handleQuestionChange}
            />
          </Form.Group>

          {Object.keys(availableModels).length > 1 && (
            <Form.Group className="mb-3">
              <Form.Label>Select QA Model</Form.Label>
              <div>
                <ToggleButtonGroup 
                  type="radio" 
                  name="model-options" 
                  value={selectedModel}
                  onChange={handleModelChange}
                >
                  {Object.entries(availableModels).map(([key, model]) => (
                    <ToggleButton
                      key={key}
                      id={`model-${key}`}
                      value={key}
                      variant={getModelButtonVariant(key)}
                      disabled={!model.available}
                    >
                      {model.name}
                    </ToggleButton>
                  ))}
                </ToggleButtonGroup>
              </div>
              <Form.Text className="text-muted">
                {availableModels[selectedModel]?.description}
              </Form.Text>
            </Form.Group>
          )}

          <Button variant="primary" type="submit" disabled={!question.trim()}>
            Get Answer
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default QuestionInput;