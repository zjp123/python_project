from . import cart_app


@cart_app.route('/getcart')
def getcart():

    return 'cart'