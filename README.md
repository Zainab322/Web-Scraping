# Web-Scraping

This project provides two scripts to scrape papers from the NeurIPS conference website, save paper details to a text file, and download available PDFs. It includes both a Java implementation and a Python implementation.

## Prerequisites

### Java Implementation:
- **JDK 8 or later** is required for running the Java program.
- **Required Libraries:**
  - [JSoup](https://jsoup.org/) for HTML parsing.
- **IDE or command-line tools** (like Terminal or Command Prompt) for running Java applications.

### Python Implementation:
- **Python 3.6 or later** is required for running the Python program.
- **Required Libraries**:
  - `requests` (for making HTTP requests).
  - `beautifulsoup4` (for HTML parsing).
  
To install the required Python libraries, run:

```bash
pip install requests beautifulsoup4


### Setup and Running

- **Java Script**
Clone this repository or download the NeurIPSScraper.java file.

- **ICompile the Java file: Open your terminal or command prompt and navigate to the directory where the .java file is located. Run the following command to compile the Java file:

javac NeurIPSScraper.java

### Program Details:
- **The Java script will fetch the NeurIPS main page and scrape links to papers by year.
- **For each year, it will scrape paper titles, authors, abstracts, and any available PDF links.
- **It will save paper details in a text file named NeurIPS_Papers.txt.
- **PDFs will be downloaded into the directory D:/MyPapers/ (this path can be modified in the script).

### Important Variables to Modify:
Change the baseDownloadPath variable to specify a different directory for downloading PDFs (default is D:/MyPapers/).

- **Python Script**
Clone this repository or download the neurips_scraper.py file.

- **Run the Python script: After installing the libraries, run the Python script by using the following command:
python neurips_scraper.py

###Program Details:
- **The Python script scrapes the NeurIPS website for conference papers, year by year.
- **It saves the title, authors, abstract, and PDF link for each paper in a text file called NeurIPS_Papers.txt.
- **It will download any available PDFs to a directory called NeurIPS_Papers.
