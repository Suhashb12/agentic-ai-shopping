from tools.sql_tool import search_products, products_under_price

class ProductAgent:
    def handle(self, user_input: str):
        text = user_input.lower()

        if "under" in text:
            price = int("".join(filter(str.isdigit, text)))
            return products_under_price(price)

        return search_products(user_input)
