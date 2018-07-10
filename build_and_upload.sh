aws ecr get-login --no-include-email --region eu-west-3 > authDockerAws.sh
sh authDockerAws.sh
docker build --no-cache -t budgetkeeper-api .
docker tag budgetkeeper-api:latest 989665778089.dkr.ecr.eu-west-3.amazonaws.com/budgetkeeper-api:latest
docker push 989665778089.dkr.ecr.eu-west-3.amazonaws.com/budgetkeeper-api:latest
rm authDockerAws.sh