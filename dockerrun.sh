docker stop $(docker ps -a -q  --filter ancestor=sigmaxm)
docker build -t sigmaxm:latest .
docker run -d -p 5002:5002 sigmaxm
