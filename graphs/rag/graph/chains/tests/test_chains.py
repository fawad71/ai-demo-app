from pprint import pprint

from langgraph.rag.graph.chains.retrieval_grader import retrieval_grader, GradeDocuments
from langgraph.rag.graph.chains.generation import generation_chain
from langgraph.rag.graph.nodes.retrieve import retriever
from langgraph.rag.graph.chains.hallucination_grader import hallucination_grader, GradeHallucinations
from langgraph.rag.graph.chains.router import question_router, RouteQuery

def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    documents = retriever.invoke(question)
    doc_txt = documents[1].page_content
    
    res: GradeDocuments = retrieval_grader.invoke({"question": question, "document": doc_txt})
    
    assert res.binary_score == "yes"
    
def test_retrieval_grader_answer_no() -> None:
    question = "how to make Pizza?"
    documents = retriever.invoke(question)
    doc_txt = documents[1].page_content
    
    res: GradeDocuments = retrieval_grader.invoke({"question": question, "document": doc_txt})
    
    assert res.binary_score == "no"
    
def test_generation_chain() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question": question})
    pprint(generation)
    
def test_hallucination_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"context": docs, "question": question})
    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )
    assert res.binary_score


def test_hallucination_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    res: GradeHallucinations = hallucination_grader.invoke(
        {
            "documents": docs,
            "generation": "In order to make pizza we need to first start with the dough",
        }
    )
    assert not res.binary_score


def test_router_to_vectorstore() -> None:
    question = "agent memory"

    res: RouteQuery = question_router.invoke({"question": question})
    assert res.datasource == "vectorstore"


def test_router_to_websearch() -> None:
    question = "how to make pizza"

    res: RouteQuery = question_router.invoke({"question": question})
    assert res.datasource == "websearch"