Phishing & Fake News Detector
A web-based application built with Flask to detect phishing URLs and fake news articles using machine learning models.

🛠 Features
Phishing Detector

Enter a URL to check if it is safe or a phishing attempt.
Provides a suggested safe URL if phishing is detected.
Fake News Detector

Paste news text to check whether it is real or fake.
Uses a trained ML pipeline (lr_model.pkl or fake_news_pipeline.pkl) for predictions.
Responsive UI

Clean, modern interface with a clear button for input fields.
Works on desktop and mobile devices.
💻 Tech Stack
Backend: Python, Flask
Frontend: HTML, CSS, JavaScript
Machine Learning: scikit-learn (joblib for model serialization)
Models:
phishing.pk1 for URL classification
lr_model.pkl or fake_news_pipeline.pkl for fake news classification
project/ │ ├── app.py # Flask app ├── models/ │ ├── phishing.pk1 # Phishing ML model │ ├── vectorizer.pk1 # URL vectorizer │ ├── fake_news_pipeline.pkl # Fake news ML pipeline ├── templates/ │ ├── index.html │ ├── phishing.html │ ├── fake-news.html │ └── about.html ├── static/ │ ├── css/ │ │ ├── phishing.css │ │ └── fake-news.css │ └── images/ └── README.md

🚀 Installation
Clone the repository
git clone https://github.com/USERNAME/REPO.git
cd REPO


Create a virtual environment

python -m venv env


Activate the environment

Windows CMD:

env\Scripts\activate


PowerShell:

.\env\Scripts\Activate.ps1


Mac/Linux:

source env/bin/activate


Install dependencies

pip install -r requirements.txt


If requirements.txt is missing, install manually:

pip install flask joblib scikit-learn


Run the application

python app.py


Open http://127.0.0.1:8000 in your browser.

⚡ Usage

Navigate to Phishing Detector → Enter a URL → Click Check URL

Navigate to Fake News Detector → Paste news text → Click Check News

View results and suggestions on the page.
