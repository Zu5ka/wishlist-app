def create_user(client, username, password):
    return client.post("/register", data={
        "username": username,
        "password": password,
        "password_again": password
    })

def login_user(client, username, password):
    return client.post("/login", data={
        "username": username,
        "password": password
    })
