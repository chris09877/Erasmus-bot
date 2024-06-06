import spacy
import os
import re
import json

nlp = spacy.load('nl_core_news_sm')

def extract_sentences(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

def generate_doc_name(filename):
    if filename.startswith("opleidingen_") and filename.endswith(".html.txt"):
        name = filename.split("opleidingen_")[1].split(".html.txt")[0]
        name = ''.join([i for i in name if not i.isdigit()])
        return name
    else:
        return filename

def process_files_and_extract_sentences(directory):
    file_sentences = {}

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            sentences = extract_sentences(text)
            file_sentences[filename] = sentences

            # Generate JSON file for each document
            doc_name = generate_doc_name(filename)
            json_data = {'name': doc_name, 'description': ' '.join(sentences)}

            json_output_path = os.path.join('./JSON', f'{os.path.splitext(filename)[0]}.json')
            with open(json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    return file_sentences

directory_path = './preprocessed-files/'

os.makedirs('./JSON', exist_ok=True)

file_sentences = process_files_and_extract_sentences(directory_path)
