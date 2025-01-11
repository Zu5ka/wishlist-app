from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
      return "Zadejte uživatelské jméno i heslo.", 400
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
      login_user(user)
      return '',200, {'HX-Redirect': url_for('views.index')}
    else:
      return "Nesprávné heslo nebo uživatelské jméno.", 400

@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  else:
    username = request.form.get('username')
    password = request.form.get('password')
    password_again = request.form.get('password_again')
    if not username or not password or not password_again:
      return "Vyplňte všechna pole.", 400
    if username.strip() == "" or password.strip() == "":
      return "Uživatelské jméno musí obsahovat alespoň 1 znak a heslo musí být dlouhé alespoň 8 znaků.", 400
    if password != password_again:
      return "Hesla se neshodují.", 400
    if len(password) < 8:
      return "Zadejte heslo dlouhé alespoň 8 znaků.", 400
    if User.query.filter_by(username=username).first():
      return "Uživatel s tímto jménem už existuje.", 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return '', 200, {'HX-Redirect': url_for('views.index')}

@auth_blueprint.route("/logout", methods=['POST'])
@login_required
def logout():
  logout_user()
  return '', 200, {'HX-Redirect': url_for('auth.login')}