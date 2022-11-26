import os
from flask import Flask
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_mail import Mail

mail_obj = Mail()
# application factory
def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        #SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'switchfx.sqlite'),
    )
    #app.config.from_object('testconfig')
    app.config.from_pyfile('config.py')
    
    

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register the database function with the application
    from . import db
    db.init_app(app)

    #Register  Authentication Blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    #Register the mail sending Blue print
    from . import mail
    app.register_blueprint(mail.bp)
    #mail.mail_init(app)
    mail_obj.init_app(app)
   
    


    #Register Bootstrap5
    bootstrap = Bootstrap5(app)

    #Register the index page
    from . import forex
    app.register_blueprint(forex.bp)
    app.add_url_rule('/', endpoint='index')

  #  from . import admview
  #  app.register_blueprint(admview.bp)

       

    return app

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
