# Run project

## 1. Add a new IP on Ubuntu

To make the Docker project only start on a specific IP, we first add a new IP on the system's network card:
```bash
# set ip
sudo ip addr add 192.168.10.101/24 dev ens33

# see list of ip
ip a

# See specific ip 
ip a | grep 192.168.10.101

```


Add one important point to your documentation:

The `ip addr add` command temporarily adds the IP. 
This means that if the system is rebooted, this IP may be removed. To make the IP permanent, you need to change the Ubuntu network settings, such as Netplan.

## 2. Adding the IP address to the env File
go and open .env and chenge:
```dotenv
HOST_IP=192.168.10.101
```

## 3. Running Django commands inside Docker

After the containers are up, to run Django commands, we need to log in to the `web` service or run the commands inside the same service.

### Making migrations

If there are changes made to Django models, we use the following command to create migration files:
```bash
# paper migration
docker compose exec web python manage.py makemigrations

# add to database
docker compose exec web python manage.py migrate

# create super user
docker compose exec web python manage.py createsuperuser
```

### git
```commandline
git branch -M main
 
git remote add origin https://github.com/pedram-enayati-kashani/agahima.git

git push -u origin main
```

# Production mode

### change command in docker-compose.yml
your_project_name: Be sure to replace this with the actual name of the main Django projects folder.
```commandline
in:
command: python manage.py runserver 0.0.0.0:8000

to:
command: gunicorn --workers 3 --bind 0.0.0.0:8000 your_project_name.wsgi:application
```

### change DEBUG to False in setting.py
```python
in:
DEBUG=True

to:
DEBUG=False
```

## NPM
```commandline
npm run dev

npm run build
```

## Translate
```commandline
docker compose exec web python manage.py makemessages -l fa

docker compose exec web python manage.py compilemessages

```