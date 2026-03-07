from config.database import get_db, close_db

class DatabaseOperations:

    @staticmethod
    def get_user_by_username(username, password):
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
            print(e)

    @staticmethod
    def get_user_by_email(email, password):
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
            print(e)