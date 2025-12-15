from tools.sql_tool import search_products

class RecommendationAgent:
    def handle(self, user_input: str):
        # very simple heuristic for now
        words = user_input.lower().split()
        keyword = words[-1]
        return search_products(keyword)
