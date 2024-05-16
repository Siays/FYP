import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

def scrape_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for article in soup.find_all('article', class_='article'):
        title = article.find('h1').text.strip()
        content = article.find('div', class_='entry-content').text.strip()
        articles.append({'title': title, 'content': content})
    return articles

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    tokens = [re.sub(r'[^a-zA-Z0-9]', '', token) for token in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)

def calculate_cosine_similarity(articles, user_input):
    tfidf_vectorizer = TfidfVectorizer()
    article_texts = [article['content'] for article in articles]
    article_texts.append(user_input)
    tfidf_matrix = tfidf_vectorizer.fit_transform(article_texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])
    return cosine_similarities

def rank_articles(cosine_similarities, articles):
    sorted_indices = cosine_similarities.flatten().argsort()[::-1]
    sorted_articles = [articles[i] for i in sorted_indices]
    return sorted_articles

def scrape_courses(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the cards from the webpage
    cards = soup.find_all('div', class_='sc-d56bc236-4')

    # Initialize an empty list to store the courses data
    courses_data = []

    # Iterate over the cards and extract the required data
    for card in cards:
        title = card.find('p', class_='sc-d56bc236-10 tdBWn').text
        duration = card.find('p', class_='sc-d56bc236-0 sc-d56bc236-12 sc-d56bc236-13 iOJnhy dFhhBp').text
        categories = card.find_all('p', class_='sc-d56bc236-0 sc-d56bc236-2 iOJnhy llXHdp')
        category_names = [category.text for category in categories]
        course_data = {
            'title': title,
            'duration': duration,
            'categories': category_names
        }
        courses_data.append(course_data)

    return courses_data

def main():
    user_input = input("Enter your search query: ")
    if not user_input:
        print("Error: Empty search query")
        return

    url = "https://aeon.co/search?q=" + user_input
    courses_url = 'https://www.website.com'  # replace with the actual url

    courses_data= scrape_courses(courses_url)
    if not courses_data:
        print("Error: No courses found")
        return

    articles = scrape_articles(url)
    if not articles:
        print("Error: No articles found")
        return

    preprocessed_user_input = preprocess_text(user_input)
    cosine_similarities = calculate_cosine_similarity(articles, preprocessed_user_input)
    sorted_articles = rank_articles(cosine_similarities, articles)

    print("Ranked Articles:")
    for i, article in enumerate(sorted_articles, start=1):
        print(f"Rank {i}: {article['title']}")

    print("\nCourses:")
    for course in courses_data:
        print(f"Title: {course['title']}\nDuration: {course['duration']}\nCategories: {course['categories']}\n")

if __name__ == "__main__":
    main()