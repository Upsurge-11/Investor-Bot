"""
Configuration manager to centralize all configuration handling
"""
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self.strategy_config = None
        self.company_mapping = None
    
    def load_strategy_config(self) -> Dict[str, Any]:
        """Load strategy configuration"""
        if self.strategy_config is None:
            config_path = self.config_dir / "strategy_config.yaml"
            try:
                with open(config_path, 'r') as file:
                    self.strategy_config = yaml.safe_load(file)
            except FileNotFoundError:
                print(f"Strategy config not found at {config_path}")
                self.strategy_config = self._get_default_strategy_config()
            except Exception as e:
                print(f"Error loading strategy config: {e}")
                self.strategy_config = self._get_default_strategy_config()
        
        return self.strategy_config
    
    def load_company_mapping(self) -> Dict[str, str]:
        """Load company name to ticker mapping"""
        if self.company_mapping is None:
            mapping_path = Path("data") / "company_mapping.json"
            try:
                with open(mapping_path, 'r') as file:
                    self.company_mapping = json.load(file)
            except FileNotFoundError:
                print(f"Company mapping not found at {mapping_path}")
                self.company_mapping = {}
            except Exception as e:
                print(f"Error loading company mapping: {e}")
                self.company_mapping = {}
        
        return self.company_mapping
    
    def get_strategy_setting(self, strategy_type: str, setting_name: str, default_value: Any = None) -> Any:
        """Get specific strategy setting"""
        config = self.load_strategy_config()
        return config.get(strategy_type, {}).get(setting_name, default_value)
    
    def get_momentum_config(self) -> Dict[str, Any]:
        """Get momentum strategy configuration"""
        return self.get_strategy_setting('momentum', {})
    
    def get_value_config(self) -> Dict[str, Any]:
        """Get value strategy configuration"""
        return self.get_strategy_setting('value', {})
    
    def get_risk_config(self) -> Dict[str, Any]:
        """Get risk management configuration"""
        return self.get_strategy_setting('risk_management', {})
    
    def _get_default_strategy_config(self) -> Dict[str, Any]:
        """Get default strategy configuration"""
        return {
            'momentum': {
                'top_gainers': {'enabled': True, 'top_n': 5, 'min_gain_percent': 2.0},
                'moving_average': {'enabled': True, 'short_period': 20, 'long_period': 50}
            },
            'mean_reversion': {
                'rsi': {'enabled': True, 'period': 14, 'oversold_threshold': 30},
                'support_resistance': {'enabled': True, 'support_tolerance': 0.02}
            },
            'value': {
                'low_pe': {'enabled': True, 'max_pe_ratio': 15},
                'high_dividend': {'enabled': True, 'min_yield_percent': 2.0}
            },
            'risk_management': {
                'max_recommendations': 15,
                'min_confidence_score': 50
            }
        }
    
    def save_strategy_config(self, config: Dict[str, Any]) -> bool:
        """Save strategy configuration"""
        try:
            config_path = self.config_dir / "strategy_config.yaml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            
            self.strategy_config = config  # Update cached config
            return True
        except Exception as e:
            print(f"Error saving strategy config: {e}")
            return False
    
    def get_company_ticker(self, company_name: str) -> Optional[str]:
        """Get ticker symbol for company name"""
        mapping = self.load_company_mapping()
        return mapping.get(company_name)
    
    def get_company_name(self, ticker: str) -> Optional[str]:
        """Get company name for ticker symbol"""
        mapping = self.load_company_mapping()
        for company, tick in mapping.items():
            if tick == ticker:
                return company
        return None


# Global configuration manager
config_manager = ConfigManager()
