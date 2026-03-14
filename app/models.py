from config.database import get_db, close_db
# import dattime class to work wit dates:
from datetime import datetime

class DatabaseOperations:

    @staticmethod
    def get_user_by_username(username, password):
        """
        Gets a user from the table users.
        Args:
            username (str): the username chosen by the user.
            password (str): the password for the user account.

        Returns:
            user (tuple): the user details from table users.
            None: if the database cursor not be created or any incident with database operation.
        
        Raises:
            Exception: any database-related execption encountered during execution is caught internally and handled by rolling back the transaction.
        """

        try:
            # create the connection object
            conn = get_db()

            # create the cursor
            cursor = conn.cursor()

            # check if the cursosr exist:
            if cursor is None:
                return None
            
            # write the query
            query = "select user_id, user_name, is_admin from users where user_name = %s and password = %s"
            #execute the query
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            close_db()
            return user # -> (user_id, user_name, is_admin ) -> 10	"test_admin"	true
        except Exception as e:
            print(f"Error retrieving a user: {e}")
            return None

    @staticmethod
    def get_user_by_email(email, password):
        """
        Gets a user from the table users.
        Args:
            email (str): the users email.
            password (str): the password for the user account.

        Returns:
            user (tuple): the user details from table users.
            None: if the database cursor not be created or any incident with database operation.
        
        Raises:
            Exception: any database-related execption encountered during execution is caught internally and handled by rolling back the transaction.
        """
        try:
            # create the connection object
            conn = get_db()

            # create the cursor
            cursor = conn.cursor()

            # check if the cursosr exist:
            if cursor is None:
                return None
            
            # write the query
            query = "select user_id, user_name, is_admin from users where email = %s and password = %s"
            #execute the query
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            close_db()
            return user
        except Exception as e:
            print(f"Error retrieving a user: {e}")
            return None

    @staticmethod
    def register_new_user(email, username, password):
        """
        Registers a new user in the database, table users.
        Args:
            email (str): The email address of the user.
            username (str): the username chosen by the user.
            password (str): the password for the user account.

        Returns:
            bool:
                True if the user (employee) was succesfully registered.
                False if the registration failed due to an error.
                None if the database cursor not be created.
        
        Raises:
            Exception: any database-related execption encountered during execution is caught internally and handled by rolling back the transaction.
        """
        try:
            # Open connection with database
            conn = get_db()

            cursor = conn.cursor()
            # Check if the cursor is None
            if cursor is None:
                return None

            query = "insert into users (email, user_name, password) values(%s,%s,%s) returning user_id;"

            cursor.execute(query, (email, username, password))
            
            
            id = cursor.fetchone()[0] # Get the id from the registered that we have just inserted
            print(f"Id returned: {id}")


            query = "insert into user_details (user_id) values (%s);"
            cursor.execute(query, (id, ))
            
            # commit to save changes permanently in the database 
            conn.commit()

            # Debugging purpose:
            print("user registered succesfully")
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error: Registration Failed. {e}")
            return False
        finally:
            # Always clean up resources
            if cursor:
                cursor.close()
            close_db()

    @staticmethod
    def get_all_users():
        """
        Retrieves all non-admin users from the database.

        Args:
            None
        
        Returns:
            List: List of tuples if the users exist.
            None: If the cursor couldn't be created, and error occurs or no users are found.        
        Raises:
            Exception: Any database-related exception encountered internally.
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            # Check if the cursor is None
            if cursor is None:
                return None

            query = "select user_id, user_name, email from users where is_admin = false;"

            cursor.execute(query)

            users = cursor.fetchall()

            if users is None:
                return None
            return users
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            # Always clean up resources
            if cursor:
                cursor.close()
            close_db()

    @staticmethod
    def remove_user(user_id):
        """
            Removes a user from the database by their user ID.
            Args:
                user_id (int): The unique identifier of the user to be removed.
            Returns:
                    True if the user was successfully removed.
                    False if the deletion failed due to an error.
                    None if the database cursor could not be created.

            Raises:
                Exception: Any database-related exception encountered is caught internally, triggering a rollback and returning False.
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            # Check if the cursor is None
            if cursor is None:
                return None

            query = "delete from users where user_id = %s;"

            #  must be a tuple  -> tis is the reason for (user_id, )    
            cursor.execute(query, (user_id,))

            # commit to save changes permanently in the database 
            conn.commit()
            # Debugging purpose:
            print("user removed succesfully")
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error: Deletion Failed. {e}")
            return False
        finally:
            # Always clean up resources
            if cursor:
                cursor.close()
            close_db()

    # @staticmethod
    # def get_user_by_id(user_id): This method is not used
    #     try:
    #         # create the connection object
    #         conn = get_db()

    #         # create the cursor
    #         cursor = conn.cursor()

    #         # check if the cursosr exist:
    #         if cursor is None:
    #             return None
            
    #         # write the query
    #         query = "select user_id, user_name, email from users where user_name = %s and password = %s"
    #         #execute the query
    #         cursor.execute(query, (username, password))
    #         user = cursor.fetchone()
    #         cursor.close()
    #         close_db()
    #         return user # -> (user_id, user_name, is_admin ) -> 10	"test_admin"	true
    #     except Exception as e:
    #         print(e)



class EmployeeOperations:
    def get_user_details(id):
        """
        Gets user details from the table user_details

        Args:
            id (int): the employee id got form the session.

        Returns:
            user (tuple): A tuple with employee information.
            None: If the cursor couldn't be created, and error occurs or no users are found.
        
        Raises:
            Exception: Any database-related exception encountered internally.
        """
        
        try:
            conn = get_db()

            # create the cursor
            cursor = conn.cursor()

            # check if the cursosr exist:
            if cursor is None:
                return None 
            
            query = "select user_id, name, phone, date_birth, address, city, role from user_details where user_id = %s;" 

            cursor.execute(query, (id ,)) 

            user = cursor.fetchone() # retrieve only one row

            return user
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            close_db()

    def update_user_details(employee_details):
        """
        Updates user details into the table user_details

        Args:
            employee_details (dict): the employee info retrieved from the form.

        Returns:
            True (bool): If the update operation is successful.
            False (bool): If there is some problem with the database.
            None: If the cursor couldn't be created.
        
        Raises:
            Exception: Any database-related exception encountered internally.
        """
        try:
            conn = get_db()

            # create the cursor
            cursor = conn.cursor()

            # check if the cursosr exist:
            if cursor is None:
                return None 
            
            print("cursor exist") # Debugging purpose
            query = "update user_details set name = %s, phone = %s, date_birth = %s, address = %s, city = %s, role = %s where user_id = %s;" 
            
            print(f"debugging: {query}") # Debugging purpose

            # Manage input date

            print(f"debugging type: {type(employee_details.get('date_birth'))}")
            # Debugging purpose
            # print(type(employee_details.get("date_birth")) is not 'NoneType')
            
            if employee_details.get("date_birth") is None: 
                date_birth_str = ""
            else:
                date_birth_str = employee_details.get("date_birth").strftime("%Y-%m-%d")
              
            # Debugging purpose
            print(f"debugging - date : {date_birth_str}")
            print(f"debugging type: {type(date_birth_str)}")

            if not date_birth_str or date_birth_str == "":
                employee_details["date_birth"] = None
            else:
                employee_details["date_birth"] = datetime.strptime(date_birth_str, "%Y-%m-%d").date()

            print(f"Debugging: Before updating - {employee_details}") # Debugging purpose
            cursor.execute(query, (employee_details["name"], employee_details["phone"], employee_details["date_birth"], employee_details["address"], employee_details["city"], employee_details["role"], employee_details["user_id"] ,)) 

            print("user updated")
            # commit to save changes permanently in the database 
            conn.commit()
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error updating a user: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            close_db()

class TaskOperations:
    @staticmethod
    def insert_new_task(task, employee_id):
        """
        Registers a new task in the database, table tasks.
        Args:
            task (dict): The task information got from the form.
            employee_id (int): The employee id got form the session.

        Returns:
            True: if the task associated to the user (employee) was succesfully created.
            False: if the task creation failed due to an error.
            None: if the database cursor not be created.
        
        Raises:
            Exception: any database-related execption encountered during execution is caught internally and handled by rolling back the transaction.
        """

        try:
            print(f"Task: {task}") 
            print(f"ID: {employee_id}") 
            print(f"data type of dead line: {type(task['deadline'])}")
            conn = get_db()

            cursor = conn.cursor()

            if cursor is None:
                return None
            
            if not employee_id:
                raise ValueError("Session Id for employee is missing")
                return None

            query = "insert into tasks (title, description, deadline, user_id) values (%s, %s, %s, %s);"

            print(query)

            
            cursor.execute(query,(task["title"], task["description"], datetime.strptime(task["deadline"], "%Y-%m-%d").date() , employee_id,))

            conn.commit()
            return True
        except ValueError as e:
            if conn:
                conn.rollback()
            print(f"Error Value error: {e}")
            return False
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error creating a new task: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            close_db()



