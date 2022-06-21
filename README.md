# Building docker image
docker build --tag tds-calculator_web:1.0.0 -t tds-calculator_web:latest .

# Running docker image
docker-compose up -d --build

# Shutting down docker image
docker-compose down
