from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from . import db
from .models import Wishlist, Item, User, ItemState, ListState

views_blueprint = Blueprint("views", __name__)


@views_blueprint.route("/")
@login_required
def index():
    return render_template("index.html", results=[])


@views_blueprint.route("/wishlist", methods=["POST"])
@login_required
def add_list():
    list_name = request.form.get("list_name")
    if not list_name or list_name.strip() == "":
        return "Název seznamu musí obsahovat alespoň jeden znak.", 400
    wishlist = Wishlist(name=list_name, user_id=current_user.id)
    db.session.add(wishlist)
    db.session.commit()
    return render_template("_partials/_lists_menu_entry.html", list=wishlist)


@views_blueprint.route("/wishlist/<int:list_id>", methods=["GET"])
@login_required
def show_list(list_id):
    list = Wishlist.query.filter_by(id=list_id).first()
    if list.user_id != current_user.id and current_user not in list.shared_with:
        return "Nemáte právo zobrazit tento seznam", 403
    return render_template("_partials/_list.html", list=list, current_user=current_user)


@views_blueprint.route("/<int:list_id>/item", methods=["POST"])
@login_required
def add_item(list_id):
    item_name = request.form.get("new_item_name")
    if not item_name or item_name.strip() == "":
        return "Název položky musí obsahovat alespoň jeden znak.", 400
    list = Wishlist.query.filter_by(id=list_id).first()
    if not list:
        return "Seznam neexistuje.", 404
    if list.user != current_user:
        return "Seznam není Váš.", 403
    item = Item(name=item_name, wishlist_id=list_id)
    db.session.add(item)
    db.session.commit()
    return render_template(
        "_partials/_item.html", list=item.wishlist, item=item, current_user=current_user
    )


@views_blueprint.route("/item/reserve/<int:id>", methods=["PATCH"])
@login_required
def reserve_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Položka neexistuje.", 404
    if item.state != ItemState.active and item.state != ItemState.reserved:
        return "Položka je předaná nebo smazaná.", 400
    if current_user not in item.wishlist.shared_with:
        return "Seznam je Váš nebo s Vámi není sdílený.", 403
    if item.state == ItemState.active:
        item.state = ItemState.reserved
    else:
        item.state = ItemState.active
    db.session.commit()
    return "", 200


@views_blueprint.route("/item/claim/<int:id>", methods=["PATCH"])
@login_required
def claim_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Položka neexistuje.", 404
    if item.state == ItemState.deleted:
        return "Položka už je smazaná.", 400
    if current_user != item.wishlist.user:
        return "Seznam není Váš.", 403
    if item.state != ItemState.claimed:
        item.state = ItemState.claimed
    else:
        item.state = ItemState.active
    db.session.commit()
    return render_template(
        "_partials/_item.html", item=item, list=item.wishlist, current_user=current_user
    ), 200


@views_blueprint.route("/wishlist/archive/<int:id>", methods=["PATCH"])
@login_required
def archive_list(id):
    list = Wishlist.query.filter_by(id=id).first()
    if not list:
        return "Seznam neexistuje.", 404
    if list.state == ListState.deleted:
        return "Seznam je smazaný.", 400
    if current_user != list.user:
        return "Seznam není váš.", 403
    if list.state != ListState.archived:
        list.state = ListState.archived
    else:
        list.state = ListState.active
    db.session.commit()
    return render_template(
        "_partials/_list.html", list=list, current_user=current_user, oob=True
    ), 200


@views_blueprint.route("/wishlist/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_list(id):
    list = Wishlist.query.filter_by(id=id).first()
    if not list:
        return "Seznam neexistuje.", 404
    if list.user_id != current_user.id:
        return "Seznam patří jinému uživateli.", 403
    list.state = 2
    db.session.commit()
    return render_template("_partials/_placeholder.html", list=list, oob=True), 200


@views_blueprint.route("/item/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_item(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Položka neexistuje.", 404
    if item.wishlist.user_id != current_user.id:
        return "Položka neexistuje ve Vašem seznamu.", 403
    if item.wishlist.state != ItemState.active:
        return "Položka se nachází na archivovaném nebo smazaném seznamu", 400
    item.state = 3
    db.session.commit()
    return "", 200


@views_blueprint.route("/user/search/<int:list_id>", methods=["POST"])
@login_required
def search_user(list_id):
    user_query = request.form.get("search")
    list = Wishlist.query.filter_by(id=list_id).first()
    if not list:
        return "Seznam neexistuje.", 404
    if not user_query:
        return render_template(
            "_partials/_user_search_results.html", results=[], list=list
        )
    users = (
        User.query.filter(User.username.ilike("%" + user_query + "%")).limit(20).all()
    )
    results = [x for x in users if x not in list.shared_with and x != current_user]
    return render_template(
        "_partials/_user_search_results.html", results=results, list=list
    )


@views_blueprint.route("/list/<int:list_id>/share/<int:user_id>", methods=["PATCH"])
@login_required
def share_list(list_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    list = Wishlist.query.filter_by(id=list_id).first()
    if not user or not list:
        return "Uživatel nebo seznam neexistuje.", 404
    if list.user_id != current_user.id:
        return "Seznam patří jinému uživateli.", 403
    if user_id == current_user.id:
        return "Nelze nasdílet vlastní seznam.", 400
    if user in list.shared_with:
        return "Seznam již je nasdílený.", 400
    list.shared_with.append(user)
    db.session.commit()
    return render_template(
        "_partials/_shared_user.html", user=user, list=list, oob=True
    )


@views_blueprint.route("/list/<int:list_id>/unshare/<int:user_id>", methods=["PATCH"])
@login_required
def unshare_list(list_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    list = Wishlist.query.filter_by(id=list_id).first()
    if not user or not list:
        return "Uživatel nebo seznam neexistuje.", 404
    if list.user_id != current_user.id:
        return "Seznam patří jinému uživateli.", 403
    if user_id == current_user.id:
        return "Nelze provést s vlastním seznamem.", 400
    if user not in list.shared_with:
        return "Seznam není sdílený s tímto uživatelem.", 400
    list.shared_with.remove(user)
    db.session.commit()
    return "", 200, {"HX-Trigger": "search-refresh"}
