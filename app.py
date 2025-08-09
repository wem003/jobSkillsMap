from flask_app import create_app

# Call the app factory in flask_app/__init__.py
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
