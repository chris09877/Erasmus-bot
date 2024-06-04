#import spacy
#import os
#from collections import defaultdict

# Load Dutch spaCy model
#nlp = spacy.load('nl_core_news_sm')

#
# def extract_named_entities(text):
#     doc = nlp(text)
#     return [ent.text for ent in doc.ents]
#
#
# # Function to process files and extract named entities
# def process_files_and_extract_entities(directory):
#     file_entities = {}
#     all_entities = defaultdict(int)
#
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory, filename)
#
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 text = file.read()
#
#             named_entities = extract_named_entities(text)
#             file_entities[filename] = named_entities
#
#             for entity in named_entities:
#                 all_entities[entity] += 1
#
#     return file_entities, all_entities
#
#
# # Function to find common entities in all files
# def find_common_entities(file_entities):
#     if not file_entities:
#         return []
#
#     common_entities = set(file_entities[next(iter(file_entities))])
#
#     for entities in file_entities.values():
#         common_entities.intersection_update(entities)
#
#     return list(common_entities)
#
#
# # Directory containing preprocessed text files
# directory_path = './preprocessed-files/'
#
# # Extract named entities from all files
# file_entities, all_entities = process_files_and_extract_entities(directory_path)
#
# # Find common entities across all files
# common_entities = find_common_entities(file_entities)
#
# # Print the results
# print("Most common named entities (present in all files):")
# print(common_entities)
# print()
#
# for filename, entities in file_entities.items():
#     print(f'"{filename}" contains these named entities:')
#     print(entities)
#     print()
#
# def extract_sentences(text):
#     doc = nlp(text)
#     return [sent.text for sent in doc.sents]
#
#
# # Function to process files and extract sentences
# def process_files_and_extract_sentences(directory):
#     file_sentences = {}
#     all_sentences = defaultdict(int)
#
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory, filename)
#
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 text = file.read()
#
#             sentences = extract_sentences(text)
#             file_sentences[filename] = sentences
#
#             for sentence in sentences:
#                 all_sentences[sentence] += 1
#
#     return file_sentences, all_sentences
#
#
# # Function to find common sentences in all files
# def find_common_sentences(file_sentences):
#     if not file_sentences:
#         return []
#
#     common_sentences = set(file_sentences[next(iter(file_sentences))])
#
#     for sentences in file_sentences.values():
#         common_sentences.intersection_update(sentences)
#
#     return list(common_sentences)
#
#
# # Directory containing preprocessed text files
# directory_path = './preprocessed-files/'
#
# # Extract sentences from all files
# file_sentences, all_sentences = process_files_and_extract_sentences(directory_path)
#
# # Find common sentences across all files
# common_sentences = find_common_sentences(file_sentences)
#
# # Print the results
# print("Most common sentences (present in all files):")
# print(common_sentences)
# print()
#
# for filename, sentences in file_sentences.items():
#     print(f'"{filename}" contains these sentences:')
#     for sentence in sentences:
#         print(f'- {sentence}')
#
#     print()



import spacy
import os
import re
import json
from collections import defaultdict

# Load Dutch spaCy model
nlp = spacy.load('nl_core_news_sm')

# Function to extract sentences from text
def extract_sentences(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

# Function to extract named entities from a sentence
def extract_named_entities(sentence):
    doc = nlp(sentence)
    entities = {}
    for ent in doc.ents:
        entities[ent.text] = ent.label_
    return entities

# Function to generate a name for the document based on its filename
def generate_doc_name(filename):
    if filename.startswith("opleidingen_") and filename.endswith(".html.txt"):
        name = filename.split("opleidingen_")[1].split(".html.txt")[0]
        name = ''.join([i for i in name if not i.isdigit()])
        return name
    else:
        return filename

# Function to process files and extract sentences
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
            json_data = {'name': doc_name, 'sentences': {}}
            for sentence in sentences:
                entities = extract_named_entities(sentence)
                json_data['sentences'][sentence] = entities

            json_output_path = os.path.join('./JSON', f'{os.path.splitext(filename)[0]}.json')
            with open(json_output_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    return file_sentences

# Directory containing preprocessed text files
directory_path = './preprocessed-files/'

# Create directory for JSON files if it doesn't exist
os.makedirs('./JSON', exist_ok=True)

# Extract sentences from all files
file_sentences = process_files_and_extract_sentences(directory_path)
