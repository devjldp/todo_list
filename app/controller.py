# import methods and objects from flask
from flask import render_template, redirect, url_for, request, session, flash

from config.database import get_db
from app.models import DatabaseOperations
from app import app


# create the routes
@app.route('/', methods = ["GET", "POST"])
def index():
    """
    Handle the landing page and user login process.
    For GET request, this function renders the login page.
    For POST request, it attempts to authenticate the user:
        if the user is administrator redirects to the administrator dashboard
        if the user is a employee redirects to the employee dashboard
    """
    if request.method == "POST":
        username_email = request.form.get("user") 
        password = request.form.get("password")

        if username_email.find('@') != -1: # check if joseiungo
            # invoke a function to retrieve the user from the database using the email
            user = DatabaseOperations.get_user_by_email(username_email, password)
        else:
            # invoke a function to retrieve the user from the database using the username
            user = DatabaseOperations.get_user_by_username(username_email, password)

        # check if the user retrieve from the database  != None -> create the session
        if user is not None:
            # Create the session 
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["is_admin"] = user[2]
            # redirect by role
            if session["is_admin"]:
                # if the user is admin
                return redirect("/admin_dashboard")
            return redirect("/user_dashboard")
        #if the user doesn't exist:
        #display a message
        flash("wrong credential. Try again!", "error")
        return redirect(url_for("index"))

    return render_template("index.html")


@app.route('/admin_dashboard', methods = ["GET", "POST"])
def admin_dashboard():
    """
    Admin Dasboard route
    This route handles the admin dashboard functionality. It allows an admin
    to view all users and register new users through a web form.

    Methods:
        GET:
            - Fetches all registered users and renders th 'admin_dashboard.html' template
        POST:
            - Receives form data for a new user: 'email', 'username', and 'password'.
            - Calls AdminOperations.register_new_user() to register the user.
            - Uses flash messages to indicate success or failure.
            - Redirects back to the dashboard to prevent form resubmission.

     Returns:
        - On GET: Rendered template 'admin_dashboard.html' with 'employees' context.
        - On POST: Redirect to 'admin_dashboard' route after processing form submission.
    """

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        result = DatabaseOperations.register_new_user(email, username, password)
        if result:
            flash("New user registered sucessfully", "success")
        else:
            flash("Oh Something goes wrong. Try Again!", "error")

        return redirect(url_for("admin_dashboard"))
    users = DatabaseOperations.get_all_users()
    return render_template("admin_dashboard.html", employees = users)



@app.route('/remove_user/<int:user_id>', methods=["GET", "POST"])
def remove_user(user_id):
    """
    Flask route to remove a user from the system by user ID.

    Args:
        user_id (int): The unique identifier of the user to be removed, passed as part of the URL.

    Returns:
        Response: A Flask redirect response to the admin dashboard page.
                  A flash message is included indicating whether the deletion was successful or failed.
    """
    print(f"The id is {user_id}")
    result = DatabaseOperations.remove_user(user_id)
    
    if result:
        flash("User removed sucessfully", "success")
    else:
        flash("Oh Something goes wrong. Try Again!", "error")

    return redirect(url_for("admin_dashboard"))


@app.route('/logout')
def logout():
    """
    log out the session and redirect to the index
    """
    session.clear() # Reset the session
    return redirect(url_for('index'))


@app.route('/user_dashboard', methods=["GET", "POST"])
def user_dashboard():
    return render_template("user_dashboard.html")








