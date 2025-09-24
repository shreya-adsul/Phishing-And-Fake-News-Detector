from flask import Flask, request, jsonify, render_template # pyright: ignore[reportMissingImports]
from joblib import load
from urllib.parse import urlparse
import re

app = Flask(__name__)

# ----------------------------
# Preprocessing functions
# ----------------------------

def preprocess_url(url):
    url = url.lower().strip()
    if url.startswith("http://") or url.startswith("https://"):
        url = url.split("//")[1]  # remove protocol
    if url.endswith("/"):
        url = url[:-1]
    return url

def preprocess_text(text):
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    # Keep numbers and abbreviations
    return text

# ----------------------------
# Load Phishing model & vectorizer
# ----------------------------
phishing_model = load("models/phishing.pk1")
vectorizer = load("models/vectorizer.pk1")

# ----------------------------
# Load Fake News model & vectorizer
# ----------------------------
fake_news_model = load("models/lr_model.pkl")
fake_news_vectorizer = load("models/vectorizer.pkl")

# ----------------------------
# Home & About Pages
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# ----------------------------
# Phishing Page
# ----------------------------
@app.route('/phishing', methods=['GET', 'POST'])
def phishing_page():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            url = data.get('url') if data else None
        else:
            url = request.form.get('url')

        if not url:
            msg = "No URL provided"
            if request.is_json:
                return jsonify({"error": msg}), 400
            else:
                return render_template('phishing.html', result=msg, url="")

        result = check_phishing(url)
        suggestion = None
        if result == "⚠️ Phishing URL detected!":
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            if domain.startswith("www."):
                domain = domain[4:]
            suggestion = f"https://{domain}"

        if request.is_json:
            return jsonify({"result": result, "suggestion": suggestion})
        else:
            return render_template('phishing.html', result=result, suggestion=suggestion, url=url)

    return render_template('phishing.html', result=None)

def check_phishing(url):
    url = preprocess_url(url)
    vectorized_url = vectorizer.transform([url])
    prediction = phishing_model.predict(vectorized_url)[0]

    if prediction == "bad":
        return "⚠️ Phishing URL detected!"
    else:
        return "✅ Safe URL"

# ----------------------------
# Fake News Page
# ----------------------------
@app.route('/fakenews', methods=['GET', 'POST'])
def fake_news_page():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            news_text = data.get('news') if data else None
        else:
            news_text = request.form.get('news')

        if not news_text:
            msg = "No news text provided"
            if request.is_json:
                return jsonify({"error": msg}), 400
            else:
                return render_template('fake-news.html', result=msg, news="")

        result = check_fake_news(news_text)

        if request.is_json:
            return jsonify({"result": result})
        else:
            return render_template('fake-news.html', result=result, news=news_text)

    return render_template('fake-news.html', result=None)

def check_fake_news(text):
    cleaned_text = preprocess_text(text)
    
    # Transform text using vectorizer
    vectorized_text = fake_news_vectorizer.transform([cleaned_text])

    # Predict using logistic regression model
    prediction = fake_news_model.predict(vectorized_text)[0]

    # Map prediction to friendly message
    if prediction == 0:  # 0 = fake, 1 = real
        return "⚠️ Fake News Detected!"
    else:
        return "✅ News seems Legitimate"

# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8000)
