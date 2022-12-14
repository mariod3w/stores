# STORES BACKEND

Arrancar el proyecto localmente
==========

1 - Agregar el archivo `.env` con las variable de entorno.

2 - Para iniciar el proyecto con docker compose, correr las migraciones y crear el super usuario:

    $ docker-compose up -d
    $ docker ps
    $ docker exec -it <CONTAINER_WEB_ID> python manage.py migrate --settings=stores_backend.settings.prod
    $ docker exec -it <CONTAINER_WEB_ID> python manage.py createsuperuser --settings=stores_backend.settings.prod


Collección de Postman [POSTMAN](https://www.postman.com/mariod3w/workspace/prueba-tecnica-stores/collection/1086396-906b47bf-223c-4731-a644-af3b5c1e4b24?action=share&creator=1086396&ctx=documentation)