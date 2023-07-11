Crypto data streaming test project using crypto compare API.

Notes:
- docker-compose build --no-cache (docker compose build --no-cache)
- docker-compose up
- http://localhost/status
- network: 
    - docker network create app-psql
    - docker network connect app-psql crypto_data_streaming-python-1
    - docker network connect app-psql crypto_data_streaming-pgsql-1
    - docker inspect app-psql
