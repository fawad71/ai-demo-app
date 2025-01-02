from typing import Any, Dict
from graphs.rag.graph.state import GraphState
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

retriever = Chroma(
    collection_name="rag-chroma",
    embedding_function=embeddings,
    persist_directory=".chroma",
).as_retriever()

def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Retrieves the documents from the vector store.
    """
    print("--- Retrieving documents ---")

    question = state["question"]
    documents = retriever.invoke(question)

    return {"documents": documents, "question": question}
