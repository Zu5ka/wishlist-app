from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
  return render_template('login.html')

@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
  return render_template('register.html')

@auth_blueprint.route("/logout", methods=['POST'])
@login_required
def logout():
  pass