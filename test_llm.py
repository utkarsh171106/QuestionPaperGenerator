from llm import generate_questions

prompt = """
Generate 5 questions about Object Oriented Programming.
Give questions suitable for a university examination.
"""

result = generate_questions(prompt)

print("\nRESULT:\n")
print(result)