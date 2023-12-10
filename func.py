from extensions import *

def login_required(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if 'admin' or 'cashier' in session:
            return f(*args, **kwargs)
        return redirect(url_for('index'))

    return inner_func