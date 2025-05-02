import math
import yaml
import numpy as np
import matplotlib.pyplot as plt
from _1_user_behavior import User, load_user_config
from _2_Q_learning import QLearningPricingAgent
from _2_static_pricing import StaticPricing
from _3_rule_based import RuleBasedPricing

def initialize_users(user_config, total_users=300, ratios=(0.4, 0.3, 0.3)):
    light = int(total_users * ratios[0])
    medium = int(total_users * ratios[1])
    heavy = total_users - light - medium

    return (
            [User('Light', user_config['Light']) for _ in range(light)] +
            [User('Medium', user_config['Medium']) for _ in range(medium)] +
            [User('Heavy', user_config['Heavy']) for _ in range(heavy)]
    )


def run_simulation(users, strategy, network_capacity, iterations=500):
    if strategy == 'static':
        model = StaticPricing()
    elif strategy == 'rule_based':
        model = RuleBasedPricing()
    elif strategy == 'q_learning':
        agent = QLearningPricingAgent().load_model()
        current_price = agent.current_price
    else:
        raise ValueError("Unknown pricing strategy")

    metrics = {
        'congestion': [],
        'satisfaction': [],
        'revenue': [],
        'price': [],
    }

    prev_state = None
    last_delta = 0

    for _ in range(iterations):
        if strategy == 'q_learning':
            price = current_price
        else:
            price = model.current_price if strategy == 'rule_based' else model.calculate_price(
                {'Light': 120, 'Medium': 90, 'Heavy': 90}
            )

        total_usage = sum(u.get_data_usage(price) for u in users)
        congestion = total_usage / network_capacity

        satisfaction = np.mean([
            u.get_satisfaction(u.get_data_usage(price), price, congestion)
            for u in users
        ])
        revenue = total_usage * price

        metrics['congestion'].append(congestion)
        metrics['satisfaction'].append(satisfaction)
        metrics['revenue'].append(revenue)
        metrics['price'].append(price)

        if strategy == 'q_learning':
            if prev_state is not None:
                agent.update_q_table(prev_state, last_delta, (congestion, price))
                agent.decay_epsilon()

            last_delta = agent.choose_action(congestion)
            current_price = agent.apply_price_change(last_delta)
            prev_state = (congestion, price)

        elif strategy == 'rule_based':
            model.update_price(congestion)

    if strategy == 'q_learning':
        agent.save_model()

    return metrics


def plot_results(metrics, strategy):
    plt.figure(figsize=(14, 10))

    # Network Congestion
    plt.subplot(2, 2, 1)
    plt.plot(metrics['congestion'])
    plt.title(f'{strategy} Pricing - Network Congestion')
    plt.ylabel('Congestion Ratio')
    plt.ylim(0, 1)

    # User Satisfaction
    plt.subplot(2, 2, 2)
    plt.plot(metrics['satisfaction'])
    plt.title(f'{strategy} Pricing - User Satisfaction')
    plt.ylabel('Satisfaction Score')
    plt.ylim(0, 1)

    # ISP Revenue
    plt.subplot(2, 2, 3)
    plt.plot(metrics['revenue'])
    plt.title(f'{strategy} Pricing - ISP Revenue')
    plt.ylabel('Revenue (RMB)')

    # Price Variation
    plt.subplot(2, 2, 4)
    plt.plot(metrics['price'])
    plt.title(f'{strategy} Pricing - Price Variation')
    plt.ylabel('Price (RMB/GB)')

    plt.tight_layout()
    plt.savefig(f'{strategy}_performance.png')
    plt.close()


def compare_strategies(results_dict):
    plt.figure(figsize=(14, 12))

    colors = {
        'static': '#1f77b4',
        'rule_based': '#ff7f0e',
        'q_learning': '#2ca02c'
    }

    ax1 = plt.subplot(2, 2, 1)
    for strategy in results_dict:
        ax1.plot(results_dict[strategy]['congestion'],
                 color=colors[strategy], alpha=0.7, label=strategy)
    ax1.set_title('Network Congestion Comparison')
    ax1.set_ylabel('Congestion Ratio')
    ax1.legend()

    ax2 = plt.subplot(2, 2, 2)
    for strategy in results_dict:
        ax2.plot(results_dict[strategy]['satisfaction'],
                 color=colors[strategy], alpha=0.7, label=strategy)
    ax2.set_title('User Satisfaction Comparison')
    ax2.set_ylabel('Satisfaction Score')

    # Revenue Comparison
    ax3 = plt.subplot(2, 2, 3)
    for strategy in results_dict:
        ax3.plot(results_dict[strategy]['revenue'],
                 color=colors[strategy], alpha=0.7, label=strategy)
    ax3.set_title('ISP Revenue Comparison')
    ax3.set_ylabel('Revenue (RMB)')

    # Price Comparison
    ax4 = plt.subplot(2, 2, 4)
    for strategy in results_dict:
        ax4.plot(results_dict[strategy]['price'],
                 color=colors[strategy], alpha=0.7, label=strategy)
    ax4.set_title('Price Variation Comparison')
    ax4.set_ylabel('Price (RMB/GB)')

    plt.tight_layout()
    plt.savefig('strategy_comparison.png')
    plt.close()


if __name__ == "__main__":
    user_config = load_user_config()
    users = initialize_users(user_config)
    network_capacity = StaticPricing().network["capacity"]

    results = {}
    for strategy in ['static', 'rule_based', 'q_learning']:
        results[strategy] = run_simulation(users, strategy, network_capacity, iterations=200)
        plot_results(results[strategy], strategy)
        print(f"{strategy} simulation finished, result saved as {strategy}_performance.png")

    compare_strategies(results)
    print("Comparison chart saved as strategy_comparison.png")