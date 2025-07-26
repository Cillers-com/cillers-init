# Redpanda Documentation

## Overview

Redpanda is a streaming data platform that is API-compatible with Apache Kafka. It provides high-performance, low-latency streaming for real-time applications without the complexity of managing ZooKeeper.

## What Redpanda Does

Redpanda serves as a distributed streaming platform that:

- **Message Streaming**: Handles high-throughput, low-latency message streaming between applications
- **Event Sourcing**: Stores events in an immutable log for event-driven architectures
- **Data Integration**: Acts as a central hub for data pipelines and real-time analytics
- **Decoupling**: Enables loose coupling between microservices through asynchronous messaging
- **Durability**: Provides persistent storage of messages with configurable retention policies

## Key Features

- **Kafka API Compatibility**: Drop-in replacement for Apache Kafka
- **No ZooKeeper**: Simplified architecture without external dependencies
- **High Performance**: Built in C++ for optimal performance
- **Cloud Native**: Designed for containerized and Kubernetes environments
- **Schema Registry**: Built-in schema management capabilities

## Configuration Format

The Redpanda controller uses YAML configuration files to define topics and their settings. The configuration supports:

- Global defaults for all topics
- Per-topic defaults
- Environment-specific overrides

### Configuration Structure

```yaml
# Global defaults applied to all topics
defaults:
  partitions: 1
  replication: 1
  config:
    cleanup.policy: "delete"
    retention.ms: 604800000  # 7 days
    segment.ms: 86400000     # 1 day

# Topic definitions
topics:
  topic_name:
    # Topic-specific defaults (override global defaults)
    defaults:
      partitions: 3
      replication: 2
      config:
        cleanup.policy: "compact"
        retention.ms: 2592000000  # 30 days
    
    # Environment-specific settings (override all defaults)
    env_settings:
      development:
        partitions: 1
        replication: 1
        config:
          retention.ms: 86400000  # 1 day for dev
      
      production:
        partitions: 6
        replication: 3
        config:
          retention.ms: 7776000000  # 90 days for prod
```

### Configuration Parameters

#### Topic-Level Settings

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `partitions` | integer | Number of partitions for the topic | 1 |
| `replication` | integer | Replication factor for the topic | 1 |
| `config` | object | Topic-specific configuration parameters | {} |

#### Common Topic Configuration Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `cleanup.policy` | string | Log cleanup policy: "delete" or "compact" | "delete" |
| `retention.ms` | integer | Message retention time in milliseconds | 604800000 |
| `retention.bytes` | integer | Maximum size of log before deletion | -1 (unlimited) |
| `segment.ms` | integer | Time before a new log segment is rolled | 86400000 |
| `segment.bytes` | integer | Maximum size of a single log segment | 1073741824 |
| `compression.type` | string | Compression codec: "none", "gzip", "snappy", "lz4", "zstd" | "none" |
| `max.message.bytes` | integer | Maximum size of a message | 1048576 |
| `min.insync.replicas` | integer | Minimum replicas that must acknowledge a write | 1 |

## Example Configurations

### Basic Topic Configuration

```yaml
defaults:
  partitions: 1
  replication: 1
  config:
    cleanup.policy: "delete"
    retention.ms: 604800000

topics:
  user-events:
    defaults:
      partitions: 3
      config:
        cleanup.policy: "delete"
        retention.ms: 2592000000
    
    env_settings:
      production:
        partitions: 12
        replication: 3
```

### Event Sourcing Configuration

```yaml
defaults:
  partitions: 1
  replication: 1
  config:
    cleanup.policy: "compact"
    retention.ms: -1  # Keep forever
    min.cleanable.dirty.ratio: 0.1

topics:
  order-events:
    defaults:
      partitions: 6
      replication: 2
      config:
        cleanup.policy: "compact"
        retention.ms: -1
        segment.ms: 3600000  # 1 hour segments
    
    env_settings:
      development:
        partitions: 1
        replication: 1
        config:
          retention.ms: 86400000  # 1 day for dev
      
      production:
        partitions: 24
        replication: 3
        config:
          min.insync.replicas: 2
```

### High-Throughput Configuration

```yaml
defaults:
  partitions: 1
  replication: 1
  config:
    compression.type: "lz4"
    batch.size: 65536
    linger.ms: 10

topics:
  metrics-stream:
    defaults:
      partitions: 12
      replication: 2
      config:
        cleanup.policy: "delete"
        retention.ms: 86400000  # 1 day
        segment.ms: 3600000     # 1 hour segments
        compression.type: "zstd"
        max.message.bytes: 10485760  # 10MB
    
    env_settings:
      development:
        partitions: 2
        config:
          retention.ms: 3600000  # 1 hour for dev
      
      production:
        partitions: 48
        replication: 3
        config:
          min.insync.replicas: 2
          retention.ms: 259200000  # 3 days
```

### Multi-Environment Configuration

```yaml
defaults:
  partitions: 1
  replication: 1
  config:
    cleanup.policy: "delete"
    retention.ms: 604800000
    compression.type: "lz4"

topics:
  user-activity:
    defaults:
      partitions: 3
      config:
        retention.ms: 2592000000  # 30 days
    
    env_settings:
      development:
        partitions: 1
        replication: 1
        config:
          retention.ms: 86400000  # 1 day
      
      staging:
        partitions: 3
        replication: 2
        config:
          retention.ms: 604800000  # 7 days
      
      production:
        partitions: 12
        replication: 3
        config:
          retention.ms: 7776000000  # 90 days
          min.insync.replicas: 2

  payment-events:
    defaults:
      partitions: 6
      replication: 2
      config:
        cleanup.policy: "compact"
        retention.ms: -1  # Keep forever
        min.cleanable.dirty.ratio: 0.05
    
    env_settings:
      development:
        partitions: 1
        replication: 1
        config:
          retention.ms: 86400000  # 1 day for dev
      
      production:
        partitions: 24
        replication: 3
        config:
          min.insync.replicas: 2
          segment.ms: 1800000  # 30 minutes
```

## Environment Variables

The Redpanda controller supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDPANDA_HOST` | Redpanda broker hostname | "redpanda" |
| `REDPANDA_PORT` | Redpanda broker port | "9092" |

## Usage

The RedpandaController automatically:

1. Connects to the Redpanda cluster with retry logic
2. Loads the configuration from `redpanda.yaml`
3. Creates topics that don't exist
4. Applies the appropriate settings based on the environment
5. Handles topic configuration merging (global → topic defaults → environment-specific)

## Best Practices

1. **Partitioning**: Choose partition count based on expected throughput and consumer parallelism
2. **Replication**: Use replication factor of 3 for production environments
3. **Retention**: Set appropriate retention policies based on data lifecycle requirements
4. **Compression**: Use compression for high-throughput topics to reduce storage and network usage
5. **Environment Separation**: Use different configurations for development, staging, and production
6. **Monitoring**: Monitor topic metrics like lag, throughput, and error rates
