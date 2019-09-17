
# Define the application directory
import os

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')

# Secret key for signing cookies
SECRET_KEY = os.getenv('SECRET_KEY')