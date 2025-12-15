from tools.sql_tool import search_products, products_under_price

class ProductAgent:
    def handle(self, user_input: str):
        if "under" in user_input.lower():
            price = int("".join(filter(str.isdigit, user_input)))
            return products_under_price(price)
        return search_products(user_input)
