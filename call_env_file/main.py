import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
my_variable = os.getenv('MY_VARIABLE')
other_variable = os.getenv('OTHER_VARIABLE')

# Use the variables in your code
print(my_variable)
print(other_variable)

