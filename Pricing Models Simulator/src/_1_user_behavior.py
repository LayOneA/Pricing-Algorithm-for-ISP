import math
import yaml

class User:
    def __init__(self, user_type, config):
        self.user_type = user_type
        self.price_threshold = config["price_threshold"]  # 预期价格P0
        self.price_elasticity = config["price_elasticity"]  # 弹性系数e
        self.usage_high = config["usage_high"]  # 预期用量Q0
        self.usage_low = config["usage_low"]  # 最低用量Q_min
        self.k = config.get("decay_factor", 0.1)  # 衰减系数k

    def get_data_usage(self, price_per_gb):
        if price_per_gb <= self.price_threshold:
            return self.usage_high
        else:
            delta_price = price_per_gb - self.price_threshold
            exponent = -self.price_elasticity * self.k * delta_price
            calculated_usage = self.usage_high * math.exp(exponent)
            return max(self.usage_low, calculated_usage)

    def get_satisfaction(self, actual_usage, current_price, congestion):
        # 1. 使用量达成率
        usage_ratio = actual_usage / self.usage_high
        # 2. 价格容忍度
        if current_price <= self.price_threshold:
            price_tolerance = 1.0
        else:
            price_tolerance = 1 / (1 + self.price_elasticity * (current_price - self.price_threshold))
            if actual_usage == self.usage_low:
                price_penalty = (self.price_threshold - current_price) / self.price_threshold
                price_tolerance = price_penalty + price_tolerance
        # 3. 拥堵容忍度
        if congestion <= 0.5:
            congestion_tolerance = 1
        else:
            congestion_tolerance = 1 - (congestion-0.5)
        # 组合权重调整为（3:1:6）
        satisfaction = (
                usage_ratio * 0.3 +
                price_tolerance * 0.1 +
                congestion_tolerance * 0.6
        )
        return max(0.0, min(1.0, satisfaction))

    def __str__(self):
        return (f"{self.user_type} user | Threshold: {self.price_threshold} RMB/GB | "
                f"Elasticity: {self.price_elasticity} | Decay: {self.k}")


def load_user_config(file_path="../config/user_types.yaml"):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config["user_types"]