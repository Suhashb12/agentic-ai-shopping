from agents.product_agent import ProductAgent
from agents.recommend_agent import RecommendationAgent
from agents.order_agent import OrderAgent

class Orchestrator:
    def __init__(self):
        self.product_agent = ProductAgent()
        self.recommend_agent = RecommendationAgent()
        self.order_agent = OrderAgent()

    def route(self, user_input: str):
        text = user_input.lower()

        if "buy" in text or "order" in text:
            return self.order_agent.handle(user_input)

        if "recommend" in text or "similar" in text:
            return self.recommend_agent.handle(user_input)

        return self.product_agent.handle(user_input)
