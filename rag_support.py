"""
Claude RAG Support Bot
Answers customer questions by first retrieving the most relevant
knowledge base article, then having Claude answer grounded in that
content only — instead of guessing from general knowledge.
"""

import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def retrieve_relevant_doc(question: str, knowledge_base: list) -> dict:
    """
    Simple keyword-overlap retrieval: scores each doc by how many
    question words appear in its content, returns the best match.
    (A production system would use embeddings/vector search instead —
    this keeps the demo dependency-free and easy to read.)
    """
    question_words = set(question.lower().split())
    best_doc = None
    best_score = 0

    for doc in knowledge_base:
        doc_words = set(doc["content"].lower().split())
        score = len(question_words & doc_words)
        if score > best_score:
            best_score = score
            best_doc = doc

    return best_doc or knowledge_base[0]


def answer_question(question: str, knowledge_base: list) -> str:
    relevant_doc = retrieve_relevant_doc(question, knowledge_base)

    system_prompt = (
        "You are a customer support assistant. Answer the customer's "
        "question using ONLY the reference article below. If the "
        "article doesn't contain the answer, say you don't have that "
        "information and suggest contacting human support.\n\n"
        f"Reference article — {relevant_doc['title']}:\n{relevant_doc['content']}"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
    )

    return response.content[0].text


if __name__ == "__main__":
    with open("knowledge_base.json") as f:
        kb = json.load(f)

    with open("sample_questions.json") as f:
        questions = json.load(f)

    for q in questions:
        print(f"\nQuestion: {q['question']}")
        answer = answer_question(q["question"], kb)
        print("Answer:", answer)
