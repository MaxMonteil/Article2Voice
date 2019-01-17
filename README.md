# Article2Voice
A mini web app that can take an article link, parse the article, and return an audio file.

## How to install

Clone the repo then install the packages

	$ git clone https://github.com/MaxMonteil/Article2Voice.git
	$ cd Article2Voice

### Server

	$ cd server
	$ pipenv install

You will need to make an account one the Google Cloud Platform and set up a project using Text to Speech, here's their tutorial:

[Cloud Text-to-Speech API Quickstart](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python)

#### Dependencies

Extra things you need to make sure you've installed so everything can run and install smoothly.

* Python 3
* Pip (the version for python 3)
* Pipenv
* Newspaper3k dependencies [link](https://github.com/codelucas/newspaper#get-it-now)
	* You won't need the NLP related libraries
