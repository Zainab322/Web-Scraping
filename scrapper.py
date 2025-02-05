import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
TIMEOUT = 30
THREAD_COUNT = 10
BASE_URL = "https://papers.nips.cc"

def fetch_document(url):
    """Fetch and parse the HTML document from the given URL."""
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def download_pdf(file_url, save_path):
    """Download a PDF file from the given URL and save it to the specified path."""
    try:
        response = requests.get(file_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"PDF Downloaded: {save_path}")
    except requests.RequestException as e:
        print(f"Failed to download: {file_url} - {e}")

def scrape_paper(paper, base_url, text_writer, download_folder):
    """Scrape paper details and save them to a text file. Download the PDF if available."""
    try:
        paper_url = base_url + paper["href"]
        paper_doc = fetch_document(paper_url)
        if not paper_doc:
            return

        title_element = paper_doc.select_one("meta[name='citation_title']")
        title = title_element["content"].strip() if title_element else "No title"

        author_elements = paper_doc.select("meta[name='citation_author']")
        authors = ", ".join(author["content"] for author in author_elements) if author_elements else "Unknown Authors"

        abstract_element = paper_doc.select_one("p")
        abstract = abstract_element.text.strip() if abstract_element else "No abstract available"

        pdf_meta = paper_doc.select_one("meta[name='citation_pdf_url']")
        pdf_url = pdf_meta["content"] if pdf_meta else "No PDF available"

        paper_data = (
            f"Title: {title}\n"
            f"Authors: {authors}\n"
            f"Abstract: {abstract}\n"
            f"URL: {paper_url}\n"
            f"PDF: {pdf_url}\n"
            "--------------------------------------------------\n"
        )

        with text_writer_lock:
            text_writer.write(paper_data)
            text_writer.flush()

        if pdf_url != "No PDF available":
            pdf_filename = os.path.join(download_folder, title.replace("/", "_").replace(":", "_") + ".pdf")
            download_pdf(pdf_url, pdf_filename)
    except Exception as e:
        print(f"Error scraping paper: {paper['href']} - {e}")

def main():
    """Main function to scrape NeurIPS papers."""
    main_page_url = BASE_URL + "/"
    main_doc = fetch_document(main_page_url)
    if not main_doc:
        return

    year_links = main_doc.select("a[href^='/paper_files/paper/']")
    years = [BASE_URL + year["href"] for year in year_links]

    os.makedirs("NeurIPS_Papers", exist_ok=True)

    with open("NeurIPS_Papers.txt", "w", encoding="utf-8") as text_writer:
        global text_writer_lock
        text_writer_lock = type('Lock', (), {'acquire': lambda: None, 'release': lambda: None})()
        if THREAD_COUNT > 1:
            from threading import Lock
            text_writer_lock = Lock()

        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            futures = []
            for year_url in years:
                year_doc = fetch_document(year_url)
                if not year_doc:
                    continue

                paper_links = year_doc.select("a[href*='-Abstract-Conference.html']")
                year = "".join(filter(str.isdigit, year_url))
                year_folder = os.path.join("NeurIPS_Papers", year)
                os.makedirs(year_folder, exist_ok=True)

                for paper in paper_links:
                    futures.append(executor.submit(scrape_paper, paper, BASE_URL, text_writer, year_folder))

            for future in as_completed(futures):
                future.result()

    print("\nData saved to NeurIPS_Papers.txt")

if __name__ == "__main__":
    main()