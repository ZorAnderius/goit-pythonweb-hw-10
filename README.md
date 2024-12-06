# Contacts App - Python Web Application

## Installation

## 1. Clone the repository

```bash
    git clone https://github.com/ZorAnderius/goit-pythonweb-hw-08.git
    cd goit-pythonweb-hw-08
```

## 2. Add environment variables

```bash
    POSTGRES_USER=<YOUR_USERNAME>
    POSTGRES_PASSWORD=<YOUR_PASSWORD>
    POSTGRES_DB=<YOUR_DB_NAME>
```

## 3. Run the application

```bash
   docker-compose up
```

## 4. Open the browser and go to http://localhost:8000


## 5. Swagger documentation: http://localhost:8000/docs

## 6. Add new migration

```bash
    docker exec -it contacts-app alembic revision --autogenerate -m 'Add new migration'
    alembic upgrade head
```





