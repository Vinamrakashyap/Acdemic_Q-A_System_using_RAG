from retriever_creation_7 import retriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = PromptTemplate(
    template="""You are a strict academic exam assistant. Your job is to write a comprehensive, well-structured answer using ONLY the provided PPT slide context.

CRITICAL RULES (MUST FOLLOW):
1. ZERO OUTSIDE KNOWLEDGE: Rely EXCLUSIVELY on the provided Context. Do NOT bring in external textbook facts, assumptions, or general efficiency numbers. If the PPT reports a lower efficiency (e.g., 10–13%) than standard textbooks, strictly state ONLY what is in the Context.
2. PRESERVE ALL NUMERICAL DATA: Include every exact temperature, boiling point, pressure, efficiency range, and technical specification mentioned in the Context.
3. EXPLAIN DIAGRAMS STEP-BY-STEP: Using the diagram details and slide text, explain the working principle and role of every component (e.g., separator, turbine, condenser, generator, heat exchanger, working fluid) in logical sequence.
4. EXPLICITLY FLAG MISSING INFO: If any requested detail or sub-concept is not present in the Context, clearly state: "Not mentioned in the provided slides."
5. 10-MARK EXAM STRUCTURE:
   - **Introduction / Definition**
   - **Types / Classifications** (with exact operating conditions & efficiencies)
   - **Working Principle & Diagram Component Flow** (numbered step-by-step)
   - **Comparison Table** (if multiple systems/cycles are covered in the context)

Context:
{context}

Question:
{question}

Structured Exam Answer:""",
    input_variables=["context", "question"]
)

parser = StrOutputParser()
chain = prompt | llm | parser

if __name__ == "__main__":
    query = input("Ask your query: ")
    results = retriever.invoke(query)

    # Debug toggle: Retrieved chunks dekhne ke liye True karein
    SHOW_RETRIEVED_CHUNKS = False
    if SHOW_RETRIEVED_CHUNKS:
        print("\n--- RETRIEVED CONTEXT ---")
        for i, doc in enumerate(results, 1):
            print(f"\n[Chunk {i} | Slide {doc.metadata.get('page_number')}]")
            print(doc.page_content)
        print("-------------------------\n")

    final_retrieved_result = "\n\n---\n\n".join([doc.page_content for doc in results])

    response = chain.invoke({
        "context": final_retrieved_result,
        "question": query
    })

    print("\nAnswer:\n")
    print(response)