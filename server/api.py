from flask import Flask, jsonify, make_response, request, abort
from articleExtraction import extract_article

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')


@app.route('/api/v1/article', methods=['POST'])
def get_article():
    if not request.json or 'url' not in request.json:
        abort(400)

    article = extract_article(request.json['url'])
    return jsonify(article), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
