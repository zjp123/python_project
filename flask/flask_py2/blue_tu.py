from flask import Blueprint

app_stores = Blueprint('zjp', __name__)

@app_stores.route('/order')
def get_order():

    return 'order'