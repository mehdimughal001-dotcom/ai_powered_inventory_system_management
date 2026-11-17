from datetime import datetime

class Product:
    def __init__(self, product_id, name, category, price, quantity, reorder_level, description=""):
        self.product_id = str(product_id)
        self.name = str(name)
        self.category = str(category)
        self.price = float(price)
        self.quantity = int(quantity)
        self.reorder_level = int(reorder_level)
        self.description = str(description)

    def calculate_total_value(self):
        return self.price * self.quantity

    def check_stock_status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= self.reorder_level:
            return "Low Stock"
        return "In Stock"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "description": self.description,
            "type": "standard",
            "total_value": self.calculate_total_value(),
            "status": self.check_stock_status()
        }


class PerishableProduct(Product):
    def __init__(self, product_id, name, category, price, quantity, reorder_level, description="", expiry_date=""):
        super().__init__(product_id, name, category, price, quantity, reorder_level, description)
        self.expiry_date = str(expiry_date)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "perishable"
        data["expiry_date"] = self.expiry_date
        return data
