import React, { useState } from 'react';
import { Form, Button, Card, OverlayTrigger, Tooltip } from 'react-bootstrap';
import axios from 'axios';
import { InfoCircle } from 'react-bootstrap-icons';

const UrlInput = ({ 
  setUrls, 
  setContent, 
  setLoading, 
  setError, 
  setContentLoaded,
  setProcessedUrls
}) => {
  const [urlInput, setUrlInput] = useState('');
  const [urlList, setUrlList] = useState([]);

  const handleUrlChange = (e) => {
    setUrlInput(e.target.value);
  };

  const addUrl = () => {
    if (urlInput.trim() === '') return;
    
    // Basic URL validation
    try {
      new URL(urlInput);
      
      if (!urlList.includes(urlInput)) {
        setUrlList([...urlList, urlInput]);
      }
      setUrlInput('');
    } catch (error) {
      setError('Please enter a valid URL');
      setTimeout(() => setError(''), 3000);
    }
  };

  const removeUrl = (index) => {
    const newUrlList = [...urlList];
    newUrlList.splice(index, 1);
    setUrlList(newUrlList);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (urlList.length === 0) {
      setError('Please add at least one URL');
      setTimeout(() => setError(''), 3000);
      return;
    }

    setLoading(true);
    setError('');
    setContentLoaded(false);

    try {
      const response = await axios.post('http://localhost:5000/api/extract', { urls: urlList });
      setUrls(urlList);
      setContent(response.data.content);
      setContentLoaded(true);
      setProcessedUrls(urlList); // Store processed URLs
    } catch (error) {
      console.error('Error extracting content:', error);
      setError(error.response?.data?.error || 'Failed to extract content from URLs');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addUrl();
    }
  };

  const renderTooltip = (props) => (
    <Tooltip id="button-tooltip" {...props}>
      Click "Add" to include this URL for content extraction
    </Tooltip>
  );

  return (
    <Card className="shadow-sm">
      <Card.Body>
        <Card.Title>Step 1: Enter URLs to Extract Content</Card.Title>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Website URLs</Form.Label>
            <div className="d-flex url-input-wrapper">
              <Form.Control
                type="text"
                placeholder="Enter URL (e.g., https://example.com)"
                value={urlInput}
                onChange={handleUrlChange}
                onKeyDown={handleKeyPress}
              />
              <OverlayTrigger
                placement="top"
                delay={{ show: 250, hide: 400 }}
                overlay={renderTooltip}
              >
                <span className="tooltip-icon">
                  <InfoCircle size={18} />
                </span>
              </OverlayTrigger>
              <Button variant="secondary" className="ms-2" onClick={addUrl}>
                Add URL
              </Button>
            </div>
          </Form.Group>

          {urlList.length > 0 && (
            <div className="mb-3">
              <p className="mb-2">URLs to extract content from:</p>
              <ul className="list-group">
                {urlList.map((url, index) => (
                  <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                    <span className="text-truncate" style={{ maxWidth: '80%' }}>{url}</span>
                    <Button variant="outline-danger" size="sm" onClick={() => removeUrl(index)}>
                      Remove
                    </Button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <Button variant="primary" type="submit" disabled={urlList.length === 0}>
            Extract Content
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default UrlInput;