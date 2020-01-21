# How to use Flask-Login in Flask?
  1. Make sure you have `SECRET_KEY` in your `.env` file
      - Flask-Login uses sessions for authentication, secret key is used to encrypting the cookies in session, the user could look at the contents of cookie but not modify it, unless they know the secret key used for signing.
  1. Initializing Flask-Login in your `app.py` or `__init__.py`
      - A user loader tells Flask-Login how to get a specific user object from the ID that is stored in the session cookie
      ```py
        from flask_login import LoginManager
        from models.user import User

        login_manager = LoginManager()
        login_manager.init_app(app)
        
        @login_manager.user_loader
        def load_user(user_id):
          return User.get_by_id(user_id) # get id from session,then retrieve user object from database with peewee query
       ``` 
  1. Optional (Customizing the Login Process) => https://flask-login.readthedocs.io/en/latest/#customizing-the-login-process
      - if a user try to access route with `@login_required` decorator without logged in:
        - Line 1 : redirect user to "sessions.new" 
        - Line 2 : flash message 
        - Line 3 : declare the flash message category
      ```py
        login_manager.login_view = "sessions.new" 
        login_manager.login_message = "Please log in before proceeding"
        login_manager.login_message_category = "warning"
        ```
  1. Add the login_user function to create the session in `instagram_web/blueprints/sessions/views.py`. 
      ```py
        from flask_login import login_user
        from models.user import User
        from werkzeug.security import check_password_hash

        @sessions_blueprint.route('/', methods=['POST'])
        def create():
          user = User.get_or_none(User.email==request.form.get('email'))
          if user:
            if check_password_hash(user.password, request.form.get('password')) :
              login_user(user) # store user id in session
              return redirect(url_for('users.show')) # redirect to profile page
            else:
              # password not matched
          else:
            # no user found in database
       ``` 
  1. Use the logout_user function for logging out in `instagram_web/blueprints/sessions/views.py`.
      - have login_required decorator because it doesn't make sense to logout a user who isn't logged in to begin with
      ```py
        from flask_login import logout_user, login_required

        @sessions_blueprint.route('/delete')
        @login_required
        def destroy():
            logout_user()
            return redirect(url_for('sessions.new'))
       ``` 
  1. Adding `UserMixin` class to our User model in `models/user.py`.
      - The UserMixin will provide `is_authenticated`, `is_active`, `is_anonymous` and `get_id()` properties and methods to our model so Flask-Login will be able to work with it
      ```py
        from flask_login import UserMixin

        class User(UserMixin, BaseModel):
          username = pw.CharField(unique=False)
          password = pw.CharField()
          email = pw.CharField(unique=True)
       ``` 
  1. Use `current_user` in jinja template and `views.py`.
      - Access the logged-in user with the `current_user` proxy, which is available in every template.
      - For example, you can use it in your `templates/_navbar.html` as below:

      ```jinja

        {% if current_user.is_authenticated %}
          <li>
            <a href="{{ url_for('sessions.destroy')}}">Sign Out</a>
          </li>
        {% else %}
          <li>
            <a href="{{ url_for('sessions.new')}}">Sign In</a>
          </li>
          <li>
            <a href="{{ url_for('users.new')}}">Sign Up</a>
          </li>
        {% endif %}
      ```
      - OR, use it in your `instagram_web/blueprints/users/views.py` as below:
      ```py
        from flask_login import current_user

        @users_blueprint.route('/<id>/edit', methods=["GET"])
        def edit(id):
          user = User.get_or_none(User.username == username)
          if current_user.role == "admin" or current_user.id == user.id:
            return render_template("users/edit.html", user=user)
          else:
            # flash error message
       ``` 

      
