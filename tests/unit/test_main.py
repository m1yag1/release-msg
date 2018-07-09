from datetime import datetime


def test_root_url_loads(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert 'Release Reminder Creator' in response


def test_root_url_post_request_and_product_formatting(test_client):
    response = test_client.get('/')
    form = response.form
    form['release_date'] = 'Jul 04, 2055'
    form['tutor_products'] = ['Accounts', 'Exercises', 'Payments']
    form['cnx_products'] = ['CNX', 'Books']
    response = form.submit()
    assert response.status_code == 302
    response = response.follow()
    assert 'Jul 04, 2055' in response
    assert 'Accounts, Exercises, and Payments' in response
    assert 'CNX and Books' in response


def test_root_url_post_request_with_todays_date(test_client):
    response = test_client.get('/')
    form = response.form
    form['release_date'] = datetime.today().date().strftime('%b %d, %Y')

    response = form.submit()
    assert response.status_code == 302
    response = response.follow()
    assert 'today' in response


def test_root_url_post_request_with_single_product(test_client):
    response = test_client.get('/')
    form = response.form
    form['tutor_products'] = ['Accounts']
    form['cnx_products'] = ['CNX']
    assert 'Accounts' in response
    assert 'CNX' in response


def test_gen_product_string():
    one_product = ['Accounts']
    two_products = ['CNX', 'Books']
    many_products = ['Accounts', 'Exercises', 'Payments', 'Web']
    from app.main import gen_product_string

    assert gen_product_string(one_product) == 'Accounts'
    assert gen_product_string(two_products) == 'CNX and Books'
    assert gen_product_string(many_products) == 'Accounts, Exercises, Payments, and Web'


def test_error_page_404(test_client):
    response = test_client.get('/supadupafly', expect_errors=True)
    assert response.status_code == 404


def test_error_page_500(test_client):
    response = test_client.get('/fivehundred', expect_errors=True)
    assert response.status_code == 500

