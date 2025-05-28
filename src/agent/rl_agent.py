"""
Reinforcement Learning Agent
Defines RLAgent to decide sourcing plans via optimization or learning.
"""
class RLAgent:
    def __init__(self, env, forecaster):
        raise NotImplementedError("Set up your agent here")

    def decide_action(self, state):
        """
        Choose an action based on current state.
        :param state: current environment state
        :return: (action, adjusted_flag, risky_region)
        """
        raise NotImplementedError("Replace with your decision logic")

"""
Reinforcement Learning Agent
Defines RLAgent to decide sourcing plans via optimization or learning.
"""
from itertools import product

class RLAgent:
    """
    AI agent that decides sourcing plans. Combines forecasting and optimization.
    """
    def __init__(self, env, forecaster):
        self.env = env
        self.forecaster = forecaster
        # Generate all possible actions (combinations of region choices for each material)
        self.all_actions = self._generate_all_actions()
        self.last_action = None

    def _generate_all_actions(self):
        """Generate all possible sourcing plans (all combinations of regions for each material)."""
        actions = []
        for combo in product(self.env.regions, repeat=len(self.env.materials)):
            action = {self.env.materials[i]: combo[i] for i in range(len(self.env.materials))}
            actions.append(action)
        return actions

    def decide_action(self, state):
        """
        Decide on the best sourcing action for the current state.
        state: current prices dict.
        Returns: (chosen_action, risk_adjusted_flag, risky_region)
        """
        # Forecast next-period prices
        if self.forecaster:
            forecasted = self.forecaster.forecast(self.env.current_prices)
        else:
            forecasted = {region: {mat: 0.0 for mat in self.env.materials} for region in self.env.regions}

        best_action = None
        best_metric = float('inf')
        for action in self.all_actions:
            cost, _ = self.env.calculate_cost(action, apply_disruptions=False)
            future_cost = sum(forecasted[action[mat]][mat] if False else forecasted[action[mat]][mat] for mat in action)
            # using consistent mapping: future_cost = sum(forecasted[region][material])
            future_cost = sum(forecasted[action[mat]][mat] for mat in action)
            metric = cost + 0.1 * future_cost
            if metric < best_metric:
                best_metric = metric
                best_action = action

        # Risk mitigation: avoid over-concentration in low-reliability regions
        adjusted = False
        risky_region = None
        region_counts = {}
        for material, region in best_action.items():
            region_counts[region] = region_counts.get(region, 0) + 1

        for region, count in region_counts.items():
            if count > 1 and self.env.region_data[region]['reliability'] < 0.98:
                risky_region = region
                mat_to_switch = None
                best_alt = None
                min_extra_cost = float('inf')
                for mat in [m for m, r in best_action.items() if r == region]:
                    for alt in self.env.regions:
                        if alt == region:
                            continue
                        alt_action = best_action.copy()
                        alt_action[mat] = alt
                        alt_cost, _ = self.env.calculate_cost(alt_action, apply_disruptions=False)
                        # compute cost increase relative to original best_action
                        orig_cost, _ = self.env.calculate_cost(best_action, apply_disruptions=False)
                        extra_cost = alt_cost - orig_cost
                        if extra_cost < min_extra_cost:
                            min_extra_cost = extra_cost
                            best_alt = alt
                            mat_to_switch = mat
                if mat_to_switch:
                    best_action[mat_to_switch] = best_alt
                    adjusted = True
                break

        self.last_action = best_action
        return best_action, adjusted, risky_region

    def learn_from_experience(self, state, action, reward, next_state):
        """
        Placeholder for RL learning updates with (state, action, reward, next_state).
        """
        pass