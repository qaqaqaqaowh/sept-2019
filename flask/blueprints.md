# How to work with Blueprints in Flask?
### 1. Create a new blueprint in your `views.py`   
  1. Provide the name of the blueprint (as a string), `__name__` (name of the file), and `templates_folder`
  1. Inside `instagram_web/blueprints/images/views.py`
      ```py
        from flask import Blueprint


        images_blueprint = Blueprint(
          # name of the blueprint
          'images',
          __name__,
          template_folder='templates'
        )
       ``` 
    
    
### 2. Register your blueprint in app
  1. In our case, we register it in`instagram_web/__init__.py`
  1. Remember to import it from the corresponding file
  1. Give it a URL prefix
  1. Inside `instagram_web/__init__.py` 
      ```py
      from flask import register_blueprint
      from instagram_web.blueprints.images.views import images_blueprint 


      app.register_blueprint(images_blueprint, url_prefix='/images')
      ```

  1. Why do we need to specify the URL prefix?
        - This allows us to attach the same path before all the routes inside the blueprint
          - e.g., All the `'/new'`, `/delete`, `/edit` routes in the `images_blueprint` will become `images/new`, `images/delete`, `images/edit`
