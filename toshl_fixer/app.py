import os

from dateutil.utils import today
from flask import Flask

from toshl_fixer.core.auto_tag import auto_tag
from toshl_fixer.core.delete_duplicates import delete_duplicates
from toshl_fixer.core.fetch import fetch_data

app = Flask(__name__)


@app.route('/remove-dup')
def remove_dup():
    expenses = fetch_data()
    delete_duplicates('2020-01-01', str(today()), expenses=expenses)
    return 'Done!'


@app.route('/tag')
def tag():
    auto_tag()
    return 'Done!'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
