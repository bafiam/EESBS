import os
import uuid
from appConfig import db
import click
import datetime
from flask.cli import with_appcontext
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from appConfig import initialize_app, db
from app.api.auth.models import User
from flask_cors import CORS
from app.api.auth.utils.validations import validate_password_format
eesbs_app = initialize_app(os.getenv('FLASK_ENV')or 'development')

CORS(eesbs_app)
# Import a module / component using its blueprint handler variable (mod_auth)
from app.api.auth.blueprint import mod_auth as auth_module
from app.api.profile.blueprint import mod_profile as profile_module

# Register blueprint(s)
eesbs_app.register_blueprint(auth_module)
eesbs_app.register_blueprint(profile_module)


#push an application context so as to perform database operations outside an application context
eesbs_app.app_context().push()
#instantiates the manager and migrate classes by passing the app instance to their respective constructors
manager = Manager(eesbs_app)
migrate = Migrate(eesbs_app, db)
manager.add_command('db', MigrateCommand)



@click.command("seed_admin")
@with_appcontext
def seed_admin():
    registered = datetime.datetime.now()
    admin_data = {
        "username": eesbs_app.config['SEED_ADMIN_USERNAME'],
        "password": eesbs_app.config['SEED_ADMIN_PASSWORD'],
        "email": eesbs_app.config['SEED_ADMIN_EMAIL'],
        "is_admin": True, 
        
        }
    check_admin_username= User.query.filter_by(email=admin_data['username']).first()
    if check_admin_username is None:
        check_admin_email=  user_email = User.query.filter_by(email=admin_data['email']).first()
        if check_admin_email is None:
            check_admin_password = validate_password_format(admin_data)
            if check_admin_password is None:
                verify_data=admin_data
                new_admin= User(
                public_id=str(uuid.uuid4()),
                username=verify_data['username'],
                password=verify_data['password'],
                email=verify_data['email'],
                is_admin=verify_data['is_admin'],
                registered_on=datetime.datetime.utcnow()
                )
                db.session.add(new_admin)
                db.session.commit()
                print("admin added")
            else:
                print(check_admin_password)
        else:
            print("Email already taken")
    else:
          print("Username already taken")
eesbs_app.cli.add_command(seed_admin)
