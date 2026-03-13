# import methods and objects from flask
from flask import render_template, redirect, url_for, request, session, flash

from datetime import datetime

from config.database import get_db
from app.models import DatabaseOperations, EmployeeOperations
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
            flash("New employee registered sucessfully", "success")
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
        flash("Employee removed sucessfully", "success")
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
    """
    Handles the user dashboard page.

    GET:
        - Retrieves the logged-in user's details from the database.
        - Formats the data and sends it to the template for display.

    POST:
        - Receives updated user information from the form.
        - Updates the user's details in the database.
        - Redirects back to the dashboard after the update.

    Raises:
        Exception: If the session has not been initialized.
    """
    # Handle form submission (update user information)
    if request.method == "POST":
        print("Receiving data form employee")   # Debuguing purpose
        employee_details = {
            "user_id": session["user_id"],
            "name" : request.form.get("name").lower(),
            "phone": request.form.get("phone").lower(),
            "date_birth": request.form.get("date_birth"),
            "address": request.form.get("address").lower(),
            "city": request.form.get("city").lower(),
            "role": request.form.get("role").lower()
        }

        print(f"Debugging - post method: {employee_details}")
        # Retrieve the date of birth string submitted from the form
        date_birth_str = employee_details.get("date_birth")
        # Check if the input is empty or consists only of whitespace
        if not date_birth_str or date_birth_str.strip() == "":
            employee_details["date_birth"] = None
        else:
            employee_details["date_birth"] = datetime.strptime(date_birth_str, "%Y-%m-%d").date()
                
        print(f"Debugging - post method transformation: {employee_details}")
        # Call the data layer to update the user details in the database
        result = EmployeeOperations.update_user_details(employee_details)

        if result:
            flash("Employee updated sucessfully", "success")
        else:
            flash("Oh Something goes wrong. Try Again!", "error")

        return redirect(url_for("user_dashboard"))
        
    # Retrieve user details from the database using the user_id stored in the session - GET method
    user = EmployeeOperations.get_user_details(session["user_id"])
        
    print(user)
    # Initialize dictionary to store formatted employee details

    employee_details = {
        "user_id": user[0],
        "name": user[1].capitalize() if user[1] else None,
        "phone": user[2].capitalize() if user[2] else None,
        "date_birth": user[3],  # esto es un objeto date
        "date_birth_str": user[3].strftime("%Y-%m-%d") if user[3] else None, 
        "address": user[4].capitalize() if user[4] else None,
        "city": user[5].capitalize() if user[5] else None,
        "role": user[6].capitalize() if user[6] else None
    }

    print(employee_details)

    counter = 0

    # # Populate the employee_details dictionary with values from the database to show the intiial form

    for key in employee_details.keys():
        if key == "date_birth_str":
            continue
        print(key)
        if user[counter] == None:
            employee_details[key] = key.capitalize()
            counter += 1
            continue
        if isinstance(user[counter], str):
            employee_details[key] = user[counter].capitalize()
            counter += 1
            continue
        employee_details[key] = user[counter]
        counter += 1
    
    # Render the dashboard template with the employee data
    return render_template("user_dashboard.html", employee = employee_details)






