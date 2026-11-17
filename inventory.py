import json
import os
from models import Product, PerishableProduct

class InventoryManager:
    def __init__(self, data_file="data/products.json"):
        self.data_file = data_file
        self.products = {}
        self.load_inventory()

    def load_inventory(self):
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            sample_data = [
                {
                    "product_id": "P001",
                    "name": "Organic Whole Milk",
                    "category": "Dairy",
                    "price": 3.49,
                    "quantity": 15,
                    "reorder_level": 20,
                    "description": "Fresh organic whole milk from local pasture-raised cows.",
                    "type": "perishable",
                    "expiry_date": "2026-06-15"
                },
                {
                    "product_id": "P002",
                    "name": "Artisanal Sourdough Bread",
                    "category": "Bakery",
                    "price": 5.99,
                    "quantity": 8,
                    "reorder_level": 10,
                    "description": "Handcrafted fermented sourdough bread baked daily.",
                    "type": "perishable",
                    "expiry_date": "2026-06-10"
                },
                {
                    "product_id": "P003",
                    "name": "Stainless Steel Water Bottle",
                    "category": "Accessories",
                    "price": 24.99,
                    "quantity": 45,
                    "reorder_level": 10,
                    "description": "Insulated double-wall stainless steel bottle keeping drinks cold for 24h.",
                    "type": "standard",
                    "expiry_date": ""
                },
                {
                    "product_id": "P004",
                    "name": "Organic Green Tea Bags",
                    "category": "Beverages",
                    "price": 12.50,
                    "quantity": 0,
                    "reorder_level": 15,
                    "description": "Premium Japanese green tea bags rich in antioxidants.",
                    "type": "standard",
                    "expiry_date": ""
                },
                {
                    "product_id": "P005",
                    "name": "Wireless Ergonomic Mouse",
                    "category": "Electronics",
                    "price": 39.99,
                    "quantity": 25,
                    "reorder_level": 5,
                    "description": "Comfortable wireless mouse with adjustable DPI and silent clicks.",
                    "type": "standard",
                    "expiry_date": ""
                }
            ]
            with open(self.data_file, 'w') as f:
                json.dump(sample_data, f, indent=4)

        try:
            with open(self.data_file, 'r') as f:
                items = json.load(f)
                self.products = {}
                for item in items:
                    if item.get("type") == "perishable":
                        p = PerishableProduct(
                            product_id=item["product_id"],
                            name=item["name"],
                            category=item["category"],
                            price=item["price"],
                            quantity=item["quantity"],
                            reorder_level=item["reorder_level"],
                            description=item.get("description", ""),
                            expiry_date=item.get("expiry_date", "")
                        )
                    else:
                        p = Product(
                            product_id=item["product_id"],
                            name=item["name"],
                            category=item["category"],
                            price=item["price"],
                            quantity=item["quantity"],
                            reorder_level=item["reorder_level"],
                            description=item.get("description", "")
                        )
                    self.products[p.product_id] = p
        except Exception as e:
            print(f"Error loading inventory: {e}")
            self.products = {}

    def save_inventory(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            data = [p.to_dict() for p in self.products.values()]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving inventory: {e}")

    def add_product(self, data):
        product_id = data.get("product_id")
        if not product_id:
            return False, "Product ID is required."
        if product_id in self.products:
            return False, f"Product ID {product_id} already exists."
        
        p_type = data.get("type", "standard")
        try:
            if p_type == "perishable":
                product = PerishableProduct(
                    product_id=product_id,
                    name=data["name"],
                    category=data["category"],
                    price=data["price"],
                    quantity=data["quantity"],
                    reorder_level=data["reorder_level"],
                    description=data.get("description", ""),
                    expiry_date=data.get("expiry_date", "")
                )
            else:
                product = Product(
                    product_id=product_id,
                    name=data["name"],
                    category=data["category"],
                    price=data["price"],
                    quantity=data["quantity"],
                    reorder_level=data["reorder_level"],
                    description=data.get("description", "")
                )
            self.products[product_id] = product
            self.save_inventory()
            return True, "Product added successfully."
        except Exception as e:
            return False, str(e)

    def update_product(self, product_id, data):
        if product_id not in self.products:
            return False, "Product not found."
        
        try:
            existing = self.products[product_id]
            p_type = data.get("type", existing.to_dict().get("type", "standard"))
            
            name = data.get("name", existing.name)
            category = data.get("category", existing.category)
            price = float(data.get("price", existing.price))
            quantity = int(data.get("quantity", existing.quantity))
            reorder_level = int(data.get("reorder_level", existing.reorder_level))
            description = data.get("description", existing.description)
            
            if p_type == "perishable":
                expiry_date = data.get("expiry_date", getattr(existing, "expiry_date", ""))
                product = PerishableProduct(product_id, name, category, price, quantity, reorder_level, description, expiry_date)
            else:
                product = Product(product_id, name, category, price, quantity, reorder_level, description)
            
            self.products[product_id] = product
            self.save_inventory()
            return True, "Product updated successfully."
        except Exception as e:
            return False, str(e)

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_inventory()
            return True, "Product deleted successfully."
        return False, "Product not found."

    def get_product(self, product_id):
        if product_id in self.products:
            return self.products[product_id].to_dict()
        return None

    def get_all_products(self):
        return [p.to_dict() for p in self.products.values()]

    def search_products(self, query):
        query = query.lower()
        results = []
        for p in self.products.values():
            if (query in p.product_id.lower() or 
                query in p.name.lower() or 
                query in p.category.lower() or
                query in p.description.lower()):
                results.append(p.to_dict())
        return results

    def get_statistics(self):
        products = self.get_all_products()
        total_products = len(products)
        total_units = sum(p["quantity"] for p in products)
        total_value = sum(p["total_value"] for p in products)
        
        low_stock = sum(1 for p in products if p["status"] == "Low Stock")
        out_of_stock = sum(1 for p in products if p["status"] == "Out of Stock")
        
        return {
            "total_products": total_products,
            "total_units": total_units,
            "total_value": round(total_value, 2),
            "low_stock_count": low_stock,
            "out_of_stock_count": out_of_stock
        }
