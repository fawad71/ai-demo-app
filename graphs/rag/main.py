from graphs.rag.graph.graph import app
from pprint import pprint

if __name__ == "__main__":
    response = app.invoke(input={"question": "how to make pizza?", "documents": []})
    pprint(response["generation"])
