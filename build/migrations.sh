python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py makemigrations app
python3 manage.py migrate app