from flask import Flask
from src.controller import Controller
import logging


def create_app():
    logging.basicConfig(filename='flask_logs.log', level=logging.DEBUG)

    app = Flask(__name__)

    @app.route('/')
    def hello_stacc():
        return 'Hello, STACC!'

    @app.route('/info')
    def get_all_companies_info():
        return Controller.get_all_information()

    @app.route('/info/<ticker>')
    def get_company_info(ticker):
        return Controller.get_company_information(ticker)

    @app.route('/historical/<ticker>')
    def get_company_historical_price_data(ticker):
        return Controller.get_company_price_history(ticker)

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=5000)
