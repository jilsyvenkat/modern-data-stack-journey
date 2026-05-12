import ollama
import json
from datetime import datetime

print("AI-Powered Analytics Pipeline")
print("=" * 60)
print("Simulating Snowflake Cortex outputs with local Ollama")
print("=" * 60)

# simulated Cortex outputs
# in production these come directly from Snowflake SQL
cortex_results = {
    "run_date": datetime.now().isoformat(),
    "feedback_analysis": [
        {
            "feedback_id": 1,
            "customer": "Michael P",
            "product": "Laptop",
            "sentiment_score": 0.92,
            "sentiment_label": "POSITIVE",
            "summary": "Customer very satisfied with laptop purchase",
            "category": "positive experience"
        },
        {
            "feedback_id": 2,
            "customer": "Shawn M",
            "product": "Phone",
            "sentiment_score": -0.87,
            "sentiment_label": "NEGATIVE",
            "summary": "Poor battery life and unhelpful customer service",
            "category": "customer service complaint"
        },
        {
            "feedback_id": 3,
            "customer": "Katharine R",
            "product": "Tablet",
            "sentiment_score": 0.12,
            "sentiment_label": "NEUTRAL",
            "summary": "Acceptable product with slow delivery",
            "category": "delivery problem"
        },
        {
            "feedback_id": 4,
            "customer": "Michael P",
            "product": "Keyboard",
            "sentiment_score": 0.95,
            "sentiment_label": "POSITIVE",
            "summary": "Outstanding service and product quality",
            "category": "positive experience"
        },
        {
            "feedback_id": 5,
            "customer": "Shawn M",
            "product": "Mouse",
            "sentiment_score": -0.94,
            "sentiment_label": "NEGATIVE",
            "summary": "Product failed after two weeks, no resolution",
            "category": "refund request"
        }
    ],
    "anomalies_detected": [
        {
            "date": "2024-01-07",
            "order_count": 150,
            "expected": 50,
            "type": "SPIKE",
            "deviation": "+200%"
        },
        {
            "date": "2024-01-14",
            "order_count": 5,
            "expected": 50,
            "type": "DROP",
            "deviation": "-90%"
        }
    ]
}

# use Ollama to generate executive report
prompt = f"""
You are a Chief Data Officer preparing a weekly AI analytics
report for the board. Use ONLY the data provided below.

CORTEX ANALYTICS RESULTS:
{json.dumps(cortex_results, indent=2)}

Write a board-level report with:
1. CUSTOMER SENTIMENT SUMMARY (overall health, key issues)
2. ANOMALIES REQUIRING ATTENTION (business impact)
3. TOP 3 RECOMMENDED ACTIONS (specific, prioritised)
4. DATA QUALITY NOTES

Keep under 300 words. Be direct and business-focused.
"""

print("\nGenerating executive report using local LLM...")
print("(Simulating Snowflake Cortex + Ollama integration)")
print("-" * 60)

response = ollama.chat(
    model='llama3.2',
    messages=[
        {
            'role': 'system',
            'content': """You are a Chief Data Officer who writes
            clear, concise board reports. You translate data
            insights into business actions. No technical jargon."""
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]
)

print("\nAI ANALYTICS EXECUTIVE REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)
print(response['message']['content'])
print("=" * 60)

# summary statistics
positive = len([f for f in cortex_results['feedback_analysis']
                if f['sentiment_label'] == 'POSITIVE'])
negative = len([f for f in cortex_results['feedback_analysis']
                if f['sentiment_label'] == 'NEGATIVE'])
neutral  = len([f for f in cortex_results['feedback_analysis']
                if f['sentiment_label'] == 'NEUTRAL'])

print(f"\nSENTIMENT BREAKDOWN:")
print(f"  Positive: {positive}/5 ({positive*20}%)")
print(f"  Negative: {negative}/5 ({negative*20}%)")
print(f"  Neutral:  {neutral}/5  ({neutral*20}%)")
print(f"\nANOMALIES: {len(cortex_results['anomalies_detected'])} detected")
print(f"\nPipeline: Snowflake Cortex → Python → Ollama → Board Report")
