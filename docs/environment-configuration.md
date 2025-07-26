# Environment Configuration Documentation

## Overview

The Cillers Init system uses an `env.yaml` file to define and validate the available environments for deployment. This file serves as the central registry for all supported environments and ensures that only valid environments are used during initialization.

## What the env.yaml File Does

The environment configuration file:

- **Environment Validation**: Defines which environments are valid for the system
- **Deployment Control**: Prevents accidental deployments to undefined environments
- **Environment Registry**: Serves as a central list of all supported deployment targets
- **Configuration Consistency**: Ensures all components use the same environment definitions

## File Location

The `env.yaml` file should be located in the configuration directory:
```
/conf/init/env.yaml
```

## Configuration Format

The `env.yaml` file uses a simple YAML structure with an `environments` array listing all valid environment names.

### Basic Structure

```yaml
environments:
  - development
  - staging
  - production
```

### Extended Structure with Metadata

```yaml
environments:
  - development
  - staging
  - production
  - testing
  - integration

# Optional: Environment metadata (not currently used by the system but useful for documentation)
environment_metadata:
  development:
    description: "Local development environment"
    purpose: "Developer workstations and local testing"
    resource_profile: "minimal"
  
  staging:
    description: "Pre-production staging environment"
    purpose: "Integration testing and QA validation"
    resource_profile: "medium"
  
  production:
    description: "Production environment"
    purpose: "Live customer-facing services"
    resource_profile: "high-availability"
  
  testing:
    description: "Automated testing environment"
    purpose: "CI/CD pipeline testing"
    resource_profile: "minimal"
  
  integration:
    description: "Integration testing environment"
    purpose: "Cross-service integration testing"
    resource_profile: "medium"
```

## Example Configurations

### Simple Three-Tier Setup

```yaml
environments:
  - development
  - staging
  - production
```

This is the most common setup with:
- **development**: Local development and unit testing
- **staging**: Pre-production testing and validation
- **production**: Live production environment

### Extended Multi-Environment Setup

```yaml
environments:
  - local
  - development
  - testing
  - integration
  - staging
  - pre-production
  - production
  - disaster-recovery
```

This extended setup includes:
- **local**: Individual developer environments
- **development**: Shared development environment
- **testing**: Automated testing environment
- **integration**: Cross-service integration testing
- **staging**: User acceptance testing
- **pre-production**: Final validation before production
- **production**: Live production environment
- **disaster-recovery**: Backup production environment

### Multi-Region Setup

```yaml
environments:
  - development
  - staging
  - production-us-east
  - production-us-west
  - production-eu-west
  - production-ap-southeast
```

This setup supports multiple production regions:
- Regional production environments for different geographical areas
- Allows for region-specific configurations
- Supports global deployment strategies

### Feature Branch Environments

```yaml
environments:
  - development
  - staging
  - production
  - feature-auth-service
  - feature-payment-gateway
  - feature-mobile-app
```

This setup includes temporary feature environments:
- Dedicated environments for major feature development
- Allows isolated testing of new features
- Can be created and destroyed as needed

## Environment Naming Conventions

### Recommended Naming Patterns

1. **Simple Names**: Use lowercase, single words when possible
   ```yaml
   environments:
     - dev
     - staging
     - prod
   ```

2. **Descriptive Names**: Use clear, descriptive names
   ```yaml
   environments:
     - development
     - staging
     - production
   ```

3. **Hyphenated Names**: Use hyphens for multi-word environments
   ```yaml
   environments:
     - pre-production
     - disaster-recovery
     - load-testing
   ```

4. **Regional Names**: Include region identifiers for multi-region setups
   ```yaml
   environments:
     - production-us-east-1
     - production-eu-west-1
     - production-ap-southeast-1
   ```

### Naming Best Practices

- Use consistent naming patterns across all environments
- Avoid special characters except hyphens
- Keep names concise but descriptive
- Use lowercase for consistency
- Consider alphabetical ordering for easier management

## Integration with Other Components

The environment names defined in `env.yaml` are used throughout the system:

### Redpanda Configuration
```yaml
topics:
  user-events:
    env_settings:
      development:    # Must match env.yaml
        partitions: 1
      production:     # Must match env.yaml
        partitions: 12
```

### Couchbase Configuration
```yaml
buckets:
  app-data:
    env_settings:
      development:    # Must match env.yaml
        ram_quota_mb: 100
      production:     # Must match env.yaml
        ram_quota_mb: 1024
```

### Environment Variable
The system uses the `ENVIRONMENT` environment variable to specify which environment to use:
```bash
export ENVIRONMENT=production
```

This value must match one of the environments listed in `env.yaml`.

## Validation Behavior

When the system starts:

1. **Environment Check**: The system reads the `ENVIRONMENT` environment variable
2. **File Loading**: Loads and parses the `env.yaml` file
3. **Validation**: Checks if the specified environment exists in the `environments` list
4. **Error Handling**: If validation fails, the system exits with an error message

### Error Examples

```bash
# If ENVIRONMENT=invalid-env and it's not in env.yaml
Error: Environment 'invalid-env' is not listed in env.yaml
```

## Usage Examples

### Setting Environment for Deployment

```bash
# Set environment variable
export ENVIRONMENT=production

# Run the init system
python src/main.py
```

### Docker Compose Usage

```yaml
version: '3.8'
services:
  init:
    image: cillers/init
    environment:
      - ENVIRONMENT=staging
    volumes:
      - ./conf:/conf
```

### Kubernetes Usage

```yaml
apiVersion: apps/v1
kind: Job
metadata:
  name: cillers-init
spec:
  template:
    spec:
      containers:
      - name: init
        image: cillers/init
        env:
        - name: ENVIRONMENT
          value: "production"
        volumeMounts:
        - name: config
          mountPath: /conf
```

## Best Practices

1. **Keep It Simple**: Start with basic environments and add more as needed
2. **Consistent Naming**: Use consistent naming conventions across all environments
3. **Documentation**: Document the purpose of each environment
4. **Version Control**: Keep `env.yaml` in version control with your configurations
5. **Validation**: Always test environment configurations before deployment
6. **Security**: Ensure environment names don't expose sensitive information
7. **Cleanup**: Remove unused environments to keep the list manageable

## Troubleshooting

### Common Issues

1. **Environment Not Found**
   - Check that the environment name in `ENVIRONMENT` variable matches exactly (case-sensitive)
   - Verify the `env.yaml` file exists and is readable
   - Ensure YAML syntax is correct

2. **YAML Parsing Errors**
   - Validate YAML syntax using a YAML validator
   - Check for proper indentation (use spaces, not tabs)
   - Ensure the `environments` key is present

3. **File Not Found**
   - Verify the `env.yaml` file is in the correct location (`/conf/init/env.yaml`)
   - Check file permissions are readable
   - Ensure the configuration directory is properly mounted in containers

### Debugging Commands

```bash
# Check if file exists
ls -la /conf/init/env.yaml

# Validate YAML syntax
python -c "import yaml; print(yaml.safe_load(open('/conf/init/env.yaml')))"

# Check current environment variable
echo $ENVIRONMENT
```

## Migration and Updates

When updating environments:

1. **Add New Environments**: Simply add new entries to the `environments` list
2. **Remove Environments**: Remove entries and update all dependent configurations
3. **Rename Environments**: Update the name in `env.yaml` and all configuration files that reference it
4. **Test Changes**: Always test configuration changes in a non-production environment first

## Security Considerations

- Environment names should not contain sensitive information
- Keep the `env.yaml` file in version control but be mindful of any metadata that might be sensitive
- Use environment-specific access controls for different deployment targets
- Consider using separate configuration repositories for different security zones
