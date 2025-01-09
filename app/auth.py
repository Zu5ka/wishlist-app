from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from . import app, db
from .models import User

@app.route("/login", methods=['GET', 'POST'])
def login():
  pass

@app.route("/register", methods=['GET', 'POST'])
def register():
  pass

@app.route("/logout", methods=['POST'])
@login_required
def logout():
  pass