from typing import Optional, Tuple

import gymnasium
from gymnasium import spaces
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from gymnasium.utils.env_checker import check_env

class TradingEnv(gymnasium.Env):
    def __init__(self, data):
        super(TradingEnv, self).__init__()

        self.data = data
        self.current_step = 0
        self.buy_threshold = 0.5
        self.sell_threshold = -0.5
        self.total_portfolio = 10000 #initial cash
        self.cash = 10000 #cash for trading
        self.shares_owned = 0
        self.position = None
        self.first_trade_done = False
        self.iteration_logs = []

        # Define action and observation spaces
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low = np.array([-1, 0, -1, -1]),
            high = np.array([1, 1000, 1, 1]),
            shape=(4, ),
            dtype=np.float32
        )

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, dict]:

        if seed is not None:
            np.random.seed(seed)

        self.current_step = 0
        self.buy_threshold = 0.5
        self.sell_threshold = -0.5
        self.total_portfolio = 10000
        self.cash = 10000
        self.shares_owned = 0
        self.position = None
        self.first_trade_done = False
        return self._next_observation(), {}

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        if action == 0:
            self.buy_threshold += 0.05
        elif action == 1:
            self.buy_threshold -= 0.05
        elif action == 2:
            self.sell_threshold += 0.05
        elif action == 3:
            self.sell_threshold -= 0.05

        #update port value
        self.total_portfolio = self._update_port_value()

        #go to next step
        self.current_step += 1

        #idk wth is this
        terminated = self.current_step >= len(self.data) - 1  # End of dataset
        truncated = False

        #cal reward
        reward = self._calculate_reward()
        log_entry = {'non'}
        if terminated:
            log_entry = {
                "buy_threshold": self.buy_threshold,
                "sell_threshold": self.sell_threshold,
                "final_portfolio_value": self.total_portfolio,
            }
        self.iteration_logs.append(log_entry)

        return self._next_observation(), reward, terminated, truncated, {}

    def _next_observation(self):
        #get data on market info
        row = self.data.iloc[self.current_step]
        return np.array([
            row['sentiment_score'],
            row['closing_price'],
            self.buy_threshold,
            int(self.position is not None)
        ])

    def _calculate_reward(self):
        profit = 0
        buy_reward = 0
        row = self.data.iloc[self.current_step]
        closing_price = row['closing_price']
        if row['sentiment_score'] >= self.buy_threshold and self.shares_owned == 0:
            #buy share with all cash
            num_share_to_buy = int(self.cash / closing_price)
            if num_share_to_buy > 0:
                cost = num_share_to_buy * closing_price
                self.cash -= cost
                self.shares_owned += num_share_to_buy
                self.position = closing_price
                buy_reward = 1.0

        elif row['sentiment_score'] <= self.sell_threshold and self.shares_owned > 0:
            #sell all
            revenue = self.shares_owned * closing_price
            profit = revenue - (self.position * self.shares_owned)
            ###transaction_costs = revenue * 0.001  # lmao look at this sht
            ###revenue -= transaction_costs
            self.cash += revenue

            #reset position after sell all
            self.shares_owned = 0
            self.position = None

        current_port_value = self._update_port_value()
        port_change = current_port_value - self.total_portfolio # change in port value
        #update port value for next step
        self.total_portfolio = current_port_value

        #reward for growth, penalty for loss
        if port_change > 0:
            reward_for_growth = port_change * 0.001
        else:
            reward_for_growth = port_change * 0.002
        # Small penalty for holding or inactivity without trading decisions
        inactivity_penalty = -0.01

        if not self.first_trade_done:
            inactivity_penalty += -0.1
        else:
            inactivity_penalty += -0.05
        total_reward = reward_for_growth + inactivity_penalty + profit * 1.05 + buy_reward

        return total_reward

    def _update_port_value(self):
        #Update total portfolio value based on cash and current share value.
        current_price = self.data.iloc[self.current_step]['closing_price']
        share_value = current_price * self.shares_owned
        return self.cash + share_value
# uncomment to train
# #load market data
# df = pd.read_csv('filtered_data.csv')
#
# #Initialize the trading environment
# env = TradingEnv(df)
#
# #Train PPO moddel
# model = PPO("MlpPolicy", env, verbose=1, device='cpu')
# model.learn(total_timesteps= 130000)
#
# logs_df = pd.DataFrame(env.iteration_logs)
# logs_df.to_csv("iteration_logs.csv", index=False)
#
# # Save the trained model to a file.
# model.save("rl_sentiment_closing_price_bot")
#


