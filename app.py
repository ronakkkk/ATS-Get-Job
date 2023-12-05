import pandas as pd
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def read_job_dataset(file_path):
    return pd.read_csv(file_path)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def preprocess_job_dataset(df):
    df["description"] = df["description"].astype(str).apply(lambda x: x.lower())
    df["combined_text"] = df["location"] + ' ' + df["title"] + ' ' + df["company"] + ' ' + df["description"]
    df["combined_text"] = df["combined_text"].fillna('')
    return df

def calculate_cosine_similarity(train_df, resume_text):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(train_df["combined_text"])
    
    resume_tfidf_vector = tfidf_vectorizer.transform([resume_text])
    
    cosine_similarities = linear_kernel(resume_tfidf_vector, tfidf_matrix).flatten()
    train_df["cosine_similarity"] = cosine_similarities
    return train_df

def get_top_matching_jobs(train_df, n=10):
    return train_df.nlargest(n, "cosine_similarity")[["location", "title", "company", "description", "cosine_similarity"]]

# Example usage
train_df = read_job_dataset("output.csv")
train_df = preprocess_job_dataset(train_df)

resume_text = extract_text_from_pdf('JinayPanchalResumeH.pdf')

train_df = calculate_cosine_similarity(train_df, resume_text)

top_jobs = get_top_matching_jobs(train_df)
# display(top_jobs)
print(top_jobs)
# import sys

# print("Python Version:", sys.version)

