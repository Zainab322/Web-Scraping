**WEB SCRAPING AND DATA ANNOTATION WITH LLMs**

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




# Research Paper Annotation using LLMs

## Overview
This project automates the annotation of research papers scraped from NeurIPS (https://papers.nips.cc) using Large Language Models (LLMs). The script assigns a predefined category to each paper based on its title and abstract.

## Features
- Classifies research papers into five categories:
  - Deep Learning
  - NLP
  - Computer Vision
  - Reinforcement Learning
  - Optimization
- Uses Google Gemini API for text classification.
- Implements retry logic with exponential backoff for handling API rate limits.
- Saves the annotated dataset in a structured CSV file.

## Requirements
Python 3.7+
Required libraries:
- google-generativeai
- pandas

## Setup
# Install required libraries
pip install google-generativeai pandas

## API Configuration
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY_HERE")
```

## Usage
# Ensure that 'neurips_papers.csv' exists in the project directory
python annotate_papers.py


## Script Explanation
```python
# Load Dataset
import pandas as pd
df = pd.read_csv("neurips_papers.csv")

# Classify Papers using Google Gemini API
def classify_paper_gemini(title, abstract):
    prompt = f"""
    Classify the following research paper into one of these categories: {CATEGORIES}.
    If the category is unclear, pick the closest match.
    
    Title: {title}
    Abstract: {abstract}
    
    Just return the category name.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()
```

## License
This project is open-source and available for educational and research purposes.

