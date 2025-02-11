from langgraph.graph import START,END, StateGraph

from graphs.rag.graph.consts import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEBSEARCH, ROUTER
from graphs.rag.graph.nodes import generate, grade_documents, retrieve, web_search
from graphs.rag.graph.state import GraphState
from graphs.rag.graph.chains.answer_grader import answer_grader
from graphs.rag.graph.chains.hallucination_grader import hallucination_grader
from graphs.rag.graph.chains.router import question_router, RouteQuery

def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["web_search"]:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return 'some docs are not relevant'
    else:
        print("---DECISION: GENERATE---")
        return 'all docs are relevant'

def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"

def router(state: GraphState):
    print("---ROUTE QUESTION---")
    
def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return 'query related to web search'
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return 'query related to vectorstore'

workflow = StateGraph(GraphState)

workflow.add_node(ROUTER, router)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.add_edge(START, ROUTER)

workflow.add_conditional_edges(
    ROUTER,
    route_question,
    {
        'query related to web search': WEBSEARCH,
        'query related to vectorstore': RETRIEVE,
    },
)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        'some docs are not relevant': WEBSEARCH,
        'all docs are relevant': GENERATE,
    },
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": WEBSEARCH,
    },
)

workflow.add_edge(WEBSEARCH, GENERATE)

workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graphs/rag/graph/rag_graph.png")