from flask import Flask
from src.controller import get_company_information, get_all_information, get_company_price_history


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_stacc():
        return 'Hello, STACC!'

    @app.route('/info')
    def get_all_companies_info():
        return get_all_information()

    @app.route('/info/<ticker>')
    def get_company_info(ticker):
        return get_company_information(ticker)

    @app.route('/historical/<ticker>')
    def get_company_historical_price_data(ticker):
        return get_company_price_history(ticker)

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=5000)
