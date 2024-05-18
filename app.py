import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
import googletrans

from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

def get_synonyms_antonyms(word):
    # 네이버 사전 URL
    url = f"https://ko.dict.naver.com/api3/koko/search?query={word}"
    
    # HTTP GET 요청을 보내고 응답을 받습니다.
    response = requests.get(url)
    
    # 응답을 파싱합니다.
    if response.status_code == 200:
        data = response.json()
        
        # 유의어와 반의어를 추출합니다.
        if 'entry' in data and data['entry']:
            entry = data['entry'][0]
            synonyms = entry.get('means', {}).get('synonym', [])
            antonyms = entry.get('means', {}).get('antonym', [])
            return synonyms, antonyms
    return [], []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    translator = googletrans.Translator()

    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    translated_text = translator.translate(original_text, dest=target_language).text
    original_language = translator.translate(original_text, dest=target_language).src

    # Get synonyms and antonyms
    synonyms, antonyms = get_synonyms_antonyms(original_text)

    # Call render template, passing the translated text,
    # original text, target language, synonyms, and antonyms to the template
    return render_template(
        'result.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language,
        original_language=original_language,
        synonyms=synonyms,
        antonyms=antonyms
    )
