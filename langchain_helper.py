from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
from langchain.document_loaders import DirectoryLoader
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate


def generate_answer_by_question(question):
    load_dotenv()
    
    documents = DirectoryLoader('./documents/').load()

    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', '?', ' '],
        chunk_size = 300,
        chunk_overlap = 50,
    )
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    # Create vectors
    vectorstore = FAISS.from_documents(texts, embeddings)
    # Persist the vectors locally on disk
    vectorstore.save_local("faiss_index_db")
    # Load from local storage
    db = FAISS.load_local("faiss_index_db", embeddings, allow_dangerous_deserialization=True)
    # question = "What is HTML?"

    docs = db.similarity_search_with_score(query = question, k = 5)

    semantic_results = []
    for doc in docs:
        doc, score = doc
        semantic_results.append(doc.page_content)

    llm = OpenAI(temperature=1)
    prompt = ChatPromptTemplate.from_template(
        f"""
        Answer the question based only on the following list of context:
        {semantic_results}
    Question: {question}
    """
    )

    chain = prompt | llm
    answer = chain.invoke({})

    return answer

if __name__ == "__main__":
    print(generate_answer_by_question("What is HTML?"))
