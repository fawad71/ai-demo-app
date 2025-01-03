from graphs.rag.graph.graph import app
from pprint import pprint

if __name__ == "__main__":
    user_input = input("Enter your prompt: ")
    response = app.invoke(input={"question": user_input, "documents": []})
    pprint(response["generation"])