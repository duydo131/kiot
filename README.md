# Django REST API Kiot Management

## How To Run

### 1. Update env in docker-compose file

```
update env for connect to your database
```

### 2. Build Dọcker
```
docker-compose build
```

### 3. Run redis, api from docker-compose
```
docker-compose up
```

Server will run at localhost and listen on port 8000


### 4. Run worker, beat celery
```
python -m celery -A config beat
python -m celery -A config worker
```
