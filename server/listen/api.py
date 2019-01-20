'''Standard application API'''
import os
import sys
from flask import Flask, jsonify, make_response, abort, send_from_directory
from flask_cors import CORS
from urllib.parse import urlparse
from articleExtraction import extract_article
from texttospeech import article_to_speech

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
CORS(app)

SELF_URL = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return jsonify({'message': 'This is an example'})


@app.route('/api/v1/article/<path:article_url>', methods=['GET', 'OPTIONS'])
def get_article(article_url):
    # Make sure there is a url passed
    if not article_url or len(article_url) == 0:
        abort(400)

    if not url_validator(article_url):
        abort(400)

    article = extract_article(article_url)

    filename = (article['title'].encode('ascii', 'ignore').decode('utf-8') +
                '.mp3')

    if len(article['text']) >= 5000:
        abort(413)

    if not file_was_downloaded(filename):
        binary_audio = article_to_speech(article['text'])

        with open(os.environ['AUDIOS_DIR'] + '/' + filename, 'wb') as out:
            out.write(binary_audio)

    return jsonify({'file': SELF_URL + 'audio/' + filename})


@app.route('/audio/<string:filename>')
def stream_audio(filename):
    if not file_was_downloaded(filename):
        abort(404)

    return send_from_directory(os.environ['AUDIOS_DIR'], filename,
                               mimetype='audio/mp3',
                               attachment_filename=filename)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(413)
def article_too_long(error):
    return make_response(jsonify({'error': 'The article is too long.'}), 413)


def url_validator(url):
    '''Verifies that the given URL is valid and complete.'''
    result = urlparse(url)
    return all([result.scheme, result.netloc, result.path])


def file_was_downloaded(filename):
    filepath = os.path.join(os.environ['AUDIOS_DIR'], filename)

    return os.path.isfile(filepath)


if __name__ == '__main__':
    app.run(debug=True)
