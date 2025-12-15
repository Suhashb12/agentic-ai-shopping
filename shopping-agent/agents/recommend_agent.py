from tools.sql_tool import search_products

class RecommendationAgent:
    def handle(self, user_input: str):
        # simple heuristic for now
        keywords = user_input.split()
        return search_products(keywords[-1])
