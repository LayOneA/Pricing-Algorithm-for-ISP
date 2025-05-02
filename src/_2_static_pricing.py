import yaml

class StaticPricing:
    def __init__(self, config_path="../config/static_pricing.yaml"):
        with open(config_path) as f:
            config = yaml.safe_load(f)

        self.user_types = config["user_types"]
        self.network = config["network"]

    def calculate_price(self, user_counts):

        total_demand = sum(
            user_counts[utype] * self.user_types[utype]["usage_high"]
            for utype in ["Light", "Medium", "Heavy"]
        )

        demand_ratio = total_demand / self.network["capacity"]

        total_users = sum(user_counts.values())
        weighted_threshold = sum(
            (user_counts[utype] / total_users) * self.user_types[utype]["price_threshold"]
            for utype in ["Light", "Medium", "Heavy"]
        )

        price = self.network["base_price"] + (demand_ratio * weighted_threshold)

        return price