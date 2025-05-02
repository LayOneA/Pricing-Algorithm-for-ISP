import numpy as np
import matplotlib.pyplot as plt

# 这个是随便找的静态参数
TIME_STEPS = 24
INITIAL_PRICE = 10.0
NUM_USERS = 100
CAPACITY = 500
PRICE_ADJUSTMENT_FACTOR = 0.1
TARGET_CONGESTION = 0.5

revenues = []
satisfactions = []

price = INITIAL_PRICE

for t in range(TIME_STEPS):
    base_usage = 5
    usage_sensitivity = 0.5
    user_usages = []

    for _ in range(NUM_USERS):
        usage = np.random.normal(base_usage - usage_sensitivity * price, 1)
        usage = max(0, usage)
        user_usages.append(usage)

    total_usage = sum(user_usages)
    congestion = total_usage / CAPACITY

    price_change = PRICE_ADJUSTMENT_FACTOR * (congestion - TARGET_CONGESTION)
    price = max(0, price + price_change)

    revenue = price * total_usage
    satisfaction = max(0, 1.5 - congestion - 0.05 * price)  # 控制变量

    revenues.append(revenue)
    satisfactions.append(satisfaction)

figs = []

fig4 = plt.figure()
plt.plot(revenues, marker='o', color='purple')
plt.title('Revenue over Time')
plt.xlabel('Hour')
plt.ylabel('Revenue')
figs.append(fig4)

fig5 = plt.figure()
plt.plot(satisfactions, marker='o', color='orange')
plt.title('User Satisfaction over Time')
plt.xlabel('Hour')
plt.ylabel('Satisfaction (Arbitrary Scale)')
figs.append(fig5)

plt.tight_layout()
plt.show()