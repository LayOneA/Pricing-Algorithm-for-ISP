import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("📡 Network Simulation Dashboard")

num_users = st.sidebar.slider("Number of Users", 10, 500, 100, step=10)
capacity = st.sidebar.slider("Network Capacity (GB)", 100, 1000, 500, step=50)
initial_price = st.sidebar.slider("Initial Price per GB (RMB)", 1.0, 20.0, 10.0, step=0.5)
target_congestion = st.sidebar.slider("Target Congestion Level", 0.1, 1.0, 0.5, step=0.05)
price_adjustment_factor = st.sidebar.slider("Price Adjustment Factor", 0.01, 0.5, 0.1, step=0.01)
time_steps = st.sidebar.slider("Simulation Hours", 6, 48, 24, step=6)

prices = []
total_usages = []
congestion_levels = []
revenues = []
satisfactions = []
satisfactions_tweaked = []

price = initial_price

for t in range(time_steps):
    base_usage = 5
    usage_sensitivity = 0.5
    user_usages = []

    for _ in range(num_users):
        usage = np.random.normal(base_usage - usage_sensitivity * price, 1)
        usage = max(0, usage)
        user_usages.append(usage)

    total_usage = sum(user_usages)
    congestion = total_usage / capacity

    price_change = price_adjustment_factor * (congestion - target_congestion)
    price = max(0, price + price_change)

    revenue = price * total_usage
    satisfaction = max(0, 1.5 - congestion - 0.05 * price)

    penalty = 0
    if congestion > 0.6:
        penalty += (congestion - 0.6) * 1.5
    if price > 8:
        penalty += (price - 8) * 0.1
    satisfaction_tweaked = max(0, 1 - penalty)

    prices.append(price)
    total_usages.append(total_usage)
    congestion_levels.append(congestion)
    revenues.append(revenue)
    satisfactions.append(satisfaction)
    satisfactions_tweaked.append(satisfaction_tweaked)

df = pd.DataFrame({
    "Hour": range(time_steps),
    "Price": prices,
    "Total Usage": total_usages,
    "Congestion": congestion_levels,
    "Revenue": revenues,
    "Satisfaction": satisfactions,
    "Satisfaction (Tweaked)": satisfactions_tweaked
})

st.subheader("📊 Simulation Data")
st.dataframe(df.style.format("{:.2f}"))

st.subheader("📈 Metrics Over Time")
fig, axs = plt.subplots(3, 2, figsize=(14, 10))
axs = axs.flatten()

metrics = ["Price", "Total Usage", "Congestion", "Revenue", "Satisfaction", "Satisfaction (Tweaked)"]
colors = ['blue', 'green', 'red', 'purple', 'orange', 'teal']

for i, metric in enumerate(metrics):
    axs[i].plot(df["Hour"], df[metric], marker='o', color=colors[i])
    axs[i].set_title(metric)
    axs[i].set_xlabel("Hour")
    axs[i].set_ylabel(metric)
    axs[i].grid(True)

plt.tight_layout()
st.pyplot(fig)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name='simulation_results.csv',
    mime='text/csv'
)
