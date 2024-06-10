import os
import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = 'https://github.com/WolfNuyts/erasmus-bot/tree/main/erasmus-site-parsed'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all div elements with the specified class
    div_elements = soup.find_all('div', class_='react-directory-truncate')

    # Directory to save the downloaded files
    download_dir = 'downloaded_html_files'
    os.makedirs(download_dir, exist_ok=True)

    # Base URL for constructing the file URLs
    base_url = 'https://raw.githubusercontent.com/WolfNuyts/erasmus-bot/main/erasmus-site-parsed/'

    # Iterate over each div element
    for div in div_elements:
        # Find the a element within the div
        a_element = div.find('a')
        if a_element and 'href' in a_element.attrs:
            # Extract the href attribute
            href = a_element['href']
            file_name = href.split('/')[-1]

            # Construct the full URL to the file
            file_url = base_url + file_name

            # Download the file
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                # Save the file
                file_path = os.path.join(download_dir, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(file_response.text)
                print(f"Downloaded {file_name}")
            else:
                print(f"Failed to download {file_name}")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")


