import os
from groq import Groq

class InventoryAI:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")

    def _call_groq(self, prompt, system_prompt="You are an expert AI inventory management assistant."):
        if not self.client:
            return "Groq API key is not configured. Please set GROQ_API_KEY in your environment variables to enable AI intelligence features."
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with Groq API: {str(e)}"

    def analyze_inventory(self, products_summary):
        prompt = f"""
Analyze the following inventory data and provide strategic insights, stock health evaluation, and operational recommendations:

Inventory Data:
{products_summary}

Please structure your response with:
1. Executive Summary of Inventory Health
2. Key Risks (Low stock or out of stock items)
3. Efficiency Recommendations
"""
        return self._call_groq(prompt)

    def get_reorder_suggestions(self, products_summary):
        prompt = f"""
Based on the following inventory records, identify items that need reordering and recommend optimal reorder quantities based on reorder levels and current stock:

Inventory Data:
{products_summary}

Provide a clear list of products needing reorder with recommended quantities and urgency levels.
"""
        return self._call_groq(prompt)

    def answer_query(self, question, products_summary):
        prompt = f"""
You are an intelligent inventory assistant. Answer the user's question accurately based ONLY on the provided inventory data. If the answer cannot be found in the data, state that clearly.

Inventory Data:
{products_summary}

User Question: {question}
"""
        return self._call_groq(prompt)

    def generate_description(self, name, category, additional_info=""):
        prompt = f"""
Generate a professional, compelling, and concise product description (2-3 sentences) suitable for an e-commerce or inventory catalog based on the following details:
- Product Name: {name}
- Category: {category}
- Additional Details: {additional_info}
"""
        return self._call_groq(prompt, "You are a professional copywriter and product catalog expert.")
