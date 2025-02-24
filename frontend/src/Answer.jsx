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

  return (
    <Card className="shadow-sm">
      <Card.Body>
        <Card.Title className="d-flex justify-content-between align-items-center">
          <span>Answer</span>
          <Badge 
            bg={getConfidenceColor(answer.confidence)}
            className="ms-2"
          >
            Confidence: {formatConfidence(answer.confidence)}
          </Badge>
        </Card.Title>
        <Card.Subtitle className="mb-3 text-muted">
          Q: {answer.question}
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