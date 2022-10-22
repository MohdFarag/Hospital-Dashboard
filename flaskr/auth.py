import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import mysql_connector
from flaskr.log import almaza_logger

bp = Blueprint('auth', __name__, url_prefix='/auth')

#-----------Login & Logout-----------#
# Login
@bp.route("/login", methods=['GET', 'POST'])
def login():
    _,mycursor = mysql_connector()
    if request.method == 'POST':
      username  = request.form['username']
      password  = request.form['password']
     
      # Check if account exists using MySQL
      mycursor.execute(f"SELECT * FROM admin WHERE `username` = '{username}'")
      # Fetch one record and return result
      user = mycursor.fetchone()

      # If account exists in accounts table in out database
      if user:
        if check_password_hash(user[2], password):
            # Create session data, we can access this data in other routes
            session.clear()
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            almaza_logger.info(f'admin:{username} logged in succefully.')
            # Redirect to dashboard page
            return redirect(url_for('index'))
        else:
            flash("We didn't recognize the password you entered.", "error")
      else:
          # Account doesnt exist or username/password incorrect
          flash("We didn't recognize the username you entered.", "error")

    return render_template("login.html",
                          title="Login")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('id')

    if user_id is None:
        g.user = None
    else:
        _,mycursor = mysql_connector()
        mycursor.execute('SELECT * FROM admin WHERE admin_id = %s', (user_id,))
        g.user = mycursor.fetchone()

# Logout
@bp.route("/logout")
def logout():
  # Remove session data, this will log the user out
  username = session['username']
  session.clear()
  almaza_logger.info(f'admin {username} logged out succefully.')

  # Redirect to login page
  return redirect(url_for('auth.login'))

# Auth
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view