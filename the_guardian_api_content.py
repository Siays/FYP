import requests
import re


def split_and_clean_paragraphs(html_content):
    # Find all content between <p> and </p> tags
    paragraphs = re.findall(r'<p>(.*?)</p>', html_content, re.DOTALL)

    # Clean up each paragraph by removing other HTML tags
    cleaned_paragraphs = []
    for para in paragraphs:
        # Remove other HTML tags within the paragraph
        cleaned_text = re.sub(r'<[^>]+>', '', para).strip()
        if cleaned_text:
            cleaned_paragraphs.append(cleaned_text)

    return cleaned_paragraphs


# Example usage

api_key = 'a70a305b-9dee-4a94-96fd-3a9345d0af9c'
url = 'https://content.guardianapis.com/search'
params = {
    'q': 'technology',
    'api-key': api_key,
    'show-fields': 'all'
}

response = requests.get(url, params=params)
data = response.json()
choice = 5
articles = data['response']['results']
selected_article = articles[choice]['fields']['body']

# content = selected_article['fields']['body']  # Get the HTML content from the article data
paragraphs = split_and_clean_paragraphs(selected_article)
# print(paragraphs[0])


for i, paragraph in enumerate(paragraphs, 1):
    print(f"Paragraph {i}: {paragraph}\n")