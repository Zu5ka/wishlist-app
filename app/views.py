from flask import Flask, render_template, Blueprint
from flask_login import login_required

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route("/")
@login_required
def index():
    return render_template("index.html")

@views_blueprint.route("/clicked", methods=['POST'])
def clicked():
    return "<p>clicked</p>"

@views_blueprint.route("/wishlist", methods=['POST'])
@login_required
def add_list():
    return "<p>added wishlist</p>"

@views_blueprint.route("/wishlist/<int:list_id>", methods=['GET'])
@login_required
def show_list(list_id):
    return "<p>added wishlist</p>"

@views_blueprint.route("/<int:list_id>/item", methods=['POST'])
@login_required
def add_item(list_id):
    return "<p>added item</p>"

@views_blueprint.route("/item/reserve/<int:id>", methods=['PATCH'])
@login_required
def reserve_item(id):
    return f"<p>reserved item {id}</p>"

@views_blueprint.route("/item/claim/<int:id>", methods=['PATCH'])
@login_required
def claim_item(id):
    return f"<p>claimed item {id}</p>"

@views_blueprint.route("/item/archive/<int:id>", methods=['PATCH'])
@login_required
def archive_item(id):
    return f"<p>archived item {id}</p>"

@views_blueprint.route("/wishlist/archive/<int:id>", methods=['PATCH'])
@login_required
def archive_list(id):
    return f"<p>archived wishlist {id}</p>"

@views_blueprint.route("/wishlist/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_list(id):
    return f"<p>deleted wishlist {id}</p>"

@views_blueprint.route("/item/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_item(id):
    return f"<p>deleted item {id}</p>"
