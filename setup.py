import json
import os

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid19.settings")
os.environ.setdefault("ENV_FILE", ".env.dev")
django.setup()

BASE_URL = f'http://{os.getenv("DJANGO_ALLOWED_HOSTS")}:8000'

print("Setting Up all countries & statistics data")
print("------------------------------------------")

# Add Countries data
response = requests.post(f"{BASE_URL}/admin/add-countries")
if response.status_code == 200:
    print()
    print("All countries data added to the database successfully")
    print("------------------------------------")
    print()

# Add Statistics
dates = ['02-08-2022.json', '02-09-2022.json', '02-10-2022.json', '02-11-2022.json', '02-12-2022.json']

print("Statistics")
print("----------")
for d in dates:
    with open(f'data/{d}') as f:
        response = requests.post(url=f"{BASE_URL}/admin/add-statistics", json=json.load(f))
        if response.status_code == 200:
            print(f"{d} data added to the database successfully")
print()
print("Setup completed successfully!")
print(f"Open {BASE_URL} on your browser")
print()
