import os

from dateutil.utils import today
from flask import Flask

from toshl_fixer.core.delete_duplicates import delete_duplicates
from toshl_fixer.core.fetch import fetch_data

app = Flask(__name__)


@app.route('/remove-dup')
def remove_dup():
    fetch_data()
    delete_duplicates('2020-01-01', str(today()))
    return 'Done!'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
