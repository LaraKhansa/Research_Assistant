import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
from googlesearch import search
from urllib.parse import urlparse

async def fetch(url, session, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientResponseError as e:
            if e.status == 429:  # HTTP 429: Too Many Requests
                delay = 2 ** attempt  # Exponential backoff
                print(f"Too many requests. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"Error fetching URL: {e}")
                return None
    print("Maximum retries exceeded. Failed to fetch URL.")
    return None



async def scrape_google(topic, num_results=20) -> str:
    # Initialize a set to store unique website URLs
    unique_websites = set()
    # Initialize an empty string to accumulate outlines
    outlines_str = ""

    # Asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Perform Google search
        search_results = search(topic, num=num_results, stop=num_results)
        # Limit search results to 15 if num_results exceeds 15
        search_results = random.sample(list(search_results), min(num_results, 15))

        # Iterate through search results
        for url in search_results:
            # Exit loop if desired number of websites are found
            if len(unique_websites) >= num_results:
                break
            # Scrape outlines from URL and accumulate them
            outlines_str += await scrape_url(url, session, unique_websites)

    # Return accumulated outlines string
    return outlines_str
    
async def scrape_url(url, session, unique_websites) -> str:
   try:
        # Extract main domain from the URL
        domain = urlparse(url).netloc.split('www.')[-1].split('/')[0]

        # Check if the domain has already been processed
        if domain in unique_websites:
            return ""

        # Fetch HTML content asynchronously
        html_content = await fetch(url, session)
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract outlines from parsed HTML
        outlines = extract_outlines(soup)

        # Skip URLs with less than three outlines
        if len(outlines) < 3:
            return ""

        # Filter irrelevant outlines
        outlines = filter_outlines(outlines)
        outlines_str = ""

        # If outlines exist, accumulate them with website info
        if outlines:
            website_name = urlparse(url).netloc  # Extract website name from URL
            outlines_str += f"Website: {website_name}\n"
            outlines_str += f"URL: {url}\n"
            outlines_str += "Outlines:\n"
            for outline in outlines:
                outlines_str += ". "+ outline + "\n"
            outlines_str += "----------------------------------------------------------------------------------------------\n"
            # Add the domain to the set of unique websites
            unique_websites.add(domain)

        return outlines_str
   except Exception as e:
      # Handle exceptions and return empty string
      print("Error processing URL:", url)
      print(e)
      return ""


def is_irrelevant_outline(outline):
    # Minimum length threshold for relevant outlines
    min_length_threshold = 20
    return len(outline) < min_length_threshold

def filter_outlines(outlines):
    filtered_outlines = [outline for outline in outlines if not is_irrelevant_outline(outline)]
    filtered_outlines = list(set(filtered_outlines))
    return filtered_outlines

def extract_outlines(soup):
    outlines = []
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    for heading in headings:
        outlines.append(heading.text.strip())
    return outlines

