import csv
import re
import spacy
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def save_to_file(text):
    with open('pdf_as_text.txt', 'w') as f:
        f.write(text)


# 1. Convert PDF to Text using pdfminer
# This will make it easier to extract relevant data based on keywords
def pdf_to_text(pdf_file_path):
    output_string = StringIO()
    with open(pdf_file_path, 'rb') as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise ValueError("PDF file cannot be extracted")
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        text = output_string.getvalue()
        return text


# 2. Clean the text
# Remove unwanted characters, special symbols, and unnecessary whitespaces using regex
def clean_text(text):
    # Remove unwanted characters and replace them with space
    text = re.sub(r'\n', ' ', text)  # newline characters
    text = re.sub(r'\r', ' ', text)  # carriage return characters
    text = re.sub(r'\t', ' ', text)  # tab characters
    text = re.sub(r'\x0c', ' ', text)  # form feed characters

    # Remove special symbols
    text = re.sub(r'\([^)]*\)', '', text)  # text inside parentheses
    text = re.sub(r'[^a-zA-Z0-9\s\.\-]', '', text)  # non-alphanumeric characters (except for ' ', '.', and '‐')

    # Remove unnecessary whitespaces
    text = re.sub(r'\s+', ' ', text)  # replace multiple spaces with a single space
    text = re.sub(r'^\s+|\s+?$', '', text)  # remove leading and trailing spaces

    return text


# 3. Tokenize the text
# Split the text into individual words with spaCy
def tokenize_text(text):
    nlp = spacy.load("sv_core_news_sm")  # load Swedish language model
    res = nlp(text)  # use model to tokenize text
    return res


# 4. Remove stopwords
# Stopwords like 'a', 'an, 'the' are removed with a stopword list
def remove_stopwords(text):
    with open('stoppord.csv', "r") as csvfile:  # load stopwords
        stopwords_reader = csv.reader(csvfile)
        stopwords = [row[0] for row in stopwords_reader]

    # FIXME skriv om så den hanterar annat än str
    filtered_words = [word for word in text if word.lower() not in stopwords]  # remove stopwords
    filtered_text = " ".join(filtered_words) # join filtered words

    return filtered_text


# 5. Lemmatize text using spaCy
# Reduce words to their dictionary form
def lemmatize_text(text):
    lemmas = [token.lemma_ for token in text]
    return lemmas


# 6. Identify relevant keywords
# Use a library (Gensim, TextBlob) to identify relevant keywords from the preprocessed text


pdf_text = pdf_to_text('ica2021.pdf')
cleaned_text = clean_text(pdf_text)
tokenized_text = tokenize_text(cleaned_text)
stopword_free_text = remove_stopwords(tokenized_text)
lemmatized_text = lemmatize_text(stopword_free_text)




