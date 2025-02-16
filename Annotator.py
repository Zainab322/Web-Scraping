import google.generativeai as genai
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

CATEGORIES = ["Deep Learning", "NLP", "Computer Vision", "Reinforcement Learning", "Optimization"]

def classify_paper_gemini(title, abstract):
    prompt = f"""
    Classify the following research paper into one of these categories: {CATEGORIES}.
    If the category is unclear, pick the closest match.

    Title: {title}
    Abstract: {abstract}

    Just return the category name.
    """
    model = genai.GenerativeModel("gemini-pro")
    max_retries = 5
    wait_time = 5  
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):  
                print(f"Rate limit reached. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2  
            else:
                print(f"Error: {e}")
                return "Uncategorized"
    
    return "Uncategorized"  

df = pd.read_csv("neurips_papers.csv")

for index, row in df.iterrows():
    print(f"Processing {index + 1}/{len(df)}: {row['Title'][:50]}...")
    df.at[index, "Category"] = classify_paper_gemini(row["Title"], row["Abstract"])
    time.sleep(1)  

df.to_csv("neurips_papers_annotated.csv", index=False)
print("✅ Annotation complete! Saved as 'neurips_papers_annotated.csv'")