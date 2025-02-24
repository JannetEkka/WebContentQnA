import React from 'react';
import { Form, Button, Card } from 'react-bootstrap';
import axios from 'axios';

const QuestionInput = ({ 
  question, 
  setQuestion, 
  setAnswer, 
  setLoading, 
  setError,
  urls 
}) => {
  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
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
        urls
      });
      
      setAnswer({
        question,
        answer: response.data.answer,
        confidence: response.data.confidence,
        context: response.data.context
      });
    } catch (error) {
      console.error('Error getting answer:', error);
      setError(error.response?.data?.error || 'Failed to get answer');
    } finally {
      setLoading(false);
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
          <Button variant="primary" type="submit" disabled={!question.trim()}>
            Get Answer
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default QuestionInput;