import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import spacy
from fuzzywuzzy import fuzz
from datetime import datetime
import requests
from io import BytesIO
# nlp = spacy.load("en_core_web_sm")


def education_rank(education):
    education_ranks = {
        "High School Degree": 1,
        "Associate's Degree": 2,
        "Bachelor's Degree": 3,
        "Master's Degree": 4,
        "Ph.D. or Doctorate": 5
    }
    return education_ranks.get(education, 0)


def extract_text_from_pdf(pdf_url):
    # Download the PDF from the URL
    response = requests.get(pdf_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Open the PDF using pdfplumber
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            first_page = pdf.pages[0]
            resume_text = first_page.extract_text()
        return resume_text
    else:
        # If the request was not successful, print an error message
        print(f"Failed to download PDF from {pdf_url}. Status code: {response.status_code}")
        return None


def extract_education(input_text):
    education_section_match = re.search(r'\bEDUCATION\b', input_text, re.IGNORECASE)
    if not education_section_match:
        return None

    # Extract the content after the "EDUCATION" section
    education_content = input_text[education_section_match.end():]

    # Use regular expression to find the most recent education entry
    education_entries = re.findall(r'\b\d{4}\b.*?(?=\b\d{4}\b|$)', education_content, re.DOTALL)

    if education_entries:
        most_recent_entry = max(education_entries)
        return most_recent_entry.strip()
    else:
        return None


def extract_education_level(education_entry):
    if "Masters" in education_entry:
        return "Masters"
    elif "Bachelors" in education_entry:
        return "Bachelors"
    elif "PhD" in education_entry:
        return "PhD"
    else:
        return None


def education_rank(education):
    education_ranks = {
        "High School Degree": 1,
        "Associate's Degree": 2,
        "Bachelor's Degree": 3,
        "Master's Degree": 4,
        "Ph.D. or Doctorate": 5
    }

    # Convert input to lowercase for case-insensitive matching
    lower_education = education.lower()

    # Find the best match using fuzzy matching
    best_match = None
    best_score = 0
    for key in education_ranks:
        score = fuzz.partial_ratio(lower_education, key.lower())
        if score > best_score:
            best_score = score
            best_match = key

    if best_match is not None:
        return education_ranks[best_match]
    else:
        return 0


def extract_experience(resume_text):
    # Define the list of keywords to look for
    keywords = ['experience', 'employment', 'job']
    section_pattern = r'\b(?:experience|employment|projects|certifications|education|awards|skills)\b'
    section_headers = re.findall(section_pattern, resume_text, flags=re.IGNORECASE)
    for header in keywords:
        section_pattern = r'(?i)\b' + header + r'\b([\s\S]*?)(?=\b(?:' + '|'.join(section_headers) + r')\b|\Z)'
        section_content = re.search(section_pattern, resume_text)
        if section_content:
            return section_content.group(1).strip()
    return None


def extract_months_experience(experience_section):
    # Regular expression pattern to match lines with a date
    date_pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{4}\b'
    # Find lines containing dates within the experience section
    experience_lines = re.findall(rf'.*{date_pattern}.*', experience_section)
    total_exp = 0
    for experience in experience_lines:
        dates = re.findall(
            r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{4}\b',
            experience)
        print(dates)
        if len(dates) == 2:
            start_date = datetime.strptime(dates[0], '%b %Y')
            end_date = datetime.strptime(dates[1], '%b %Y')
            duration_in_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
            total_exp += duration_in_months
    return total_exp


def extract_skills(input_text, expected_skills):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(input_text)

    # Remove stop words and non-alphabetic tokens
    filtered_tokens = [w for w in word_tokens if w.lower() not in stop_words and w.isalpha()]

    # Generate bigrams and trigrams
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    found_skills = set()

    for token in filtered_tokens:
        if token.lower() in [skill.lower() for skill in expected_skills]:
            found_skills.add(token)

    # Convert ngram and expected_skills to lowercase before matching
    for ngram in bigrams_trigrams:
        if ngram.lower() in [skill.lower() for skill in expected_skills]:
            found_skills.add(ngram)

    return found_skills


def count_keywords(resume_text, keywords):
    keyword_count = {keyword: 0 for keyword in keywords}

    for keyword in keywords:
        keyword_count[keyword] = resume_text.lower().count(keyword.lower())

    return keyword_count


def resume_screening(file):
    # pdf_file_name = get_object_or_404(IndeedApplicants, id=user_id)
    # applicants = IndeedApplicants.objects.filter(job_id=job_id)
    # percent_match_applicants = []
    # for applicant in applicants:
    record = {}
    # pdf_file_path = os.path.join('./indeed/resumes/', applicant.resume)
    # pdf_file_path = os.path.join('./indeed/resumes/jd.pdf')
    # print(pdf_file_path)

    resume_text = extract_text_from_pdf(file)
    # print(resume_text)
    keyword_matches = ["Python", "Java", "HTML", "CSS", "JavaScript", "AWS", "Springboot", "PHP"]
    education = extract_education(resume_text)
    print(education)
    if education:
        education_level = extract_education_level(education)
        print(education_level)
    experience_section = extract_experience(resume_text)
    if experience_section:
    # print(experience_section)
        experience_months_duration = extract_months_experience(experience_section)
        print("Total_months worked:", experience_months_duration)
    resume_skills = extract_skills(resume_text, keyword_matches)
    print(resume_skills)
    matched_keywords = count_keywords(resume_text, keyword_matches)
    print(matched_keywords)
    keywords_match_entire_resume = 0
    for keyword in matched_keywords.keys():
        if matched_keywords[keyword] > 0:
            keywords_match_entire_resume += 1
    # # resume_data = {
    # #     "education": "Master's Degree",
    # #     "experience": experience_months_duration,  # 6 months of experience
    # #     "skills": resume_skills
    # # }
    # basic_requirements = {
    #     "education": "Bachelor's Degree",
    #     "experience": 0
    # }
    # education_match = education_rank(education_level) >= education_rank(basic_requirements["education"])
    # experience_match = experience_months_duration >= basic_requirements["experience"]
    # if keywords_match_entire_resume < len(resume_skills):
    #     keyword_match_count = len(resume_skills)
    # else:
    #     keyword_match_count = keywords_match_entire_resume
    #
    # # total_basic_requirements = len(basic_requirements)
    # # total_keyword_matches = len(keyword_matches)
    # # total_match_count = education_match + experience_match + keyword_match_count
    # # percentage_match = (total_match_count / (total_basic_requirements + total_keyword_matches)) * 100
    # # record['fullName'] = applicant.fullName
    # # record['match'] = f"{percentage_match:.2f}%"
    # # percent_match_applicants.append(record)
    # # return percentage_match
    # # Print the match percentage
    return resume_skills, resume_text
