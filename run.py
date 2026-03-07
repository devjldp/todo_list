# Entry point to the application

from app import app

if __name__ == "__main__":
    # debug = true only for development phase -> You can see errors with more detail
    app.run(debug=True)