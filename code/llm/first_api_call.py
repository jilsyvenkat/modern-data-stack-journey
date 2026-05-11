import ollama

response = ollama.chat(
    model='llama3.2',
    messages=[
        {
            'role': 'system',
            'content': """You are a senior data engineering expert
            with 20 years of experience across Banking, Finance,
            Insurance and Healthcare. You give concise, practical
            answers focused on real-world enterprise data platforms."""
        },
        {
            'role': 'user',
            'content': """In 3 bullet points, what are the most
            important things a Head of Data should know about
            Apache Iceberg in 2026?"""
        }
    ]
)

print("=" * 60)
print("Response from Llama 3.2 (via Ollama):")
print("=" * 60)
print(response['message']['content'])
print("=" * 60)
print("Model: llama3.2 (running locally — no API cost)")
