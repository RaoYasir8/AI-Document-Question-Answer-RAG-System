from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.config import settings
from app.vector_store import get_retriever


SYSTEM_PROMPT = """
You are an AI document question-answering assistant.
Use only the provided document context to answer the user's question.

Rules:
1. Answer accurately using the retrieved context.
2. If the answer is not present in the context, say:
   "I could not find this information in the uploaded documents."
3. Do not invent facts.
4. Keep the answer clear and helpful.
5. Mention when the answer is based on limited context.

Context:
{context}
"""


# Initialize LLM
llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model=settings.GROQ_MODEL,
    temperature=0.2,
    max_tokens=1024,
)


# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)


# Chains
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(
    get_retriever(),
    document_chain
)


async def answer_question(question: str) -> dict:
    result = await retrieval_chain.ainvoke({"input": question})

    answer = result.get("answer", "I could not generate an answer.")
    context_documents = result.get("context", [])

    sources = []

    for doc in context_documents:
        sources.append(
            {
                "content": doc.page_content[:500],
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }