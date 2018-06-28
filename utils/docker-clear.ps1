docker ps -aq | foreach {docker rm $_}
docker images -aq | foreach {docker rmi $_}