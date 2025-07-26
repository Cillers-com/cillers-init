# Cillers Init Docker Image

This directory contains the Docker configuration for the Cillers Init application, which handles initialization operations for Couchbase and Redpanda services.

## Building the Docker Image

To build the Docker image, run the following command from this directory:

```bash
docker build -t cillers-init:latest .
```

## Complete Workflow: Build and Upload to GCP

Here's the complete step-by-step process:

1. **Build the image first** (required before tagging):
   ```bash
   docker build -t cillers-init:latest .
   ```

2. **Tag for GCP** (replace YOUR_PROJECT_ID with your actual project ID):
   ```bash
   docker tag cillers-init:latest us-central1-docker.pkg.dev/YOUR_PROJECT_ID/cillers-repo/cillers-init:latest
   ```

3. **Push to GCP**:
   ```bash
   docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/cillers-repo/cillers-init:latest
   ```

## Uploading to Google Cloud Platform

### Prerequisites

1. Install and configure the Google Cloud CLI:
   ```bash
   # Install gcloud CLI (if not already installed)
   # Follow instructions at: https://cloud.google.com/sdk/docs/install
   
   # Authenticate with your GCP account
   gcloud auth login
   
   # Set your project ID
   gcloud config set project YOUR_PROJECT_ID
   ```

2. Configure Docker to use gcloud as a credential helper:
   ```bash
   gcloud auth configure-docker
   ```

### Artifact Registry

First, create an Artifact Registry repository (if not already created):

```bash
# Create repository (one-time setup)
gcloud artifacts repositories create cillers-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Cillers Docker images"

# Configure Docker for Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Then build, tag, and push:

```bash
# Tag the image for Artifact Registry
docker tag cillers-init:latest us-central1-docker.pkg.dev/YOUR_PROJECT_ID/cillers-repo/cillers-init:latest

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/cillers-repo/cillers-init:latest
```

### Making the Image Public

To allow others to pull the image without authentication:

**For GCR:**
```bash
gsutil iam ch allUsers:objectViewer gs://artifacts.YOUR_PROJECT_ID.appspot.com
```

**For Artifact Registry:**
```bash
gcloud artifacts repositories add-iam-policy-binding cillers-repo \
    --location=us-central1 \
    --member=allUsers \
    --role=roles/artifactregistry.reader
```

### Using the Published Image

Others can then use your published image:

**From GCR:**
```bash
docker pull gcr.io/YOUR_PROJECT_ID/cillers-init:latest
```

**From Artifact Registry:**
```bash
docker pull us-central1-docker.pkg.dev/YOUR_PROJECT_ID/cillers-repo/cillers-init:latest
```

## Running the Container

### Using Docker Run

```bash
docker run --rm \
  -e ENVIRONMENT=development \
  -e INIT_SERVICES=couchbase,redpanda \
  -v $(pwd)/../../conf/init:/conf/init:ro \
  cillers-init:latest
```

### Using Docker Compose

```bash
# Set environment variables (optional, defaults are provided)
export ENVIRONMENT=development
export INIT_SERVICES=couchbase,redpanda

# Run with docker-compose
docker-compose up --build
```

## Environment Variables

- `ENVIRONMENT` (required): The environment to run in (must be defined in `/conf/init/env.yaml`)
- `INIT_SERVICES` (optional): Comma-separated list of services to initialize (default: `couchbase,redpanda`)

## Volume Mounts

The container expects the configuration directory to be mounted at `/conf/init`. This should contain:

- `env.yaml`: Environment configuration
- `couchbase.yaml`: Couchbase configuration
- `redpanda.yaml`: Redpanda configuration

## Application Structure

- `src/main.py`: Main entry point
- `src/config.py`: Configuration management
- `src/controllers/`: Service-specific controllers
- `bin/run`: Application startup script
- `requirements.txt`: Python dependencies

## Dependencies

The application requires:
- PyYAML==6.0.1
- couchbase==4.3.2
- kafka-python

## Notes

- The container runs as root by default
- Configuration files are mounted read-only
- The application will exit after completing all operations
- Use `restart: unless-stopped` in docker-compose for automatic restarts
