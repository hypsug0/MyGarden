#!/bin/bash

echo ""
echo "My garden init_____________________________________________"
echo ""


export POSTGRES_HOST=${POSTGRES_HOST:-db}
export POSTGRES_DB=${POSTGRES_DB:-mygarden}
export POSTGRES_PORT=${POSTGRES_PORT:-5432}


shopt -s dotglob nullglob


until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT; do
    echo "Awaiting Database container on ${POSTGRES_HOST}:${POSTGRES_PORT}"
    sleep 1
done
sleep 2

PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -h $POSTGRES_HOST -p $POSTGRES_PORT -c 'create extension postgis_raster;'

cd /app

echo "************ Init database ****************"

python3 -m manage migrate
echo "dbChiro Database ready"

# python3 -m manage collectstatic --noinput
# echo "Static files collected"


# echo "************** Create dbChiro SU ******************"

# script="
# from django.conf import settings;

# username = '$APP_SU_USERNAME';
# password = '$APP_SU_PASSWORD';
# email = '$APP_SU_EMAIL';

# role_model = settings.AUTH_USER_MODEL

# if role_model.objects.filter(is_superuser=True).count()==0:
#     superuser=role_model.objects.create_user(username, email, password);
#     superuser.is_superuser=True;
#     superuser.is_staff=True;
#     superuser.save();
#     print(f'{superuser} created');
# else:
#     print('One or more Superuser already exists, creation skipped.')
# "
# printf "$script" | python3 manage.py shell

echo "************** Populate with initial data ***************"
echo "load dicts data"
python3 -m manage loaddata plantintos/fixtures/{conditions,hardiness_zones,operations}.xml.gz
echo "dicts data loaded"

echo "************ Start Gunicorn ***************"
cd /app
# if [ $DEV = true ]
# then
echo "Starting dev mode"
python -m manage runserver 0.0.0.0:8000
# else
#     echo "Starting prod mode"
#     gunicorn -b 0.0.0.0:8000 -t ${GUNICORN_TIMEOUT:-180} dbchiro.wsgi
# fi
