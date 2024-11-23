from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# HTML template for the webpage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Entry-Level SDE Job Postings</title>
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
        .job {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }
        .job h2 {
            font-size: 1.5em;
            margin: 0;
        }
        .job p {
            margin: 5px 0;
        }
        .job a {
            color: #007bff;
            text-decoration: none;
        }
        .job a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Entry-Level SDE Jobs</h1>
        {% if jobs %}
            {% for job in jobs %}
                <div class="job">
                    <h2>{{ job.title }}</h2>
                    <p><a href="{{ job.link }}" target="_blank">Apply Now</a></p>
                </div>
            {% endfor %}
        {% else %}
            <p>No job postings found. Please try again later.</p>
        {% endif %}
    </div>
</body>
</html>
"""

def fetch_jobs_from_amazon():
    """Fetch job postings from Amazon."""
    url = "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&job_type=Full-Time&level=Entry-Level&country=USA&category=Software-Development"
    response = requests.get(url)
    jobs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.select('.job-tile')  # Update the selector based on the website's structure

        for card in job_cards:
            title = card.select_one('.job-title').text.strip()
            link = "https://www.amazon.jobs" + card.select_one('a')['href']
            jobs.append({'title': title, 'link': link})

    return jobs

def fetch_jobs_from_google():
    """Fetch job postings from Google."""
    url = "https://careers.google.com/jobs/results/?distance=50&q=software%20engineer%20entry%20level&hl=en_US"
    response = requests.get(url)
    jobs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.select('.gc-card')  # Update the selector based on the website's structure

        for card in job_cards:
            title = card.select_one('.gc-card__title').text.strip()
            link = "https://careers.google.com" + card.select_one('a')['href']
            jobs.append({'title': title, 'link': link})

    return jobs

def fetch_jobs_from_meta():
    """Fetch job postings from Meta."""
    url = "https://www.metacareers.com/jobs?is_entry_level=true&fields=Software%20Engineer&countries[0]=US&roles[0]=Full%20time%20employment&q=software"
    response = requests.get(url)
    jobs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.select('.job-card')  # Update the selector based on the website's structure

        for card in job_cards:
            title = card.select_one('.job-title').text.strip()
            link = "https://www.metacareers.com" + card.select_one('a')['href']
            jobs.append({'title': title, 'link': link})

    return jobs

def fetch_jobs_from_apple():
    """Fetch job postings from Apple."""
    url = "https://jobs.apple.com/en-us/search?location=united-states-USA&team=Software%20and%20Services&jobType=Full-Time&experienceLevel=Entry%20Level"
    response = requests.get(url)
    jobs = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.select('.table-row')  # Update the selector based on the website's structure

        for card in job_cards:
            title = card.select_one('.table-text').text.strip()
            link = "https://jobs.apple.com" + card.select_one('a')['href']
            jobs.append({'title': title, 'link': link})

    return jobs

@app.route('/')
def home():
    jobs = []

    # Aggregate job postings from all sources
    jobs.extend(fetch_jobs_from_amazon())
    jobs.extend(fetch_jobs_from_google())
    jobs.extend(fetch_jobs_from_meta())
    jobs.extend(fetch_jobs_from_apple())

    # Render the webpage with job postings
    return render_template_string(HTML_TEMPLATE, jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
