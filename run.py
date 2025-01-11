import argparse
from waitress import serve
from app import app, db

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wishlist app")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port on which the app should run"
    )
    parser.add_argument("--prod", action="store_true", help="Run in production mode")
    args = parser.parse_args()

    with app.app_context():
        db.create_all()

    if args.prod:
        serve(app, host="0.0.0.0", port=args.port)
    else:
        # flask debug server
        app.run(debug=True, port=args.port)
