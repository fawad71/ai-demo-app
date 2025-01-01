from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

if __name__ == "__main__":
    print("Ingesting Data")
    loader = TextLoader("agents/rag-agent/docs/mediumblog1.txt")
    data = loader.load()

    print("splitting data")

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(data)

    print(f"Loaded {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print("embedding data")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="medium-blog",
        persist_directory="./chroma_db"
    )

    print("Data ingested successfully")
