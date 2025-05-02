import numpy as np
import yaml
import os
import pickle

class QLearningPricingAgent:
    def __init__(self, config_path="../config/q_learning.yaml"):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)['q_learning']

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, config['model_path'])
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        self.learning_rate = config['learning_rate']
        self.discount_factor = config['discount_factor']
        self.epsilon = config['epsilon_start']
        self.epsilon_min = config['epsilon_min']
        self.epsilon_decay = config['epsilon_decay']
        self.delta_actions = config['delta_actions']
        self.min_price = config['min_price']
        self.state_categories = config['state_categories']

        self.current_price = 6.5

        self.q_table = np.zeros((
            self.state_categories,
            len(self.delta_actions)
        ))

    def get_state_index(self, congestion_ratio):
        congestion_idx = min(int(congestion_ratio * 10), 9)

        if self.current_price < 4.0:
            price_idx = 0
        elif 4.0 <= self.current_price < 6.0:
            price_idx = 1
        elif 6.0 <= self.current_price < 8.0:
            price_idx = 2
        elif 8.0 <= self.current_price < 10.0:
            price_idx = 3
        elif 10.0 <= self.current_price < 12.0:
            price_idx = 4
        else:
            price_idx = 5

        return congestion_idx * 6 + price_idx

    def calculate_reward(self, prev_congestion, current_congestion):

        prev_error = abs(prev_congestion - 0.5)
        current_error = abs(current_congestion - 0.5)

        reward = 10.0 * (prev_error - current_error)

        if current_error < 0.05:
            reward += 2.0
        elif current_error > 0.8:
            reward -= 5.0

        return np.clip(reward, -10, 10)

    def choose_action(self, congestion_ratio):
        state_idx = self.get_state_index(congestion_ratio)
        if np.random.rand() < self.epsilon:
            delta = np.random.choice(self.delta_actions)
        else:
            delta = self.delta_actions[np.argmax(self.q_table[state_idx])]
        return delta

    def apply_price_change(self, delta):
        self.current_price = max(self.current_price + delta, self.min_price)
        return self.current_price

    def update_q_table(self, prev_state_info, delta, next_state_info):
        prev_congestion, _ = prev_state_info
        next_congestion, _ = next_state_info

        reward = self.calculate_reward(prev_congestion, next_congestion)

        state_idx = self.get_state_index(prev_congestion)
        next_state_idx = self.get_state_index(next_congestion)
        action_idx = self.delta_actions.index(delta)

        current_q = self.q_table[state_idx, action_idx]
        max_future_q = np.max(self.q_table[next_state_idx])
        new_q = (1 - self.learning_rate) * current_q + \
                self.learning_rate * (reward + self.discount_factor * max_future_q)
        self.q_table[state_idx, action_idx] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def save_model(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'q_table': self.q_table,
                'current_price': self.current_price
            }, f)

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.q_table = data['q_table']
                self.current_price = data.get('current_price', 6.0)
        return self