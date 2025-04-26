import yaml

class RuleBasedPricing:
    def __init__(self, config_path="../config/rule_based.yaml"):
        self._load_config(config_path)
        self.current_level = self.config["initial_level"]

    def _load_config(self, file_path):
        with open(file_path, 'r') as f:
            self.config = yaml.safe_load(f)["rule_based"]

    def update_price(self, congestion_ratio):
        if congestion_ratio > self.config["thresholds"]["upgrade"]:
            self._upgrade()
        elif congestion_ratio < self.config["thresholds"]["downgrade"]:
            self._downgrade()
        return self.current_price

    def _upgrade(self):
        if self.current_level == "low":
            self.current_level = "medium"
        elif self.current_level == "medium":
            self.current_level = "high"

    def _downgrade(self):
        if self.current_level == "high":
            self.current_level = "medium"
        elif self.current_level == "medium":
            self.current_level = "low"

    @property
    def current_price(self):
        return self.config["price_levels"][self.current_level]

    def __str__(self):
        return f"Rule_based Pricing | Level: {self.current_level} ({self.current_price} RMB/GB)"