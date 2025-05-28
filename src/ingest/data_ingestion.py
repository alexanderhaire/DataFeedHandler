"""
Data Ingestion Module
Defines load_initial_data() to fetch or initialize market data.
"""

def load_initial_data():
    """Load or initialize market data for materials, regions, FX rates, tariffs, and supplier performance."""
    data = {
        'materials': ['Steel', 'Electronics'],
        'regions': {
            'USA': {
                'FX': 1.0,
                'base_price': {'Steel': 500.0, 'Electronics': 250.0},
                'shipping_cost': {'Steel': 50.0, 'Electronics': 20.0},
                'tariff': {'Steel': 0.0, 'Electronics': 0.0},
                'reliability': 0.99
            },
            'China': {
                'FX': 0.14,
                'base_price': {'Steel': 3000.0, 'Electronics': 1400.0},
                'shipping_cost': {'Steel': 100.0, 'Electronics': 60.0},
                'tariff': {'Steel': 0.05, 'Electronics': 0.05},
                'reliability': 0.95
            },
            'Mexico': {
                'FX': 0.05,
                'base_price': {'Steel': 12000.0, 'Electronics': 5000.0},
                'shipping_cost': {'Steel': 70.0, 'Electronics': 50.0},
                'tariff': {'Steel': 0.0, 'Electronics': 0.0},
                'reliability': 0.97
            }
        }
    }
    return data
