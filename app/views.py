from flask import Flask, render_template, Blueprint, request
from flask_login import login_required, current_user
from . import db
from .models import Wishlist, Item, User

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route("/")
@login_required
def index():
    return render_template("index.html", results=[])

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
    list = Wishlist.query.filter_by(id=id).first()
    if not list:
        return "Seznam neexistuje."
    if list.user_id != current_user.id:
        return "Seznam patří jinému uživateli."
    list.state = 3
    db.session.commit()
    return render_template("_partials/_placeholder.html", list=list, oob=True), 200

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

@views_blueprint.route("/user/search/<int:list_id>", methods=['POST'])
@login_required
def search_user(list_id):
    user_query = request.form.get('search')
    list = Wishlist.query.filter_by(id=list_id).first()
    if not list:
        return "Seznam neexistuje."
    if not user_query:
        return render_template("_partials/_user_search_results.html", results=[], list=list)
    users = User.query.filter(User.username.ilike("%" + user_query + "%")).limit(20).all()
    results = [x for x in users if x not in list.shared_with and x != current_user]
    return render_template("_partials/_user_search_results.html", results=results, list=list)

@views_blueprint.route("/list/<int:list_id>/share/<int:user_id>", methods=['PATCH'])
@login_required
def share_list(list_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    list = Wishlist.query.filter_by(id=list_id).first()
    if not user or not list:
        return "Uživatel nebo seznam neexistuje."
    if list.user_id != current_user.id:
        return "Seznam patří jinému uživateli."
    if user_id == current_user.id:
        return "Nelze nasdílet vlastní seznam."
    if user in list.shared_with:
        return "Seznam již je nasdílený."
    list.shared_with.append(user)
    db.session.commit()
    return render_template("_partials/_shared_user.html", user=user, list=list, oob=True)

@views_blueprint.route("/list/<int:list_id>/unshare/<int:user_id>", methods=['PATCH'])
@login_required
def unshare_list(list_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    list = Wishlist.query.filter_by(id=list_id).first()
    if not user or not list:
        return "Uživatel nebo seznam neexistuje."
    if list.user_id != current_user.id:
        return "Seznam patří jinému uživateli."
    if user_id == current_user.id:
        return "Nelze provést s vlastním seznamem."
    if not user in list.shared_with:
        return "Seznam už je nasdílený."
    list.shared_with.remove(user)
    db.session.commit()
    return "", 200, {"HX-Trigger" : "search-refresh"}
