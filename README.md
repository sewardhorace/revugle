Create virtual environment

		$ python3 -m venv ~/.virtualenvs/revugle

Activate virtual environment

		$ source ~/.virtualenvs/revugle/bin/activate

Make sure all requirements are installed

		$ pip install -r requirements.txt

(Deactivate when done)

		$ deactivate


Run on Heroku

		$ git push heroku master
		$ heroku ps:scale worker=1