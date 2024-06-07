# import os
# import json
#
# def add_timestamp_to_files(directory):
#     # Iterate through each file in the directory
#     for filename in os.listdir(directory):
#         if filename.endswith('.json'):
#             file_path = os.path.join(directory, filename)
#             # Read the JSON file
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#             # Add the timestamp field
#             data['@timestamp'] = '2024-06-07T12:00:00Z'
#             # Write the modified JSON back to the file
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 json.dump(data, file, indent=4)  # Adjust indentation as needed
#
# # Specify the directory containing the JSON files
# directory_path = './JSON/'
#
# # Add timestamp to files in the directory
# add_timestamp_to_files(directory_path)
#
# print('Timestamp added to JSON files.')


import os
import json
from elasticsearch import Elasticsearch, helpers

# Connect to Elasticsearch using API key
api_key = "TndvZTg0OEIxbDk4OEwtN3VEWTc6d3lIYjRmT21UN2FTNmxqQzlEb0FuUQ=="
client = Elasticsearch(
    "https://localhost:9201",
    api_key=api_key
)

# Function to create an index
def create_index(index_name, index_mapping):
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=index_mapping)
        print(f'Index {index_name} created')
    else:
        print(f'Index {index_name} already exists')

# Function to generate documents for bulk indexing
def generate_documents(index_name, json_directory):
    for filename in os.listdir(json_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(json_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                document = json.load(file)
                yield {
                    "_index": index_name,
                    "_source": document
                }

# Define the index name and JSON directory
index_name = 'courses'
json_directory = './JSON/'

# Define the index mapping
index_mapping = {
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "description": {
                "type": "text"
            }
        }
    }
}

# Create the index
create_index(index_name, index_mapping)

# Generate documents for bulk indexing
documents = generate_documents(index_name, json_directory)

# Bulk index the JSON data
helpers.bulk(client, documents)

print('Indexing completed')
