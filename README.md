# Create a file .env from env_sample

# Building docker image
docker build --tag tds-calculator_web:1.0.0 -t tds-calculator_web:latest .

# Running docker image
docker-compose up -d --build

# Shutting down docker image
docker-compose down

# Pulling the latest image
docker-compose pull

# Pushing the latest image
docker tag tds-calculator_web:1.0.0 us-west1-docker.pkg.dev/binocs-staging/partner-services-repo/tds-calculator_web:1.0.0
gcloud auth login
docker push us-west1-docker.pkg.dev/binocs-staging/partner-services-repo/tds-calculator_web:1.0.0
