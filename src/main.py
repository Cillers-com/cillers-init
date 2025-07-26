#!/usr/bin/env python3

import os
import sys
import yaml
import time
from pathlib import Path
from config import Config
from controllers.couchbase_controller import CouchbaseController
from controllers.redpanda_controller import RedpandaController

def get_env_var(name, default=None):
    """Get environment variable with optional default."""
    try:
        if default is not None:
            return os.environ.get(name, default)
        else:
            return os.environ[name]
    except KeyError:
        raise KeyError(f"Environment variable '{name}' is not set")

def main():
    """Main entry point for the init module."""
    print("Starting init module...")
    
    # Get environment variables
    environment = get_env_var('ENVIRONMENT')
    services = get_env_var('INIT_SERVICES', 'couchbase,redpanda').split(',')
    
    print(f"Environment: {environment}")
    print(f"Services: {services}")
    
    # Initialize config manager
    config_dir = Path('/conf/init')
    config = Config(config_dir, environment)
    
    # Validate environment
    if not config.is_valid_environment(environment):
        print(f"Error: Environment '{environment}' is not listed in env.yaml")
        sys.exit(1)
    
    # Process services
    if 'couchbase' in services:
        couchbase_controller = CouchbaseController(environment, config_dir)
        couchbase_controller.run_ops()
    
    if 'redpanda' in services:
        redpanda_controller = RedpandaController(environment, config_dir)
        redpanda_controller.run_ops()
    
    print("All operations completed successfully")

if __name__ == "__main__":
    main()
