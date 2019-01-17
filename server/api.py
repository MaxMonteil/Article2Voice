from flask import Flask

# create and configure the app
app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
