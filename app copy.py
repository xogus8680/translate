import requests, os, uuid, json
import googletrans

from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    translator = googletrans.Translator()

    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    translated_text=translator.translate(original_text, dest=target_language).text  
    original_language = translator.translate(original_text, dest=target_language).src
    trans_trans=translator.translate('Translated text', dest=original_language).text
    origin_origin=translator.translate('Original text', dest=original_language).text


    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'result.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language,
        trans_trans=trans_trans,
        origin_origin=origin_origin,
        original_language=original_language
    )
