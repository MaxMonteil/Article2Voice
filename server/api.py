'''Standard application API'''
import io
import sys
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
from articleExtraction import extract_article
from texttospeech import article_to_speech, generate_mp3_file

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
CORS(app)


@app.route('/')
def index():
    return jsonify({'message': 'This is an example'})


@app.route('/api/v1/article', methods=['POST'])
def get_article():
    if not request.json or 'url' not in request.json:
        abort(400)

    print('Getting article...', file=sys.stderr)
    article = extract_article(request.json['url'])
    print('Article retrieved!\n', file=sys.stderr)
    # When the file name is sent as a header it can only have ascii characaters
    # .encode with ignore converts to ascii and removes the rest
    # this gives us a byte string so decode turns it back
    filename = (article['title'].encode('ascii', 'ignore').decode('utf-8') +
                '.mp3')

    print('Getting audio...', file=sys.stderr)
    binary_audio = article_to_speech(article['text'])
    print('Retrieved audio!\n', file=sys.stderr)

    # Buffer to keep file in memory instead of writing it to drive
    buff = io.BytesIO()
    print(len(buff.getvalue()), file=sys.stderr)
    content_length = generate_mp3_file(buff, binary_audio)
    print(len(buff.getvalue()), file=sys.stderr)

    response = make_response(buff.getvalue())
    buff.close()

    response.headers['Content-Type'] = 'audio/mpeg'
    response.headers['Content-Length'] = content_length
    # When testing with Postman it ignores the filename
    # Might not happen when testing from a browser
    # TODO Fix generated file name
    response.headers['Content-Disposition'] = f'attachment;filename={filename}'

    # For some reason it returns the file twice.
    # I think it has to do with the buffer. But I don't know where it doubles
    # and if that means it's pinging the Google api twice.
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
