import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
from googlesearch import search
from urllib.parse import urlparse
import os


async def fetch(url, session, retries=3, delay=1):
    if retries == 0:
        print("Maximum retries exceeded. Failed to fetch URL.")
        return
    try:
        async with session.get(url) as response:
            return await response.text(encoding='latin')
    except aiohttp.ClientResponseError as e:
        if e.status == 429:  # HTTP 429: Too Many Requests
            print(f"Too many requests. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
            return fetch(url, session, retries=retries - 1, delay=delay * 2)
        print(f"Error fetching URL: {e}")


async def scrape_websites(topic, num_results_per_link=10):
    outputs = await scrape_google(topic, num_results_per_link)
    # Select random links based on the user's input
    selected_links = random.sample(outputs, min(num_results_per_link, len(outputs)))
    # return the list of strings as a single string
    # return "\n".join(selected_links)
    return list(selected_links)


async def scrape_google(topic, num_results=15) -> list[str]:
    # Limit search results to 15 if num_results exceeds 15
    num_results = min(num_results, 15)
    # Asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Perform Google search
        search_results = search(topic, num_results=3 * num_results)
        search_results = remove_duplicate_results(search_results)
        # Shuffle search results order
        random.shuffle(search_results)
        outlines = []
        i = 0
        # Keep scraping url's until you collect wanted num_results, or till you have tried all search results
        while len(outlines) < num_results and i < len(search_results):
            result = await scrape_url(search_results[i], session)
            if result:
                outlines.append(result)
            i += 1
    return outlines


async def scrape_url(url, session) -> str:
    try:
        # Fetch HTML content asynchronously
        html_content = await fetch(url, session)
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract outlines from parsed HTML
        outlines = extract_outlines(soup)

        # If outlines exist, accumulate them with website info
        if outlines:
            return get_website_info_str(url, outlines)
        return ''

    except Exception as e:
        print(f"Error '{e}' while processing URL:{url}")
        return ''


# Minimum length threshold for relevant outlines
MIN_LENGTH_THRESHOLD = 20
is_irrelevant_outline = lambda outline: len(outline) < MIN_LENGTH_THRESHOLD
extract_main_domain_from_url = lambda url: urlparse(url).netloc.split('www.')[-1].split('/')[0]
extract_website_name_from_url = lambda url: urlparse(url).netloc
extract_title_from_url = lambda url: os.path.basename(urlparse(url).path)


def remove_duplicate_results(search_result) -> list:
    unique_domains = set()
    unique_websites = []
    for url in search_result:
        domain = extract_main_domain_from_url(url)
        if domain not in unique_domains:
            unique_domains.add(domain)
            unique_websites.append(url)
    return unique_websites


def get_website_info_str(url, outlines) -> str:
    website_name = extract_website_name_from_url(url)
    info = f"Website: {website_name}\nURL: {url}\nOutlines:\n." + '\n.'.join(outlines)
    return info


def filter_outlines(outlines) -> list[str]:
    return [outline for outline in set(outlines) if not is_irrelevant_outline(outline)]


def extract_outlines(soup) -> list[str]:
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    outlines = [heading.text.strip() for heading in headings]
    if len(outlines) >= 3:
        return filter_outlines(outlines)
