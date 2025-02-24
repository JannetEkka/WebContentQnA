import React, { useState, useRef, useEffect } from 'react';
import { Container, Row, Col, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/App.css';
import Header from './components/Header';
import UrlInput from './components/UrlInput';
import QuestionInput from './components/QuestionInput';
import Answer from './components/Answer';
import QuestionHistory from './components/QuestionHistory';

function App() {
  const [urls, setUrls] = useState([]);
  const [content, setContent] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [contentLoaded, setContentLoaded] = useState(false);
  const [processedUrls, setProcessedUrls] = useState([]);
  const [questionHistory, setQuestionHistory] = useState([]);

  const answerRef = useRef(null);

  useEffect(() => {
    if (answer && answerRef.current) {
      answerRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [answer]);

  // Function to add a question to history
  const addToHistory = (questionData) => {
    const newHistory = [questionData, ...questionHistory];
    // Limit history to most recent 10 items
    if (newHistory.length > 10) {
      newHistory.pop();
    }
    setQuestionHistory(newHistory);
  };

  // Select a question from history
  const selectFromHistory = (question) => {
    setQuestion(question);
  };

  return (
    <div className="App">
      <Header />
      <Container className="mt-4">
        <Row>
          <Col md={8}>
            <UrlInput 
              setUrls={setUrls} 
              setContent={setContent} 
              setLoading={setLoading} 
              setError={setError}
              setContentLoaded={setContentLoaded}
              setProcessedUrls={setProcessedUrls}
            />
          </Col>
          <Col md={4}>
            <QuestionHistory 
              history={questionHistory} 
              onSelectQuestion={selectFromHistory} 
            />
          </Col>
        </Row>

        {contentLoaded && (
          <Row className="mt-4">
            <Col md={8}>
              <QuestionInput 
                question={question}
                setQuestion={setQuestion}
                setAnswer={setAnswer}
                setLoading={setLoading}
                setError={setError}
                urls={urls}
                addToHistory={addToHistory}
              />
            </Col>
            <Col md={4}>
              <div className="card shadow-sm">
                <div className="card-body">
                  <h5 className="card-title">Processed URLs</h5>
                  <ul className="list-group">
                    {processedUrls.map((url, index) => (
                      <li key={index} className="list-group-item">
                        <small className="text-truncate d-block">{url}</small>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </Col>
          </Row>
        )}

        {answer && (
          <Row className="mt-4" ref={answerRef}>
            <Col md={12}>
              <Answer answer={answer} />
            </Col>
          </Row>
        )}

        {loading && (
          <div className="loading-overlay">
            <div className="loading-content">
              <Spinner animation="border" role="status" variant="primary">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
              <p className="mt-2">Processing your request...</p>
            </div>
          </div>
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