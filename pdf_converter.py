import os
import logging
import weasyprint
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_pdf(url, output_dir="data")-> str:
    try:
        # Convert the webpage content to a PDF using WeasyPrint
        pdf = weasyprint.HTML(url).write_pdf()

        # Check if the output directory exists; if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Extract the title and domain of the webpage
        title, domain = get_webpage_title(url)

        # Set a default title "Untitled" if the title extraction fails or returns an empty string
        if not title:
            title = "Untitled"

        # Generate the PDF file name based on the extracted domain and title, replacing spaces with underscores
        file_name = f"{domain}_{title.strip().replace(' ', '_')}.pdf"

        # Create the full file path by joining the output directory and the generated file name
        file_path = os.path.join(output_dir, file_name)

        # Write the generated PDF content to a file at the specified file path
        with open(file_path, 'wb') as f:
            f.write(pdf)

        # Log a success message indicating that the PDF was created successfully, along with the file path
        logger.info(f"PDF created successfully: {file_path}")

        # Return the file path of the generated PDF
        return file_path

    except Exception as e:
        # Catch any exceptions that occur during PDF creation, log an error message, and return None to indicate failure
        logger.error(f"Error creating PDF: {e}")
        return None
    

def get_webpage_title(url) -> tuple:
    try:
        # Parse the URL to extract its components
        parsed_url = urlparse(url)

        # Extract the domain from the parsed URL
        domain = parsed_url.netloc

        # Extract the title from the path component of the parsed URL
        title = os.path.basename(parsed_url.path)

        # Return the extracted title and domain
        return title, domain

    except Exception as e:
        # Log an error message and return None for both title and domain if an exception occurs
        logger.error(f"Error getting webpage title and domain: {e}")
        return None, None



# Test the DocumentHandler class
if __name__ == "__main__":
    # Example URL
    url = "https://en.wikipedia.org/wiki/Data_science"
    
    # Test create_pdf method
    create_pdf(url)
    
