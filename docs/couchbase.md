# Couchbase Documentation

## Overview

Couchbase is a distributed NoSQL document database that combines the flexibility of JSON with the power of SQL. It provides high performance, scalability, and availability for modern applications through its memory-first architecture and built-in caching layer.

## What Couchbase Does

Couchbase serves as a multi-model database platform that:

- **Document Storage**: Stores and retrieves JSON documents with flexible schemas
- **Key-Value Operations**: Provides fast key-value access patterns for high-performance applications
- **Full-Text Search**: Offers built-in search capabilities across document content
- **Analytics**: Supports real-time analytics and reporting on operational data
- **Mobile Sync**: Enables offline-first mobile applications with automatic synchronization
- **Caching**: Acts as a distributed cache layer with sub-millisecond latency

## Key Features

- **Memory-First Architecture**: Automatic caching with configurable memory quotas
- **Multi-Model**: Supports document, key-value, and analytical workloads
- **ACID Transactions**: Provides ACID guarantees across multiple documents
- **N1QL**: SQL-like query language for JSON documents
- **Auto-Scaling**: Automatic data distribution and rebalancing
- **Cross Datacenter Replication (XDCR)**: Built-in replication across clusters

## Configuration Format

The Couchbase controller uses YAML configuration files to define buckets, scopes, and collections. The configuration supports:

- Global defaults for buckets and collections
- Per-bucket and per-collection defaults
- Environment-specific overrides

### Configuration Structure

```yaml
# Global bucket defaults applied to all buckets
bucket_defaults:
  ram_quota_mb: 100
  num_replicas: 0
  flush_enabled: false
  bucket_type: "couchbase"
  max_ttl: 0

# Global collection defaults applied to all collections
collection_defaults:
  max_ttl: 0

# Bucket definitions
buckets:
  bucket_name:
    # Bucket-specific defaults (override global defaults)
    defaults:
      ram_quota_mb: 256
      num_replicas: 1
      bucket_type: "couchbase"
    
    # Environment-specific bucket settings
    env_settings:
      development:
        ram_quota_mb: 100
        num_replicas: 0
      
      production:
        ram_quota_mb: 1024
        num_replicas: 2
    
    # Scope definitions within the bucket
    scopes:
      scope_name:
        # Collection definitions within the scope
        collections:
          collection_name:
            # Collection-specific defaults
            defaults:
              max_ttl: 3600  # 1 hour
            
            # Environment-specific collection settings
            env_settings:
              development:
                max_ttl: 300  # 5 minutes for dev
              
              production:
                max_ttl: 86400  # 24 hours for prod
```

### Configuration Parameters

#### Bucket-Level Settings

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `ram_quota_mb` | integer | Memory quota for the bucket in MB | 100 |
| `num_replicas` | integer | Number of replica copies (0-3) | 0 |
| `flush_enabled` | boolean | Whether bucket can be flushed | false |
| `bucket_type` | string | Bucket type: "couchbase", "ephemeral", "memcached" | "couchbase" |
| `max_ttl` | integer | Maximum TTL for documents in seconds (0 = no limit) | 0 |

#### Collection-Level Settings

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `max_ttl` | integer | Maximum TTL for documents in seconds (0 = no limit) | 0 |

#### Bucket Types

- **couchbase**: Standard persistent bucket with full Couchbase features
- **ephemeral**: In-memory bucket without persistence (faster but data lost on restart)
- **memcached**: Simple key-value bucket compatible with Memcached protocol

## Example Configurations

### Basic Application Configuration

```yaml
bucket_defaults:
  ram_quota_mb: 100
  num_replicas: 0
  flush_enabled: false
  bucket_type: "couchbase"

collection_defaults:
  max_ttl: 0

buckets:
  app-data:
    defaults:
      ram_quota_mb: 256
      num_replicas: 1
    
    env_settings:
      production:
        ram_quota_mb: 1024
        num_replicas: 2
    
    scopes:
      _default:
        collections:
          _default:
            defaults:
              max_ttl: 0
          
          sessions:
            defaults:
              max_ttl: 3600  # 1 hour
            
            env_settings:
              development:
                max_ttl: 300  # 5 minutes
              
              production:
                max_ttl: 7200  # 2 hours
```

### Multi-Tenant Configuration

```yaml
bucket_defaults:
  ram_quota_mb: 100
  num_replicas: 1
  flush_enabled: false
  bucket_type: "couchbase"

collection_defaults:
  max_ttl: 0

buckets:
  tenant-data:
    defaults:
      ram_quota_mb: 512
      num_replicas: 1
    
    env_settings:
      development:
        ram_quota_mb: 100
        num_replicas: 0
      
      production:
        ram_quota_mb: 2048
        num_replicas: 2
    
    scopes:
      tenant-a:
        collections:
          users:
            defaults:
              max_ttl: 0
          
          sessions:
            defaults:
              max_ttl: 1800  # 30 minutes
          
          cache:
            defaults:
              max_ttl: 300  # 5 minutes
      
      tenant-b:
        collections:
          users:
            defaults:
              max_ttl: 0
          
          sessions:
            defaults:
              max_ttl: 3600  # 1 hour
          
          analytics:
            defaults:
              max_ttl: 86400  # 24 hours
```

### Caching and Session Store Configuration

```yaml
bucket_defaults:
  ram_quota_mb: 100
  num_replicas: 0
  flush_enabled: true
  bucket_type: "couchbase"

collection_defaults:
  max_ttl: 3600

buckets:
  cache-store:
    defaults:
      ram_quota_mb: 512
      num_replicas: 0
      bucket_type: "ephemeral"  # In-memory for speed
      flush_enabled: true
    
    env_settings:
      development:
        ram_quota_mb: 100
      
      production:
        ram_quota_mb: 2048
        num_replicas: 1  # Some redundancy in prod
    
    scopes:
      _default:
        collections:
          sessions:
            defaults:
              max_ttl: 1800  # 30 minutes
            
            env_settings:
              development:
                max_ttl: 300  # 5 minutes for dev
              
              production:
                max_ttl: 3600  # 1 hour for prod
          
          api-cache:
            defaults:
              max_ttl: 300  # 5 minutes
            
            env_settings:
              development:
                max_ttl: 60  # 1 minute for dev
              
              production:
                max_ttl: 600  # 10 minutes for prod
          
          user-preferences:
            defaults:
              max_ttl: 86400  # 24 hours
```

### Event Sourcing and Analytics Configuration

```yaml
bucket_defaults:
  ram_quota_mb: 256
  num_replicas: 1
  flush_enabled: false
  bucket_type: "couchbase"

collection_defaults:
  max_ttl: 0

buckets:
  event-store:
    defaults:
      ram_quota_mb: 1024
      num_replicas: 2
      flush_enabled: false
    
    env_settings:
      development:
        ram_quota_mb: 256
        num_replicas: 0
      
      production:
        ram_quota_mb: 4096
        num_replicas: 2
    
    scopes:
      events:
        collections:
          user-events:
            defaults:
              max_ttl: 0  # Keep forever
          
          order-events:
            defaults:
              max_ttl: 0  # Keep forever
          
          system-events:
            defaults:
              max_ttl: 2592000  # 30 days
            
            env_settings:
              development:
                max_ttl: 86400  # 1 day for dev
              
              production:
                max_ttl: 7776000  # 90 days for prod
      
      analytics:
        collections:
          daily-aggregates:
            defaults:
              max_ttl: 7776000  # 90 days
          
          monthly-reports:
            defaults:
              max_ttl: 31536000  # 1 year
```

### Multi-Environment Configuration

```yaml
bucket_defaults:
  ram_quota_mb: 100
  num_replicas: 0
  flush_enabled: false
  bucket_type: "couchbase"
  max_ttl: 0

collection_defaults:
  max_ttl: 0

buckets:
  application:
    defaults:
      ram_quota_mb: 256
      num_replicas: 1
    
    env_settings:
      development:
        ram_quota_mb: 100
        num_replicas: 0
        flush_enabled: true
      
      staging:
        ram_quota_mb: 512
        num_replicas: 1
        flush_enabled: false
      
      production:
        ram_quota_mb: 2048
        num_replicas: 2
        flush_enabled: false
    
    scopes:
      _default:
        collections:
          _default:
            defaults:
              max_ttl: 0
      
      user-data:
        collections:
          profiles:
            defaults:
              max_ttl: 0
          
          preferences:
            defaults:
              max_ttl: 86400  # 24 hours
            
            env_settings:
              development:
                max_ttl: 3600  # 1 hour for dev
              
              production:
                max_ttl: 604800  # 7 days for prod
          
          sessions:
            defaults:
              max_ttl: 3600  # 1 hour
            
            env_settings:
              development:
                max_ttl: 300  # 5 minutes for dev
              
              staging:
                max_ttl: 1800  # 30 minutes for staging
              
              production:
                max_ttl: 7200  # 2 hours for prod
      
      application-data:
        collections:
          configurations:
            defaults:
              max_ttl: 0
          
          feature-flags:
            defaults:
              max_ttl: 3600  # 1 hour
          
          metrics:
            defaults:
              max_ttl: 604800  # 7 days
            
            env_settings:
              development:
                max_ttl: 86400  # 1 day for dev
              
              production:
                max_ttl: 2592000  # 30 days for prod
```

## Environment Variables

The Couchbase controller supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `COUCHBASE_HOST` | Couchbase server hostname | "couchbase" |
| `COUCHBASE_USERNAME` | Admin username for cluster | "admin" |
| `COUCHBASE_PASSWORD` | Admin password for cluster | "password" |
| `COUCHBASE_TLS` | Enable TLS connection | "false" |
| `COUCHBASE_TYPE` | Type: "server" or "client" | "server" |

## Usage

The CouchbaseController automatically:

1. Initializes the Couchbase cluster (if type is "server")
2. Connects to the cluster with retry logic
3. Loads the configuration from `couchbase.yaml`
4. Creates buckets, scopes, and collections that don't exist
5. Applies the appropriate settings based on the environment
6. Handles configuration merging (global → item defaults → environment-specific)

## Data Organization

### Buckets
- Top-level containers for data
- Have memory quotas and replication settings
- Can be of different types (couchbase, ephemeral, memcached)

### Scopes
- Logical groupings within buckets
- Help organize collections by domain or tenant
- The `_default` scope exists by default in every bucket

### Collections
- Actual containers for documents
- Similar to tables in relational databases
- Can have TTL settings for automatic document expiration

## Best Practices

1. **Memory Planning**: Allocate appropriate RAM quotas based on working set size
2. **Replication**: Use 1-2 replicas for production environments
3. **TTL Usage**: Set appropriate TTL values for temporary data like sessions and cache
4. **Scope Organization**: Use scopes to separate different domains or tenants
5. **Collection Design**: Create collections based on access patterns and data lifecycle
6. **Environment Separation**: Use different configurations for development, staging, and production
7. **Monitoring**: Monitor memory usage, disk I/O, and query performance
8. **Backup Strategy**: Implement regular backups for persistent data
