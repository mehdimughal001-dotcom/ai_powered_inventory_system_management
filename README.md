# AI-Powered Inventory Management System (StockPulse AI)

An intelligent inventory management application built with **Python, Flask, Object-Oriented Programming (OOP)**, and **Generative AI (Groq API)**.

## Features
- **Complete Inventory CRUD:** Add, read, update, delete, and search products in real time.
- **OOP Architecture:** Clean inheritance structure (`Product` and `PerishableProduct`), managed by `InventoryManager` and `InventoryAI`.
- **Dashboard Analytics:** Live tracking of total products, total units, total inventory value, low-stock alerts, and out-of-stock items.
- **Generative AI Capabilities (Groq API):**
  - **AI Inventory Analysis:** Executive health summary and risk evaluation.
  - **Smart Reorder Suggestions:** Automated reorder quantity recommendations.
  - **AI Inventory Assistant:** Natural-language Q&A chatbot grounded in your live inventory.
  - **AI Description Generator:** Automatic copywriting when adding/editing products.

## Local Installation & Setup

1. **Extract the project folder and navigate into it:**
   ```bash
   cd stockpulse-ai-inventory
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   Copy `.env.example` to `.env` and add your Groq API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```
5. **Run the application:**
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:5000`.

## GitHub Upload Instructions
```bash
git init
git add .
git commit -m "Initial commit: AI Inventory System"
git branch -M main
git remote add origin https://github.com/your-username/ai-inventory-system.git
git push -u origin main
```

## Vercel Deployment Instructions
1. Import your GitHub repository to [Vercel](https://vercel.com).
2. Configure Environment Variables in Vercel project settings:
   - `GROQ_API_KEY`: Your Groq API key
   - `GROQ_MODEL`: `llama-3.3-70b-versatile`
3. Click **Deploy**. Vercel uses `vercel.json` to configure the Python runtime and launch your Flask application.
*(Note: For long-term production persistence on Vercel, connect `InventoryManager` to PostgreSQL or Supabase instead of local JSON storage.)*
