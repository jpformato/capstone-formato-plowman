# capstone-formato-plowman

## Installations
pip install django psycopg2 </br>
pip install coverage </br>

## Running The Program
In \src\App\website enter: </br>
python manage.py runserver </br>
Then go to your browser and go to: localhost:8000

## Database
To have a database with the same tables, download postgresql, and start pgadmin4. When downloading you will have to make a password.
In \src\App\website\website create a file named secrets.py with these variables: </br>
DB_NAME = \**your db name*\* </br>
DB_USER = "postgres" </br>
DB_PASSWORD = \**your password*\* </br>
DB_HOST = "localhost" </br>
DB_PORT = \**port postgres is using*\* </br>
</br>
Then in \src\App\website enter: </br>
python manage.py makemigrations </br>
python manage.py migrate

## Testing
To generate the coverage report enter this command in \src\App\website: </br>
coverage run manage.py test </br>

To view the coverage report enter this command in the same directory: </br>
coverage -m report </br>

An image of the coverage report for each sprint will also be uploaded to the docs folder.