# Creating db network
docker network create --gateway 172.30.0.12 --subnet 172.30.0.11/24 my-net
# Building and running postgres db and pgadmin4 containers
docker-compose build && docker-compose up
# Building and running dockerized app
docker build -t homework:1 . && docker run -t homework:1