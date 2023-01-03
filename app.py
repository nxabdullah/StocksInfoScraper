from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests


def scrape_prices(name):
    url = 'http://marketwatch.com/investing/stock/' + name

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')

    # get current price
    price = soup.find('bg-quote', class_='value').string

    # get closing price
    closing_price = soup.find('meta', {'name': 'price'}).attrs['content']

    # get 52 week range (upper, lower)
    range = soup.find('mw-rangebar', class_='element element--range range--yearly')
    range_upper = range.attrs['bar-high']
    range_lower = range.attrs['bar-low']

    # get analysis rating
    analyst_rating_container = soup.find('div', class_='element element--analyst')

    analyst_rating = analyst_rating_container \
        .find('li', class_="analyst__option active").string

    return {
            'name': name,
            'price': price,
            'range': [range_lower, range_upper],
            'closing_price': closing_price,
            'analyst_rating': analyst_rating
            }


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        # get the input form value
        stock_name = request.form['input_form'].lower()

        # process the input value and generate output
        output = scrape_prices(stock_name)

        print(output)

    return render_template('index.html', output=output)


if __name__ == '__main__':
    app.run()
