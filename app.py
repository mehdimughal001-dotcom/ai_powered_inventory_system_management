import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from inventory import InventoryManager
from ai_helper import InventoryAI

load_dotenv()

app = Flask(__name__)

# Note: On Vercel serverless functions, local filesystem is read-only except /tmp
DATA_PATH = "/tmp/products.json" if os.environ.get("VERCEL") else "data/products.json"
inventory_manager = InventoryManager(data_file=DATA_PATH)
inventory_ai = InventoryAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = inventory_manager.get_statistics()
    return jsonify(stats)

@app.route('/api/products', methods=['GET'])
def get_products():
    query = request.args.get('search', '')
    if query:
        products = inventory_manager.search_products(query)
    else:
        products = inventory_manager.get_all_products()
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    success, message = inventory_manager.add_product(data)
    if success:
        return jsonify({"success": True, "message": message}), 201
    return jsonify({"success": False, "message": message}), 400

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    success, message = inventory_manager.update_product(product_id, data)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 400

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    success, message = inventory_manager.delete_product(product_id)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"success": False, "message": message}), 404

# AI Endpoints
@app.route('/api/ai/analyze', methods=['POST'])
def ai_analyze():
    products = inventory_manager.get_all_products()
    summary = json.dumps(products, indent=2)
    analysis = inventory_ai.analyze_inventory(summary)
    return jsonify({"analysis": analysis})

@app.route('/api/ai/reorder', methods=['POST'])
def ai_reorder():
    products = inventory_manager.get_all_products()
    summary = json.dumps(products, indent=2)
    suggestions = inventory_ai.get_reorder_suggestions(summary)
    return jsonify({"suggestions": suggestions})

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    products = inventory_manager.get_all_products()
    summary = json.dumps(products, indent=2)
    answer = inventory_ai.answer_query(question, summary)
    return jsonify({"answer": answer})

@app.route('/api/ai/generate-description', methods=['POST'])
def ai_generate_description():
    data = request.get_json()
    name = data.get("name", "")
    category = data.get("category", "")
    info = data.get("additional_info", "")
    description = inventory_ai.generate_description(name, category, info)
    return jsonify({"description": description})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
