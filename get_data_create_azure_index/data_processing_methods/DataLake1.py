# Must-use packages
import re
import html
from bs4 import BeautifulSoup, Comment
from bs4 import MarkupResemblesLocatorWarning
import warnings
# Optional code to filter BeautifulSoup warnings from the terminal when running main.py
warnings.filterwarnings("ignore",category=MarkupResemblesLocatorWarning)


def clean_html_text(html_text: str) -> str: 
    html_text = re.sub(r'\s+', ' ', html_text).strip() # fixes spacing issue -> should be 1 space between every word now
    """
    Cleans up an HTML-scraped webpage into plain English text.
    - Removes all HTML tags.
    - Removes comments, CDATA sections, and inline styles or event attributes.
    - Decodes HTML entities (e.g., &amp; → &).
    - Removes excessive whitespace and non-breaking spaces.
    - Handles hex/decimal character references.
    """
    # Parse HTML and remove script/style elements
    soup = BeautifulSoup(html_text, "lxml")
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()  # Remove script and style tags
    
    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # Get text content
    text = soup.get_text()
    
    # Decode HTML entities (e.g., &amp; → &)
    text = html.unescape(text)
    
    # Remove CDATA sections
    text = re.sub(r'<!\[CDATA\[.*?\]\]>', '', text, flags=re.DOTALL)
    
    # Remove inline styles and event attributes (e.g., onclick, style="...")
    text = re.sub(r'style\s*=\s*"[^"]*"', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=\s*"[^"]*"', '', text, flags=re.IGNORECASE)
    
    # Replace non-breaking spaces and excessive whitespace
    text = text.replace('\xa0', ' ')  # Unicode non-breaking space
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    
    return text


def data_lake1_extract(data_lake_input, data_lake_format):
    # Change data_lake_input to ensure consistency
    data_lake_input = {key: clean_html_text(value) for key, value in data_lake_input.items()}

    # Initialize data_lake_output with the keys from data_lake_format and blank values
    data_lake_output = data_lake_format
    # Match identical fields
    data_lake_output["title"] = data_lake_input["title"]
    data_lake_output["link"] = data_lake_input["link"]
    data_lake_output["data_source"] = "data_lake1"
    data_lake_output["unparsed_body_data_lake1"] = data_lake_input["body"]
    # Return
    return data_lake_output