from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app import db



class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    image_filename = Column(String(255), nullable=True)  # Champ pour l'image

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "quantity": self.quantity,
            "category": self.category,
            "date": self.date.isoformat(),
            "image_filename": self.image_filename
        }
