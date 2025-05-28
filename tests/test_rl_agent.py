import pytest
from ingest.data_ingestion import load_initial_data
from simulation.arbitrage_env import ArbitrageEnv
from agent.rl_agent import RLAgent
from forecasting.price_forecaster import PriceForecaster

@pytest.fixture
def setup_agent():
    data = load_initial_data()
    env = ArbitrageEnv(data)
    pf = PriceForecaster()
    return RLAgent(env, pf), env

def test_generate_actions_length(setup_agent):
    agent, env = setup_agent
    actions = agent._generate_all_actions()
    expected_count = len(env.regions) ** len(env.materials)
    assert len(actions) == expected_count

def test_decide_action_valid(setup_agent):
    agent, env = setup_agent
    action, adjusted, risky = agent.decide_action(env.current_prices)
    # Action keys match materials
    assert set(action.keys()) == set(env.materials)
    # All regions in action are valid
    for region in action.values():
        assert region in env.regions
    assert isinstance(adjusted, bool)
    assert (risky is None) or (risky in env.regions)

def test_last_action_set(setup_agent):
    agent, env = setup_agent
    action, *_ = agent.decide_action(env.current_prices)
    assert agent.last_action == action