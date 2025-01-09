from flask import Flask, render_template
from flask_login import login_required
from . import app

@app.route("/")
def hello_world():
    return render_template("base.html", content="Hello World")

@app.route("/clicked", methods=['POST'])
def clicked():
    return "<p>clicked</p>"

@app.route("/wishlist", methods=['POST'])
@login_required
def add_list():
    return "<p>added wishlist</p>"

@app.route("/item", methods=['POST'])
@login_required
def add_item():
    return "<p>added item</p>"

@app.route("/item/reserve/<int:id>", methods=['PATCH'])
@login_required
def reserve_item(id):
    return f"<p>reserved item {id}</p>"

@app.route("/item/claim/<int:id>", methods=['PATCH'])
@login_required
def claim_item(id):
    return f"<p>claimed item {id}</p>"

@app.route("/item/archive/<int:id>", methods=['PATCH'])
@login_required
def archive_item(id):
    return f"<p>archived item {id}</p>"

@app.route("/wishlist/archive/<int:id>", methods=['PATCH'])
@login_required
def archive_list(id):
    return f"<p>archived wishlist {id}</p>"

@app.route("/wishlist/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_list(id):
    return f"<p>deleted wishlist {id}</p>"

@app.route("/item/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_item(id):
    return f"<p>deleted item {id}</p>"
