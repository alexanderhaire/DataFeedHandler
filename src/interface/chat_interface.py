"""
Chat Interface
Defines ChatInterface to explain plans in natural language.
"""
class ChatInterface:
    def __init__(self):
        raise NotImplementedError("Initialize your templates here")

    def explain_plan(self, plan, cost_breakdown, **kwargs):
        """
        Generate a human-friendly explanation of the plan.
        :param plan: dict(material -> region)
        :param cost_breakdown: detailed cost info
        :return: explanation string
        """
        raise NotImplementedError("Replace with your explanation logic")
