# import spacy
# import re
# import os
# import csv
#
# # Load Dutch spaCy model
# nlp = spacy.load('nl_core_news_sm')
#
#
# # Define extraction functions
# def extract_courses(text, file_name):
#     courses = {}
#
#     # Extract the relevant part of the file name using split
#     if file_name.startswith("opleidingen_") and file_name.endswith(".html.txt"):
#         file_name_parts = file_name.split("opleidingen_")[1].split(".html.txt")[0]
#         courses['name'] = file_name_parts
#     else:
#         courses['name'] = file_name
#
#     # Extract credit (studiepunten)
#     credit_match = re.search(r'studiepunten:?\s*(\d+)', text, re.IGNORECASE)
#     courses['credit'] = credit_match.group(1) if credit_match else None
#
#     # Extract vakken and credit per vak (ects)
#     vakken = []
#     vakken_matches = re.findall(r'vak:?\s*([\w\s]+),?\s*ects:?\s*(\d+)', text, re.IGNORECASE)
#     for vak, ects in vakken_matches:
#         vakken.append({'vak': vak.strip(), 'ects': ects.strip()})
#     courses['vakken'] = vakken
#
#     # Extract duur
#     duur_match = re.search(r'jaar:?\s*([\w\s]+)', text, re.IGNORECASE)
#     courses['duur'] = duur_match.group(1).strip() if duur_match else None
#     duur_match = re.search(r'jaren:?\s*([\w\s]+)', text, re.IGNORECASE)
#     courses['duur'] = duur_match.group(1).strip() if duur_match else None
#
#     # Extract campus
#     campus_match = re.search(r'campus:?\s*([\w\s]+)', text, re.IGNORECASE)
#     courses['campus'] = campus_match.group(1).strip() if campus_match else None
#
#     # Extract type (graduatbachelor postgraduat)
#     # type_match = re.search(r'(graduat|bachelor|postgraduat|opleiding)', file_name, re.IGNORECASE)
#     # courses['type'] = type_match.group(1).strip() if type_match else None
#
#     # Extract bachelor na bachelor
#     bnab_match = re.search(r'bachelor na bachelor:?\s*([\w\s]+)', text, re.IGNORECASE)
#     courses['bachelor_na_bachelor'] = bnab_match.group(1).strip() if bnab_match else None
#
#     # Extract master na master
#     mnam_match = re.search(r'master na master:?\s*([\w\s]+)', text, re.IGNORECASE)
#     courses['master_na_master'] = mnam_match.group(1).strip() if mnam_match else None
#
#     # Extract start date
#     start_match = re.search(r'start:?\s*([\w\s]+)', text, re.IGNORECASE)
#     courses['start_date'] = start_match.group(1).strip() if start_match else None
#
#     return courses
#
#
# def extract_admissions(text):
#     admissions = {}
#
#     # Extract voorwaarden
#     voorwaarden_match = re.search(r'voorwaarden:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     admissions['voorwaarden'] = voorwaarden_match.group(1).strip() if voorwaarden_match else None
#
#     # Extract deadlines
#     deadlines_match = re.search(r'deadlines:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     admissions['deadlines'] = deadlines_match.group(1).strip() if deadlines_match else None
#
#     # Extract plaats
#     plaats_match = re.search(r'plaats:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     admissions['plaats'] = plaats_match.group(1).strip() if plaats_match else None
#
#     return admissions
#
#
# def extract_faculty(text):
#     faculty = {}
#
#     # Extract name
#     name_match = re.search(r'naam:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     faculty['name'] = name_match.group(1).strip() if name_match else None
#
#     # Extract address
#     address_match = re.search(r'adres:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     faculty['address'] = address_match.group(1).strip() if address_match else None
#
#     # Extract courses
#     courses_match = re.findall(r'cursus:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     faculty['courses'] = [course.strip() for course in courses_match]
#
#     # Extract teachers
#     teachers_match = re.findall(r'docent:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     faculty['teachers'] = [teacher.strip() for teacher in teachers_match]
#
#     return faculty
#
#
# def extract_events(text):
#     events = {}
#
#     # Extract description
#     description_match = re.search(r'beschrijving:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     events['description'] = description_match.group(1).strip() if description_match else None
#
#     # Extract start and end date
#     start_end_date_match = re.search(r'datum:?\s*van\s*([\w\s,]+)\s*tot\s*([\w\s,]+)', text, re.IGNORECASE)
#     if start_end_date_match:
#         events['start_date'] = start_end_date_match.group(1).strip()
#         events['end_date'] = start_end_date_match.group(2).strip()
#
#     # Extract purpose
#     purpose_match = re.search(r'doel:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     events['purpose'] = purpose_match.group(1).strip() if purpose_match else None
#
#     # Extract address
#     address_match = re.search(r'adres:?\s*([\w\s,]+)', text, re.IGNORECASE)
#     events['address'] = address_match.group(1).strip() if address_match else None
#
#     return events
#
#
# # Function to write to a CSV file (appending if it already exists)
# def write_to_csv(data, output_csv):
#     file_exists = os.path.isfile(output_csv)
#     keys = data[0].keys()
#
#     with open(output_csv, 'a', newline='', encoding='utf-8') as output_file:
#         dict_writer = csv.DictWriter(output_file, fieldnames=keys)
#         if not file_exists:
#             dict_writer.writeheader()
#         dict_writer.writerows(data)
#
#
# # Function to process all text files in a directory and save to separate CSV files
# def process_files_and_save_to_csv(directory):
#     all_courses = []
#     all_admissions = []
#     all_faculty = []
#     all_events = []
#
#     for filename in os.listdir(directory):
#         if filename.endswith('.txt'):
#             with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
#                 text = file.read()
#
#                 # Extract information
#                 courses = extract_courses(text, filename)
#                 admissions = extract_admissions(text)
#                 faculty = extract_faculty(text)
#                 events = extract_events(text)
#
#                 all_courses.append(courses)
#                 all_admissions.append(admissions)
#                 all_faculty.append(faculty)
#                 all_events.append(events)
#
#     # Write the extracted information to separate CSV files
#     if all_courses:
#         write_to_csv(all_courses, './CSV/courses.csv')
#     if all_admissions:
#         write_to_csv(all_admissions, './CSV/admissions.csv')
#     if all_faculty:
#         write_to_csv(all_faculty, './CSV/faculty.csv')
#     if all_events:
#         write_to_csv(all_events, './CSV/events.csv')
#
#
# # Directory text files
# directory_path = './html_to_txt/'
#
# # Process the files and save the extracted information to separate CSV files
# process_files_and_save_to_csv(directory_path)
import spacy
import os

# Load Dutch spaCy model
nlp = spacy.load('nl_core_news_sm')

def preprocess_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def process_files_and_save_to_txt(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)

            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()

            preprocessed_text = preprocess_text(text)

            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(preprocessed_text)

input_directory = './html_to_txt/'
output_directory = './preprocessed-files/'

process_files_and_save_to_txt(input_directory, output_directory)
