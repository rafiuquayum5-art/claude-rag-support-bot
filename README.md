# Claude RAG Support Bot

An AI customer support agent that answers questions by first retrieving the most relevant piece of internal documentation, then having Claude answer strictly based on that content — instead of guessing from general knowledge.

## The problem this solves

Generic AI chatbots often hallucinate answers or give vague, unhelpful responses because they aren't grounded in a business's actual policies and documentation. This leads to customer frustration and support tickets that still need a human to fix. This project demonstrates a simple RAG (Retrieval-Augmented Generation) pattern that keeps answers accurate and sourced.

## How it works

1. A customer question comes in.
2. The script retrieves the most relevant article from a small knowledge base (return policy, shipping times, tracking, payment methods) using keyword matching.
3. That article is passed to Claude as grounding context, with instructions to answer only from that content — and to say so honestly if the answer isn't covered.
4. Claude returns an accurate, sourced answer instead of a generic or hallucinated one.

## Example output
