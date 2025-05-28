
"""
Simulation Environment
Defines ArbitrageEnv to simulate sourcing, costs, and disruptions.
"""
import random

class ArbitrageEnv:
    def __init__(self, initial_data):
        # Materials and regions in scope
        self.materials = initial_data['materials']
        self.regions = list(initial_data['regions'].keys())
        # Region data includes FX, base prices, shipping, tariffs, reliability
        self.region_data = initial_data['regions']
        # Current period index (time step)
        self.current_step = 0
        # Initialize current prices (in USD) for each material-region
        self.current_prices = {region: {} for region in self.regions}
        for region, info in self.region_data.items():
            fx_rate = info['FX']
            for material in self.materials:
                base_local = info['base_price'][material]
                self.current_prices[region][material] = base_local * fx_rate
        # Parameters for simulating price changes
        self.volatility = {
            region: {material: 0.02 for material in self.materials}
            for region in self.regions
        }
        self.trend = {
            region: {material: 0.0 for material in self.materials}
            for region in self.regions
        }

    def _update_prices(self):
        """Simulate price changes for the next time step."""
        for region, mat_prices in self.current_prices.items():
            for material, price in mat_prices.items():
                drift = self.trend[region][material]
                vol = self.volatility[region][material]
                change_pct = random.uniform(-vol, vol) + drift
                new_price = price * (1 + change_pct)
                self.current_prices[region][material] = max(new_price, 0.01)

    def calculate_cost(self, action, apply_disruptions=False):
        """
        Calculate the total landed cost for a sourcing action.
        Returns (total_cost, breakdown dict).
        """
        breakdown = {}
        total_cost = 0.0
        # Simulate disruptions if enabled
        disruptions = {}
        if apply_disruptions:
            for region, info in self.region_data.items():
                if random.random() > info['reliability']:
                    disruptions[region] = True
        # Compute costs per material
        for material, region in action.items():
            info = self.region_data[region]
            base_price = self.current_prices[region][material]
            tariff = base_price * info['tariff'][material]
            shipping = info['shipping_cost'][material]
            cost = base_price + tariff + shipping
            disrupted = False
            if apply_disruptions and region in disruptions:
                cost *= 1.5
                disrupted = True
            breakdown[material] = {
                'region': region,
                'base_price_usd': base_price,
                'tariff_cost': tariff,
                'shipping_cost': shipping,
                'disrupted': disrupted,
                'total_cost': cost
            }
            total_cost += cost
        # Apply synergy discounts for sourcing multiple items from same region
        synergy_discount = 0.0
        counts = {}
        for mat, reg in action.items():
            counts[reg] = counts.get(reg, 0) + 1
        for reg, cnt in counts.items():
            if cnt > 1:
                synergy_discount += 20.0 * (cnt - 1)
        total_cost -= synergy_discount
        if synergy_discount:
            breakdown['synergy_discount'] = synergy_discount
        return total_cost, breakdown

    def step(self, action):
        """
        Apply action, simulate disruptions, update prices, and return:
        (next_state, reward, done, info).
        """
        total_cost, cost_info = self.calculate_cost(action, apply_disruptions=True)
        reward = -total_cost
        self.current_step += 1
        self._update_prices()
        done = False
        info = {'cost_breakdown': cost_info, 'total_cost': total_cost}
        return self.current_prices, reward, done, info
