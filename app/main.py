import logging
import os

from datetime import datetime

from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for)
from flask_wtf import FlaskForm
from wtforms import (StringField, SelectMultipleField)

__logs__ = logging.getLogger(__name__)

settings = {
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'adevsecret'),
}

app = Flask(__name__)
app.config.update(settings)

# List of Tutor Products
TUTOR_PRODUCTS = [
    'Accounts',
    'Exercises',
    'Payments',
    'Tutor',
    'Web',
]

# List of CNX Products
CNX_PRODUCTS = [
    'CNX',
    'Books'
]


def gen_product_string(product_list):
    """Generates a comma delimited string with the proper use of "and" for 2 or more items.
    """
    if len(product_list) > 2:
        last_item = 'and {}'.format(product_list[len(product_list) - 1])
        product_list[len(product_list) - 1] = last_item
        return ', '.join(product_list)
    elif len(product_list) == 2:
        return ' and '.join(product_list)
    elif 0 < len(product_list) < 2:
        return product_list[0]
    else:
        return ''


# Reminder Form
class CreateReminderForm(FlaskForm):
    release_date = StringField('Release Date')
    tutor_products = SelectMultipleField('Tutor Products', choices=[(x, x) for x in TUTOR_PRODUCTS])
    cnx_products = SelectMultipleField('CNX Products', choices=[(x, x) for x in CNX_PRODUCTS])


# Register Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', status_code=404), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', status_code=500), 500


# Start routes
@app.route('/', methods=['GET', 'POST'])
def home():
    form = CreateReminderForm(request.form)

    if form.validate_on_submit():
        __logs__.info('Reminder form validated successfully')
        tutor_products = gen_product_string(form.tutor_products.data)
        cnx_products = gen_product_string(form.cnx_products.data)
        release_date = form.release_date.data

        # Turn release_date into a datetime object for comparison
        rdate = datetime.strptime(release_date, '%b %d, %Y')

        # Check release date if it is today and if so change it to the word "today"
        if rdate.date() == datetime.today().date():
            __logs__.info('Release date detected as today.')
            release_date = 'today'

        return redirect(
            url_for('show_reminder', release_date=release_date,
                    tutor_products=tutor_products, cnx_products=cnx_products))

    return render_template('home.html', form=form)


@app.route('/reminder', methods=['GET'])
def show_reminder():
    release_date = request.args.get('release_date', '')
    tutor_products = request.args.get('tutor_products', '')
    cnx_products = request.args.get('cnx_products', '')

    return render_template('reminder.html', release_date=release_date,
                           tutor_products=tutor_products,
                           cnx_products=cnx_products)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)  # pragma: no cover
