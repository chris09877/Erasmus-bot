import os
from bs4 import BeautifulSoup

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content = []
    # Find all div elements with the specified class
    div_elements = soup.find_all('div', class_='field field--name-field-text field--type-text-long field--label-hidden field--item')
    for div in div_elements:
        # Find all p, h2, h3, h4, and strong elements inside the div
        elements = div.find_all(['p', 'h2', 'h3', 'h4', 'strong'])
        for element in elements:
            content.append(element.get_text(strip=True))  # Get text content, remove leading/trailing whitespace

    return content

def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        extracted_content = extract_content(html_content)
        return extracted_content

def create_text_file(file_path, content, filename):
    new_dir = 'html_to_txt'
    os.makedirs(new_dir, exist_ok=True)
    txt_file_path = os.path.join(new_dir, filename + '.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for item in content:
            txt_file.write(item + '\n')
def scan_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.startswith('opleidingen'):
            file_path = os.path.join(folder_path, filename)
            content = process_html_file(file_path)
            create_text_file(file_path, content, filename)
            os.remove(file_path)
            print(f"HTML file '{filename}' processed and deleted. Text file created.")
    print("All HTML files processed and deleted.")

folder_path = './downloaded_html_files/'
scan_html_files(folder_path)
