class User:
    def __init__(self, user_type, price_threshold, price_elasticity):
        """
        初始化用户类
        :param user_type: 用户类型（轻度用户、中度用户、重度用户）
        :param price_threshold: 价格阈值
        :param price_elasticity: 价格弹性（高弹性或低弹性）
        """
        self.user_type = user_type
        self.price_threshold = price_threshold
        self.price_elasticity = price_elasticity

    def get_data_usage(self, price_per_gb):
        """
        根据价格计算用户的数据使用量
        :param price_per_gb: 每GB数据的价格
        :return: 数据使用量（单位：GB）
        """
        if self.price_elasticity == "high":
            # 高弹性用户
            if price_per_gb < self.price_threshold:
                # 价格低于阈值，使用更多数据
                return 10  # 假设高弹性用户在价格低于阈值时使用10GB数据
            else:
                # 价格高于阈值，使用较少数据
                return 2  # 假设高弹性用户在价格高于阈值时使用2GB数据
        elif self.price_elasticity == "low":
            # 低弹性用户
            if price_per_gb < self.price_threshold:
                # 价格低于阈值，使用更多数据
                return 8  # 假设低弹性用户在价格低于阈值时使用8GB数据
            else:
                # 价格高于阈值，使用较少数据
                return 6  # 假设低弹性用户在价格高于阈值时使用6GB数据
        else:
            raise ValueError("Invalid price elasticity")

    def __str__(self):
        return f"{self.user_type} user with price threshold {self.price_threshold} RMB/GB and {self.price_elasticity} price elasticity"


# 定义用户类型
light_user = User("Light", 8, "low")
medium_user = User("Medium", 4, "high")
heavy_user = User("Heavy", 2, "high")

# 测试
price_per_gb = 5  # 每GB数据的价格
print(f"Price per GB: {price_per_gb} RMB")
print(light_user)
print(f"Data usage: {light_user.get_data_usage(price_per_gb)} GB")
print(medium_user)
print(f"Data usage: {medium_user.get_data_usage(price_per_gb)} GB")
print(heavy_user)
print(f"Data usage: {heavy_user.get_data_usage(price_per_gb)} GB")