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
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if wishlist.user_id != current_user.id and current_user not in wishlist.shared_with:
        return "Nemáte právo zobrazit tento seznam", 403
    return render_template("_partials/_list.html", list=wishlist, current_user=current_user)


@views_blueprint.route("/<int:list_id>/item", methods=["POST"])
@login_required
def add_item(list_id):
    item_name = request.form.get("new_item_name")
    if not item_name or item_name.strip() == "":
        return "Název položky musí obsahovat alespoň jeden znak.", 400
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if not wishlist:
        return "Seznam neexistuje.", 404
    if wishlist.user != current_user:
        return "Seznam není Váš.", 403
    item = Item(name=item_name, wishlist_id=list_id)
    db.session.add(item)
    db.session.commit()
    return render_template(
        "_partials/_item.html", list=item.wishlist, item=item, current_user=current_user
    )


@views_blueprint.route("/item/reserve/<int:id>", methods=["PATCH"])
@login_required
def reserve_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if not item:
        return "Položka neexistuje.", 404
    if item.state not in (ItemState.active, ItemState.reserved):
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
def claim_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
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
def archive_list(list_id):
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if not wishlist:
        return "Seznam neexistuje.", 404
    if wishlist.state == ListState.deleted:
        return "Seznam je smazaný.", 400
    if current_user != wishlist.user:
        return "Seznam není váš.", 403
    if wishlist.state != ListState.archived:
        wishlist.state = ListState.archived
    else:
        wishlist.state = ListState.active
    db.session.commit()
    return render_template(
        "_partials/_list.html", list=wishlist, current_user=current_user, oob=True
    ), 200


@views_blueprint.route("/wishlist/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_list(list_id):
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if not wishlist:
        return "Seznam neexistuje.", 404
    if wishlist.user_id != current_user.id:
        return "Seznam patří jinému uživateli.", 403
    wishlist.state = 2
    db.session.commit()
    return render_template("_partials/_placeholder.html", list=wishlist, oob=True), 200


@views_blueprint.route("/item/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
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
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if not wishlist:
        return "Seznam neexistuje.", 404
    if wishlist.user_id != current_user.id:
        return "Seznam není Váš.", 403
    if not user_query:
        return render_template(
            "_partials/_user_search_results.html", results=[], list=wishlist
        )
    results = current_user.search_to_share(wishlist, user_query)
    return render_template(
        "_partials/_user_search_results.html", results=results, list=wishlist
    )


@views_blueprint.route("/list/<int:list_id>/share/<int:user_id>", methods=["PATCH"])
@login_required
def share_list(list_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if not user or not wishlist:
        return "Uživatel nebo seznam neexistuje.", 404
    if wishlist.user_id != current_user.id:
        return "Seznam patří jinému uživateli.", 403
    if user_id == current_user.id:
        return "Nelze nasdílet vlastní seznam.", 400
    if user in wishlist.shared_with:
        return "Seznam již je nasdílený.", 400
    wishlist.shared_with.append(user)
    db.session.commit()
    return render_template(
        "_partials/_shared_user.html", user=user, list=wishlist, oob=True
    )


@views_blueprint.route("/list/<int:list_id>/unshare/<int:user_id>", methods=["PATCH"])
@login_required
def unshare_list(list_id, user_id):
    user = User.query.filter_by(id=user_id).first()
    wishlist = Wishlist.query.filter_by(id=list_id).first()
    if not user or not wishlist:
        return "Uživatel nebo seznam neexistuje.", 404
    if wishlist.user_id != current_user.id:
        return "Seznam patří jinému uživateli.", 403
    if user_id == current_user.id:
        return "Nelze provést s vlastním seznamem.", 400
    if user not in wishlist.shared_with:
        return "Seznam není sdílený s tímto uživatelem.", 400
    wishlist.shared_with.remove(user)
    db.session.commit()
    return "", 200, {"HX-Trigger": "search-refresh"}
