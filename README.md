# PetStore App

## About Project


### Structure
```
    /docker 
        /api -- Storage with all different version of api
            DockerFile -- DockerFile with current version of api
    /src
        /app
        - schemes.py -- Message Scheme for error log
        - server.py -- Init of FastAPI
            /routers
            - pet.py - -- All routers of service pet
            - store.py -- ALl routers of service store
            - users.py -- All routers of service users
            /services
                /pet
                - logic.py -- database logic 
                - models.py  -- models of database
                - schemes.py  -- pydantic schemes
                /store
                - logic.py -- database logic 
                - models.py  -- models of database
                - schemes.py  -- pydantic schemes
                /user
                - logic.py -- database logic 
                - models.py  -- models of database
                - schemes.py  -- pydantic schemes
        /core
            /cache
            - backend.py -- Main backend for caching, use ujson insted of json(much faster)
            - cache.py -- Cache logic(Manager)
            - key_marker.py -- Custom Key Maker for making prefix for caching
            - redis.py -- Import of redis(Aioredis -- asyncio)
            /db
            - session.py -- Init of database
            /excpetions
            - base.py -- Base excpetions for all services
            - pet.py -- Exceptions of service pet
            - server.py -- Exceptions of Server
            - store.py -- Exceptions of service store
            - user.py -- Exceptions of service user
            /middlewares
            - authentication.py -- Authentication middleware for user, 
            it takes request and check if user loged if True it returs pydantic scheme of user
            /repository
            - base.py -- Base CRUD for all services
            - auth.py -- AuthHandler for auth user
            - config.py -- Init of config: db_url,test_db,dsn, etc..
            - schemes.py -- Scheme of current user(needs for middlewares)
        /migrations
            /versions
            - alembic_helper.py -- Import all models of database
            - env.py -- Settings of alembic
        /resources
        -  strings.py -- Messages for error
    /tests
        - conftest.py -- 
        /performance
        - test_performance.py -- 
        /pet
        - test_pet.py -- 
        /store
        - test_store.py -- 
        /user
        - test_email.py -- 
        - test_phone.py -- 
        - test_user.py -- 
    pre-commig.config.yaml -- 
    docker-compose.yml -
     
```     

## How to run project

### Docker
```
docker-compose up --build
docker exec (name of web service) alembic upgrade head
```

### Windows
```
 virtualenv myenv
 myenv\Scripts\activate
 pip3 install pipenv
 pipenv install
 cd src
 uvicorn app.server:app
```


### Linux
```
python3 -m venv venv 
source venv/bin/activate
pip3 install pipenv
pipenv install
cd src
uvicorn app.server:app
```
