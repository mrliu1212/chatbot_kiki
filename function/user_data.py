import sqlite3

class UserData:
    """
    A class to manage user data, including plans, using SQLite database.

    Methods:
        show_plan(): Retrieves and returns the list of user plans.
        add_plan(desc, date): Adds a new plan to the user's list of plans.
        delete_plan(item): Deletes a plan from the user's list of plans.
        save_data(table_name, data): Saves data to the specified table in the database.
        check_name(name): Checks if a user with the specified name exists in the database.
        get_data(table, data): Retrieves data from the specified table in the database.
        delete_data(table, column, value): Deletes data from the specified table in the database.

    Example:
        user_data = UserData()
        user_data.check_name("John")
        user_data.add_plan("Study Python", "2023-01-01")
        plans = user_data.show_plan()
        print(plans)

    """

    def __init__(self) -> None:
        try:
            with sqlite3.connect('database/chatbot.db') as conn:
                self.conn = conn
        except sqlite3.Error as e:
            raise RuntimeError(f"Error connecting to the database: {e}")

        self.name = "User"
        self.user_id = None
        self.list_plan = []


    def show_user_info(self):
        try:
            data = ("UserID", self.user_id)
            user_info = self.get_data("Users",data)
            return user_info
        except:
            return False

    # plan
    def show_plan(self):
        """Retrieves and returns the list of user plans."""
        data = ("UserID", self.user_id)
        try:
            list_plan = self.get_data("Plans", data)
            return list_plan
        except Exception as e:
            return []

    def add_plan(self, desc, date):
        """Adds a new plan to the user's list of plans."""
        data = {
            "Description": desc,
            "Date": date,
            "UserID": self.user_id
        }
        if self.save_data("Plans", data):
            return True

    def delete_plan(self, item):
        """Deletes a plan from the user's list of plans."""
        try:
            data = ("PlanID", item[0])
            return self.delete_data("Plans", *data)
        except ValueError:
            return False


    # general utilities
    def save_data(self, table_name, data):
        """Saves data to the specified table in the database."""
        c = self.conn.cursor()

        keys = ",".join(data.keys())
        values = ",".join(["?" for _ in data.values()])

        sql_str = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"

        try:
            c.execute(sql_str, tuple(data.values()))

            if table_name == "Users":
                self.name = data['Name']
                self.user_id = c.lastrowid

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False
        finally:
            c.close()

    def check_name(self, name):
        """Checks if a user with the specified name exists in the database."""
        c = self.conn.cursor()

        sql = 'SELECT UserID FROM Users WHERE Name = ?'

        try:
            c.execute(sql, (name,))
            data = c.fetchone()

            if data:
                self.user_id = data[0]
                self.name = name
                return True
            return False
        except sqlite3.Error as e:
            return False
        finally:
            c.close()

    def get_data(self, table, data):
        """Retrieves data from the specified table in the database."""
        c = self.conn.cursor()

        sql = f'SELECT * FROM {table} WHERE {data[0]} = ?'

        try:
            c.execute(sql, (data[1],))
            result = c.fetchall()
            return result
        except sqlite3.Error as e:
            return None
        finally:
            c.close()

    def delete_data(self, table, column, value):
        """Deletes data from the specified table in the database."""
        c = self.conn.cursor()

        sql = f'DELETE FROM {table} WHERE {column} = ?'

        try:
            c.execute(sql, (value,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            return False
        finally:
            c.close()
