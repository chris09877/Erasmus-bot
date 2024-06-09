# import openai, os, requests
#
# openai.api_type = "azure"
# openai.api_version = "2024-02-15-preview"
#
# # Azure OpenAI setup
# openai.api_base = "https://erasmuschatbot.openai.azure.com/" # Add your endpoint here
# openai.api_key = "3dfadd9ef524474fae0e94ae27520a7f" #os.getenv("3dfadd9ef524474fae0e94ae27520a7f") # Add your OpenAI API key here
# deployment_id = "erasmus-bot" # Add your deployment ID here
#
# # Azure AI Search setup
# search_endpoint = "https://chatbot000.search.windows.net" # Add your Azure AI Search endpoint here
# search_key = "cXjB2FfdkQ11FUWQJvyRcDvxfhtRQpMO0acrmKfLCnAzSeDKGsdo" #os.getenv("cXjB2FfdkQ11FUWQJvyRcDvxfhtRQpMO0acrmKfLCnAzSeDKGsdo"); # Add your Azure AI Search admin key here
# search_index_name = "index05" # Add your Azure AI Search index name here
#
# def setup_byod(deployment_id: str) -> None:
#     """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
#
#     :param deployment_id: The deployment ID for the model to use with your own data.
#
#     To remove this configuration, simply set openai.requestssession to None.
#     """
#
#     class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):
#
#         def send(self, request, **kwargs):
#             request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
#             return super().send(request, **kwargs)
#
#     session = requests.Session()
#
#     # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
#     session.mount(
#         prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
#         adapter=BringYourOwnDataAdapter()
#     )
#
#     openai.requestssession = session
#
# setup_byod(deployment_id)
#
#
# message_text = [{"role": "user", "content": "hoeveel studiepunt bevat de opeliding coing?"}]
#
# completion = openai.ChatCompletion.create(
#     messages=message_text,
#     deployment_id=deployment_id,
#     data_sources=[  # camelCase is intentional, as this is the format the API expects
#       {
#   "type": "azure_search",
#   "parameters": {
#     "endpoint": "'$search_endpoint'",
#     "index_name": "index05",
#     "semantic_configuration": "default",
#     "query_type": "simple",
#     "fields_mapping": {},
#     "in_scope": True,
#     "role_information": "You are an AI assistant that helps people find information.",
#     "filter": None,
#     "strictness": 3,
#     "top_n_documents": 5,
#     "authentication": {
#       "type": "api_key",
#       "key": "cXjB2FfdkQ11FUWQJvyRcDvxfhtRQpMO0acrmKfLCnAzSeDKGsdo"
#     },
#     "key": "'$search_key'",
#     "indexName": "'$search_index'"
#   }
# }
#     ],
#     temperature=0,
#     top_p=1,
#     max_tokens=800,
#     stop=None,
#     stream=True
#
# )
# print(completion)
#
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"
openai.api_base = "https://erasmuschatbot.openai.azure.com/"  # Add your endpoint here
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add your OpenAI API key here
deployment_id = "erasmus-bot"  # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://chatbot000.search.windows.net"  # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY")  # Add your Azure AI Search admin key here
search_index_name = "index05"  # Add your Azure AI Search index name here

def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            print(f"Request URL: {request.url}")  # Debug print
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = None

setup_byod(deployment_id)

message_text = [{"role": "user", "content": "hoeveel stuiepunten voor het opleiding coding?"}]

try:
    completion = openai.ChatCompletion.create(
        messages=message_text,
        deployment_id=deployment_id,
        data_sources=[{
            "type": "azure_search",
            "parameters": {
                "endpoint": search_endpoint,
                "index_name": search_index_name,
                "semantic_configuration": "default",
                "query_type": "simple",
                "fields_mapping": {},
                "in_scope": True,
                "role_information": "You are an AI assistant that helps people find information.",
                "filter": None,
                "strictness": 3,
                "top_n_documents": 5,
                "authentication": {
                    "type": "api_key",
                    "key": search_key
                }
            }
        }],
        temperature=0,
        top_p=1,
        max_tokens=800,
        stop=None,
        stream=True
    )
    for complet in completion:
        print(complet)
except openai.error.InvalidRequestError as e:
    print(f"InvalidRequestError: {e}")
except openai.error.OpenAIError as e:
    print(f"OpenAIError: {e}")
except Exception as e:
    print(f"General Error: {e}")

print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print(f"SEARCH_KEY: {os.getenv('SEARCH_KEY')}")
