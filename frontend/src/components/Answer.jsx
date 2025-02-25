import React from 'react';
import { Card, Badge } from 'react-bootstrap';

const Answer = ({ answer }) => {
  // Helper function to determine confidence level color
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.7) return 'success';
    if (confidence >= 0.4) return 'warning';
    return 'danger';
  };

  // Helper function to format confidence as percentage
  const formatConfidence = (confidence) => {
    return `${Math.round(confidence * 100)}%`;
  };

  // Helper function to get model badge color
  const getModelBadgeColor = (model) => {
    switch(model) {
      case 'tensorflow':
        return 'primary';
      case 'nltk-advanced':
        return 'success';
      case 'distilbert':
        return 'info';
      default:
        return 'secondary';
    }
  };

  // Helper function to get model display name
  const getModelDisplayName = (model) => {
    switch(model) {
      case 'tensorflow':
        return 'TensorFlow USE';
      case 'nltk-advanced':
        return 'NLTK Advanced';
      case 'distilbert':
        return 'DistilBERT';
      default:
        return 'TF-IDF + spaCy';
    }
  };

  // Format timestamp if available
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <Card className="shadow-sm">
      <Card.Body>
        <Card.Title className="d-flex justify-content-between align-items-center">
          <span>Answer</span>
          <div>
            <Badge 
              bg={getModelBadgeColor(answer.model_used)}
              className="me-2"
            >
              {getModelDisplayName(answer.model_used)}
            </Badge>
            <Badge 
              bg={getConfidenceColor(answer.confidence)}
            >
              Confidence: {formatConfidence(answer.confidence)}
            </Badge>
          </div>
        </Card.Title>
        <Card.Subtitle className="mb-3 text-muted">
          Q: {answer.question}
          {answer.timestamp && (
            <small className="d-block mt-1">
              {formatTimestamp(answer.timestamp)}
            </small>
          )}
        </Card.Subtitle>
        <Card.Text className="border-bottom pb-3">
          {answer.answer}
        </Card.Text>
        
        {answer.context && (
          <div className="mt-3">
            <small className="text-muted">
              <strong>Context:</strong> {answer.context}
            </small>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default Answer;