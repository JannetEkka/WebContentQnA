import React from 'react';
import { Card, ListGroup, Badge } from 'react-bootstrap';

const QuestionHistory = ({ history, onSelectQuestion }) => {
  // Format timestamp to a readable format
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Helper function to get model badge color
  const getModelBadgeColor = (model) => {
    return model === 'distilbert' ? 'info' : 'secondary';
  };

  // Helper function to truncate question if too long
  const truncateQuestion = (question, maxLength = 60) => {
    if (question.length <= maxLength) return question;
    return question.substring(0, maxLength) + '...';
  };

  return (
    <Card className="shadow-sm">
      <Card.Body>
        <Card.Title>Question History</Card.Title>
        {history.length === 0 ? (
          <p className="text-muted">No questions asked yet</p>
        ) : (
          <ListGroup variant="flush">
            {history.map((item, index) => (
              <ListGroup.Item 
                key={index} 
                className="history-item" 
                onClick={() => onSelectQuestion(item.question)}
                action
              >
                <div className="d-flex justify-content-between align-items-start">
                  <div className="me-2">
                    <div>{truncateQuestion(item.question)}</div>
                    <small className="text-muted">{formatTime(item.timestamp)}</small>
                  </div>
                  <Badge bg={getModelBadgeColor(item.model)}>
                    {item.model === 'distilbert' ? 'DistilBERT' : 'TF-IDF'}
                  </Badge>
                </div>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Card.Body>
    </Card>
  );
};

export default QuestionHistory;