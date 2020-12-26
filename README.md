# Ingatlan Scraper
The web scraper allowing to get real estate data.

## How to start

**You need:** Git, Python3, pip.

### Following by steps

* Clone the App repository using Git

`git clone https://github.com/msydor3nko/ingatlan_scraper.git`

* Enter to the 'ingatlan_scraper' directory

`cd ingatlan_scraper`

* Create and activate virtual environment

`python3 -m venv venv`

`source venv/bin/activate`

* Install all required libraries from 'requirements.txt'

`pip install -r requirements.txt`

* Create '.env' file and paste there 'DATABASE_CONNECTION' setting (e.g. bellow):

`DATABASE_CONNECTION='postgresql+psycopg2://username:password@host:port/dbname'`

* Chose data saving mode ("db" or "csv") using "DATA_STORAGE_SETTINGS" in "config.py"  

`DATA_STORAGE_SETTINGS = "db"`

## How to run the App

* Run 'main.py' file using command

`python main.py`
