from orchestrator import Orchestrator

orchestrator = Orchestrator()

def run_agent(user_input: str):
    result = orchestrator.route(user_input)

    if isinstance(result, list):
        if not result:
            return "No products found."

        response = "Here are some results:\n"
        for name, brand, price, stock in result:
            response += f"- {name} ({brand}) – ₹{price}, Stock: {stock}\n"
        return response

    return result
