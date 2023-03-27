import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print(os.getenv('YARA'))
print(os.getenv('THIRDGEN'))

# Load the environment variable and parse the JSON string to a dictionary
my_dict_from_env = json.loads(os.environ.get('MY_DICT', '{}'))
print(my_dict_from_env)
print(my_dict_from_env['nested_dict']['key3'])
