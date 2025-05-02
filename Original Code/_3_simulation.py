import numpy as np
import matplotlib.pyplot as plt

# Parameters
TIME_STEPS = 24
INITIAL_PRICE = 10.0
NUM_USERS = 100
CAPACITY = 500
PRICE_ADJUSTMENT_FACTOR = 0.1
TARGET_CONGESTION = 0.5

# Initialize lists to store results
prices = []
total_usages = []
congestion_levels = []

price = INITIAL_PRICE

for t in range(TIME_STEPS):
    base_usage = 5
    usage_sensitivity = 0.5
    user_usages = []
    
    # Calculate each user's usage
    for _ in range(NUM_USERS):
        usage = np.random.normal(base_usage - usage_sensitivity * price, 1)
        usage = max(0, usage)  # Ensure usage is not negative
        user_usages.append(usage)
    
    total_usage = sum(user_usages)
    congestion = total_usage / CAPACITY
    
    # Adjust price based on congestion
    price_change = PRICE_ADJUSTMENT_FACTOR * (congestion - TARGET_CONGESTION)
    price = max(0, price + price_change)
    
    # Store results
    prices.append(price)
    total_usages.append(total_usage)
    congestion_levels.append(congestion)
    
    print(
        f"Hour {t}: Price = {price:.2f}, "
        f"Total Usage = {total_usage:.2f}, "
        f"Congestion Level = {congestion:.2f}"
    )

# Plot results
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(prices, marker='o')
plt.title('Price over Time')
plt.xlabel('Hour')
plt.ylabel('Price')

plt.subplot(3, 1, 2)
plt.plot(total_usages, marker='o', color='green')
plt.title('Total Usage over Time')
plt.xlabel('Hour')
plt.ylabel('Total Usage')

plt.subplot(3, 1, 3)
plt.plot(congestion_levels, marker='o', color='red')
plt.title('Congestion Level over Time')
plt.xlabel('Hour')
plt.ylabel('Congestion Level')

plt.tight_layout()
plt.show()