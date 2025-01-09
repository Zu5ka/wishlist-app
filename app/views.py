from flask import Flask, render_template, Blueprint, request
from flask_login import login_required, current_user
from . import db
from .models import Wishlist, Item

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
    list_name = request.form.get('list_name')
    if not list_name or list_name.strip() == "":
        return "Název seznamu musí obsahovat alespoň jeden znak."
    wishlist = Wishlist(name=list_name, user_id=current_user.id)
    db.session.add(wishlist)
    db.session.commit()
    return render_template("_partials/_lists_menu_entry.html", list=wishlist)

@views_blueprint.route("/wishlist/<int:list_id>", methods=['GET'])
@login_required
def show_list(list_id):
    list = Wishlist.query.filter_by(id=list_id).first()
    return render_template("_partials/_list.html", list=list, current_user=current_user)

@views_blueprint.route("/<int:list_id>/item", methods=['POST'])
@login_required
def add_item(list_id):
    item_name = request.form.get('new_item_name')
    if not item_name or item_name.strip() == "":
        return "Název položky musí obsahovat alespoň jeden znak."
    item = Item(name=item_name, wishlist_id=list_id)
    db.session.add(item)
    db.session.commit()
    return render_template("_partials/_item.html", list=item.wishlist, item=item, current_user=current_user)

@views_blueprint.route("/item/reserve/<int:id>", methods=['PATCH'])
@login_required
def reserve_item(id):
    return f"<p>reserved item {id}</p>"

@views_blueprint.route("/item/claim/<int:id>", methods=['PATCH'])
@login_required
def claim_item(id):
    return f"<p>archived item {id}</p>"

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
    # TODO: add a button
    return f"<p>deleted wishlist {id}</p>"

@views_blueprint.route("/item/delete/<int:id>", methods=['DELETE'])
@login_required
def delete_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Položka neexistuje."
    if item.wishlist.user_id != current_user.id:
        return "Položka v tomto seznamu neexistuje."
    item.state = 3
    db.session.commit()
    return "", 200