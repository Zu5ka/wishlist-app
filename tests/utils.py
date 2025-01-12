"""Helper functions for test_app.py"""

def create_user(client, username, password):
    """Register a new user.

    This is a helper function for testing.
    Keyword arguments:
        username -- The username for the new user.
        password -- The password for the new user.
    """
    return client.post(
        "/register",
        data={"username": username, "password": password, "password_again": password},
    )


def logout_user(client):
    """Logout current user.

    This is a helper function for testing.
    """
    client.post("/logout")


def login_user(client, username, password):
    """Login a user.

    This is a helper function for testing.
    Keyword arguments:
        username -- The username of the user to log in.
        password -- The password of the user to log in.
    """
    return client.post("/login", data={"username": username, "password": password})


def add_list(client, list_name):
    """Add a list.

    This is a helper function for testing.
    Keyword arguments:
        list_name -- The name for the new list.
    """
    return client.post("/wishlist", data={"list_name": list_name})


def share_list(client, list_id, user_id):
    """Share a list.

    This is a helper function for testing.
    Keyword arguments:
        list_id -- The ID of the list to share.
        user_id -- The ID of the user to share the list with.
    """
    return client.patch(f"/list/{list_id}/share/{user_id}")


def unshare_list(client, list_id, user_id):
    """Unshare a list.

    This is a helper function for testing.
    Keyword arguments:
        list_id -- The ID of the list to unshare.
        user_id -- The ID of the user to unshare the list with.
    """
    return client.patch(f"/list/{list_id}/unshare/{user_id}")


def respond_error(response, status, msg):
    """Test the response status code and response message.

    This is a helper function for testing.
    Keyword arguments:
        response -- The response to test.
        status -- The expected HTTP status code.
        msg -- The expected status message.
    """
    assert response.status_code == status
    assert response.text == msg


def add_item(client, item_name, list_id):
    """Add an item.

    This is a helper function for testing.
    Keyword arguments:
        item_name -- The name for the new item.
        list_id -- The ID of the list to add the item to.
    """
    return client.post(f"/{list_id}/item", data={"new_item_name": item_name})


def reserve_item(client, item_id):
    """Reserve an item.

    This is a helper function for testing.
    Keyword arguments:
        item_id -- The ID of the item to reserve.
    """
    return client.patch(f"/item/reserve/{item_id}")


def claim_item(client, item_id):
    """Claim an item.

    This is a helper function for testing.
    Keyword arguments:
        item_id -- The ID of the item to claim.
    """
    return client.patch(f"/item/claim/{item_id}")


def delete_item(client, item_id):
    """Delete an item.

    This is a helper function for testing.
    Keyword arguments:
        item_id -- The ID of the item to delete.
    """
    return client.delete(f"/item/delete/{item_id}")


def archive_list(client, list_id):
    """Archive a list.

    This is a helper function for testing.
    Keyword arguments:
        list_id -- The ID of the list to archive.
    """
    return client.patch(f"/wishlist/archive/{list_id}")


def delete_list(client, list_id):
    """Delete a list.

    This is a helper function for testing.
    Keyword arguments:
        list_id -- The ID of the list to delete.
    """
    return client.delete(f"/wishlist/delete/{list_id}")


def search_user(client, list_id, search):
    """Search for a user.

    This is a helper function for testing.
    Keyword arguments:
        list_id -- The ID of the list for which to search for users available for sharing.
        search -- the search query.
    """
    return client.post(f"/user/search/{list_id}", data={"search": search})
