import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Manages configuration loading and environment validation."""
    
    def __init__(self, config_dir: Path, environment: str):
        self.config_dir = config_dir
        self.environment = environment
        self._env_config = None
    
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        file_path = self.config_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_env_config(self) -> Dict[str, Any]:
        """Get environment configuration."""
        if self._env_config is None:
            self._env_config = self.load_yaml('env.yaml')
        return self._env_config
    
    def is_valid_environment(self, environment: str) -> bool:
        """Check if the environment is valid."""
        env_config = self.get_env_config()
        return environment in env_config.get('environments', [])
    
    def merge_settings(self, global_defaults: Dict[str, Any], 
                      item_defaults: Dict[str, Any], 
                      env_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Merge settings with precedence: env_settings > item_defaults > global_defaults."""
        result = {}
        
        # Start with global defaults
        if global_defaults:
            result.update(global_defaults)
        
        # Apply item defaults
        if item_defaults:
            result.update(item_defaults)
        
        # Apply environment-specific settings
        if env_settings:
            result.update(env_settings)
        
        return result
