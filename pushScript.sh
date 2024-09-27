#Push script to build the docker image and push it to docker.io
docker login -u "username" -p "password" docker.io

IMAGE=fvandaalen/grip3:test
docker build -t grip3 .

docker tag grip3 $IMAGE

docker push $IMAGE