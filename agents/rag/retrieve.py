from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def retrieve(query):
    print("Retrieving data...")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(model="gpt-4o")

    vectorstore = Chroma(
        collection_name="medium-blog",
        embedding_function=embeddings,
        persist_directory="./chroma_db_blog",
    )

    retrieval_qa_chat_prompt = hub.pull("common-rag")

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    result = retrieval_chain.invoke({"input": query})

    return result["answer"]
