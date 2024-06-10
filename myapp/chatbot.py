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
search_index_name = "index07"  # Add your Azure AI Search index name here

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

def get_chatbot_response(user_message):
    message_text = [{"role": "user", "content": user_message}]

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

        response_text = ""
        for complet in completion:
            if 'choices' in complet and len(complet['choices']) > 0:
                if 'delta' in complet['choices'][0] and 'content' in complet['choices'][0]['delta']:
                    response_text += complet['choices'][0]['delta']['content']

        return response_text

    except openai.error.InvalidRequestError as e:
        return f"InvalidRequestError: {e}"
    except openai.error.OpenAIError as e:
        return f"OpenAIError: {e}"
    except Exception as e:
        return f"General Error: {e}"

# Example usage
if __name__ == "__main__":
    user_message = "hoeveel studiepunten bevat de opleiding coding?"
    response = get_chatbot_response(user_message)
    print(f"Response: {response}")
