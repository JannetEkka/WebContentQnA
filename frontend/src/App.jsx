import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Header from './components/Header';
import UrlInput from './components/UrlInput';
import QuestionInput from './components/QuestionInput';
import Answer from './components/Answer';

function App() {
  const [urls, setUrls] = useState([]);
  const [content, setContent] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [contentLoaded, setContentLoaded] = useState(false);

  return (
    <div className="App">
      <Header />
      <Container className="mt-4">
        <Row>
          <Col md={12}>
            <UrlInput 
              setUrls={setUrls} 
              setContent={setContent} 
              setLoading={setLoading} 
              setError={setError}
              setContentLoaded={setContentLoaded}
            />
          </Col>
        </Row>

        {contentLoaded && (
          <Row className="mt-4">
            <Col md={12}>
              <QuestionInput 
                question={question}
                setQuestion={setQuestion}
                setAnswer={setAnswer}
                setLoading={setLoading}
                setError={setError}
                urls={urls}
              />
            </Col>
          </Row>
        )}

        {answer && (
          <Row className="mt-4">
            <Col md={12}>
              <Answer answer={answer} />
            </Col>
          </Row>
        )}

        {loading && (
          <Row className="mt-4">
            <Col md={12} className="text-center">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
            </Col>
          </Row>
        )}

        {error && (
          <Row className="mt-4">
            <Col md={12}>
              <div className="alert alert-danger">{error}</div>
            </Col>
          </Row>
        )}
      </Container>
    </div>
  );
}

export default App;