from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings

if __name__ == "__main__":
    print("Ingesting Data")
    loader = TextLoader("agents/rag-agent/docs/vector-db-blog.txt")
    data = loader.load()

    print("splitting data")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    chunks = text_splitter.split_documents(data)

    print(f"Loaded {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print("embedding data")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="medium-blog",
        persist_directory="./chroma_db_blog",
    )

    print("Data ingested successfully")
