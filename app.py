from flask import Flask, render_template_string
import requests
import os

API_KEY = os.getenv('NEWS_API_KEY')  # Fetches API key from environment variables


app = Flask(__name__)

# Your NewsAPI key
API_KEY = 'd6f098e271eb4eb59c2b1f6812093639'

# NewsAPI endpoint
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# HTML template for the webpage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technology News</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .article {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }
        .article h2 {
            font-size: 1.5em;
            margin: 0;
        }
        .article p {
            margin: 5px 0;
        }
        .article a {
            color: #007bff;
            text-decoration: none;
        }
        .article a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Technology News</h1>
        {% if articles %}
            {% for article in articles %}
                <div class="article">
                    <h2>{{ article.title }}</h2>
                    <p><a href="{{ article.url }}" target="_blank">Read more</a></p>
                </div>
            {% endfor %}
        {% else %}
            <p>No news articles found.</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Fetch news articles
    params = {
        'apiKey': API_KEY,
        'country': 'us',
        'category': 'technology',
        'pageSize': 10  # Number of articles to fetch
    }
    response = requests.get(NEWS_API_URL, params=params)
    articles = []

    if response.status_code == 200:
        news_data = response.json()
        articles = [
            {'title': article.get('title'), 'url': article.get('url')}
            for article in news_data.get('articles', [])
        ]
    else:
        print(f"Failed to fetch news: {response.status_code}")

    # Render the template with articles
    return render_template_string(HTML_TEMPLATE, articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
