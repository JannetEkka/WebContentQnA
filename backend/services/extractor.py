import requests
from bs4 import BeautifulSoup
import html2text
import logging

class ContentExtractor:
    """Extract content from URLs"""
    
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = True
        self.converter.ignore_emphasis = False
        self.converter.body_width = 0  # No wrapping
        self.logger = logging.getLogger(__name__)
    
    def extract(self, url):
        """
        Extract content from a URL
        
        Args:
            url (str): URL to extract content from
            
        Returns:
            str: Extracted content
            
        Raises:
            Exception: If extraction fails
        """
        self.logger.info(f"Extracting content from {url}")
        
        try:
            # Send request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style", "header", "footer", "nav"]):
                script.extract()
            
            # Extract title
            title = ""
            if soup.title:
                title = soup.title.get_text()
            
            # Extract main content - focus on article, main, or content divs if available
            main_content = soup.find('article') or soup.find('main') or soup.find(id='content') or soup
            
            # Convert HTML to text
            text_content = self.converter.handle(str(main_content))
            
            # Combine title and content
            full_content = f"# {title}\n\n{text_content}" if title else text_content
            
            return full_content
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error for {url}: {str(e)}")
            raise Exception(f"Failed to fetch content from {url}: {str(e)}")
        
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {str(e)}")
            raise Exception(f"Error processing content from {url}: {str(e)}")