from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "users",
}

# Connect to MySQL database
def connect_to_mysql():
    try:
        print("Connecting to MySQL database...")
        connection = mysql.connector.connect(**db_config)
        print("Connected to MySQL database successfully!")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None

# Sample data for demonstration purposes
users_data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "Admin"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "User"},
]

# Route to display "Hello, World!"
@app.route('/hello')
def hello_world():
    return "Hello, World!"

# Route to display a list of users in an HTML table
@app.route('/users')
def show_users():
    try:
        conn = connect_to_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            print(users)
            conn.close()
            return render_template('users.html', users=users)
        else:
            return "Failed to connect to the database."
    except Exception as e:
        return str(e)

# Route to render a page to accept input for a new user and store in the database
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')

        if not name or not email or not role:
            return "Please provide all user details."

        try:
            conn = connect_to_mysql()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email, role) VALUES (%s, %s, %s);", (name, email, role))
                conn.commit()
                conn.close()
                return redirect(url_for('show_users'))
            else:
                return "Failed to connect to the database."
        except Exception as e:
            return str(e)

    return render_template('new_user.html')

# Route to retrieve a specific user's details from the database
@app.route('/users/<int:user_id>')
def get_user(user_id):
    try:
        conn = connect_to_mysql()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user = cursor.fetchone()
            print(user)
            conn.close()

            if user:
                return render_template('id.html', user=user)
            else:
                return "User not found", 404
        else:
            return "Failed to connect to the database."
    except Exception as e:
        return str(e)

# Error handling for 404 Not Found errors
@app.errorhandler(404)
def not_found_error(error):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5004)
