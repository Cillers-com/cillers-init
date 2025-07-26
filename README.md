# Cillers Init

A distributed systems initialization tool developed and maintained by **Cillers AB**. This tool automates the setup and configuration of distributed infrastructure components across different environments.

## Overview

Cillers Init provides automated initialization and configuration management for:

- **Redpanda**: High-performance streaming platform (Kafka-compatible)
- **Couchbase**: Distributed NoSQL document database

The tool supports multiple environments with hierarchical configuration management, allowing you to maintain consistent baseline configurations while customizing settings for specific environments.

## Key Features

- **Multi-Environment Support**: Configure different settings for development, staging, production, and custom environments
- **Hierarchical Configuration**: Global defaults → component defaults → environment-specific overrides
- **Automated Resource Creation**: Automatically creates topics, buckets, scopes, and collections based on configuration
- **Environment Validation**: Prevents deployments to undefined environments
- **Retry Logic**: Built-in retry mechanisms for reliable initialization
- **Docker Ready**: Containerized for easy deployment in any environment

## Quick Start

### Using Docker

```bash
# Pull the latest image
docker pull cillers/init:latest

# Run with your configuration
docker run --rm \
  -e ENVIRONMENT=development \
  -e INIT_SERVICES=couchbase,redpanda \
  -v /path/to/your/config:/conf/init:ro \
  cillers/init:latest
```

### Using Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  cillers-init:
    image: cillers/init:latest
    environment:
      - ENVIRONMENT=development
      - INIT_SERVICES=couchbase,redpanda
    volumes:
      - ./conf:/conf/init:ro
    depends_on:
      - couchbase
      - redpanda
```

Then run:

```bash
docker-compose up cillers-init
```

## Configuration

The tool requires a configuration directory mounted at `/conf/init` containing:

- **`env.yaml`**: Environment definitions and validation
- **`couchbase.yaml`**: Couchbase bucket, scope, and collection configurations
- **`redpanda.yaml`**: Redpanda topic configurations

### Example Configuration Structure

```
conf/init/
├── env.yaml           # Environment registry
├── couchbase.yaml     # Couchbase configuration
└── redpanda.yaml      # Redpanda configuration
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Target environment (must exist in env.yaml) | - | Yes |
| `INIT_SERVICES` | Comma-separated services to initialize | `couchbase,redpanda` | No |
| `COUCHBASE_HOST` | Couchbase server hostname | `couchbase` | No |
| `COUCHBASE_USERNAME` | Couchbase admin username | `admin` | No |
| `COUCHBASE_PASSWORD` | Couchbase admin password | `password` | No |
| `REDPANDA_HOST` | Redpanda broker hostname | `redpanda` | No |
| `REDPANDA_PORT` | Redpanda broker port | `9092` | No |

## Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[Environment Configuration](docs/environment-configuration.md)**: Complete guide to env.yaml configuration
- **[Redpanda Documentation](docs/redpanda.md)**: Topic configuration and management
- **[Couchbase Documentation](docs/couchbase.md)**: Bucket, scope, and collection management

## Use Cases

### Development Environment Setup
Quickly initialize development environments with minimal resource allocation:
```bash
docker run --rm \
  -e ENVIRONMENT=development \
  -v ./conf:/conf/init:ro \
  cillers/init:latest
```

### Production Deployment
Initialize production environments with high-availability configurations:
```bash
docker run --rm \
  -e ENVIRONMENT=production \
  -v ./conf:/conf/init:ro \
  cillers/init:latest
```

### CI/CD Integration
Integrate into your deployment pipeline:
```yaml
# Kubernetes Job example
apiVersion: batch/v1
kind: Job
metadata:
  name: cillers-init
spec:
  template:
    spec:
      containers:
      - name: init
        image: cillers/init:latest
        env:
        - name: ENVIRONMENT
          value: "staging"
        volumeMounts:
        - name: config
          mountPath: /conf/init
      restartPolicy: OnFailure
```

## How It Works

1. **Environment Validation**: Validates the specified environment against env.yaml
2. **Configuration Loading**: Loads component-specific configuration files
3. **Resource Creation**: Creates missing resources (topics, buckets, etc.)
4. **Settings Application**: Applies environment-specific settings
5. **Verification**: Verifies successful resource creation

## Best Practices

- **Start Simple**: Begin with basic configurations and add complexity as needed
- **Environment Separation**: Use different configurations for each environment
- **Version Control**: Keep configuration files in version control
- **Testing**: Test configurations in development before production deployment
- **Monitoring**: Monitor resource usage and adjust quotas accordingly

## Support

For issues, questions, or contributions, please contact Cillers AB or refer to the comprehensive documentation in the `docs/` directory.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

**Developed and maintained by Cillers AB**
