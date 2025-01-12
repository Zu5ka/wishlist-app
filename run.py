import argparse
import secrets
from waitress import serve
from app import create_app, db, DEFAULT_DB

DEFAULT_HOST = "127.0.0.1"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wishlist app")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port on which the app should run"
    )
    parser.add_argument("--prod", action="store_true", help="Run in production mode")
    parser.add_argument(
        "--db-url",
        default=DEFAULT_DB,
        help=f"Database URL (default {DEFAULT_DB})"
    )
    parser.add_argument(
        "--secret",
        default=secrets.token_hex(32),
        help="Secret key (default: random)"
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Host (default: {DEFAULT_HOST})"
    )
    args = parser.parse_args()

    wishlist_app = create_app(db_url=args.db_url, secret=args.secret)

    with wishlist_app.app_context():
        db.create_all()

    if args.prod:
        serve(wishlist_app, host=args.host, port=args.port)
    else:
        # flask debug server
        wishlist_app.run(debug=True, host=args.host, port=args.port)
