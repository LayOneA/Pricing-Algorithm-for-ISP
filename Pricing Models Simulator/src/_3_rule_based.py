import yaml
import numpy as np

class RuleBasedPricing:
    def __init__(self, config_path="../config/rule_based.yaml"):
        self._load_config(config_path)
        self.current_price = self.config["initial_price"]
        self.target_congestion = self.config["target_congestion"]
        self.price_adjustment_factor = self.config["price_adjustment_factor"]
        self.min_price = self.config["min_price"]
        self.max_price = self.config["max_price"]

    def _load_config(self, file_path):
        with open(file_path, 'r') as f:
            self.config = yaml.safe_load(f)["rule_based"]

    def update_price(self, congestion_ratio):
        congestion_deviation = congestion_ratio - self.target_congestion
        price_delta = self.price_adjustment_factor * congestion_deviation

        self.current_price = np.clip(
            self.current_price + price_delta,
            self.min_price,
            self.max_price
        )
        return self.current_price

    @property
    def current_price(self):
        return self._current_price

    @current_price.setter
    def current_price(self, value):
        self._current_price = round(value, 2)

    def __str__(self):
        return f"Dynamic Pricing | Target: {self.target_congestion} | Current: {self.current_price} RMB/GB"