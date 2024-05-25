import os
import logging
import weasyprint
from urllib.parse import urlparse
from scraper import extract_main_domain_from_url, extract_title_from_url


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_pdf(url, output_dir="data")-> str:
    try:
        # Convert the webpage content to a PDF using WeasyPrint
        pdf = weasyprint.HTML(url).write_pdf()

        # Create the output directory if it does not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = get_pdf_file_path(url)
        # Write the generated PDF content to a file at the specified file path
        with open(file_path, 'wb') as f:
            f.write(pdf)

        # Log a success message indicating that the PDF was created successfully, along with the file path
        logger.info(f"PDF created successfully: {file_path}")

        # Return the file path of the generated PDF
        return file_path

    # Catch any exceptions that occur during PDF creation, log an error message, and return None to indicate failure
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
    

def extract_webpage_title_domain(url) -> tuple:
    try:
        domain = extract_main_domain_from_url(url)
        title = extract_title_from_url(url)

        if not title:
            raise RuntimeError('title is empty!')
        return title, domain
    except Exception as e:
        # Log an error message and return None for both title and domain if an exception occurs
        logger.error(f"Error getting webpage title and domain: {e}")
        # Set a default title "Untitled" if it fails for any reason
        return None, 'Untitled'


def get_pdf_file_path(url, output_dir= "data"):
    title, domain = extract_webpage_title_domain(url)

    # Generate the PDF file name based on the extracted domain and title, replacing spaces with underscores
    file_name = f"{domain}_{title.strip().replace(' ', '_')}.pdf"

    # Create the full file path by joining the output directory and the generated file name
    file_path = os.path.join(output_dir, file_name)
    return file_path


# Test the DocumentHandler class
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Data_science"
    # Test create_pdf method
    create_pdf(url)
