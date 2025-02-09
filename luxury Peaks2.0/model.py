from database import db

# Model for Room Booking
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<Room {self.room_type} - {self.price_per_night}>"

# Model for Restaurant Items
class RestaurantItem(db.Model):
    __tablename__ = 'restaurant_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<RestaurantItem {self.name} - {self.cuisine}>"

# Model for Additional Services (Spa, Massage, Travel, etc.)
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Service {self.name} - {self.service_type}>"

# Model for Game Store Items
class GameStoreItem(db.Model):
    __tablename__ = 'game_store_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # PC, PS, Xbox, etc.
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<GameStoreItem {self.name} - {self.category}>"

# Model for Fashion Store Items
class FashionStoreItem(db.Model):
    __tablename__ = 'fashion_store_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Men, Women, Children, etc.
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<FashionStoreItem {self.name} - {self.category}>"

# Model for Souvenir Store Items
class SouvenirItem(db.Model):
    __tablename__ = 'souvenir_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Artifact, Antique, Decor, etc.
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f"<SouvenirItem {self.name} - {self.category}>"

# Model for Customer Information
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)

    # Relationships to capture bookings and purchases made by the customer
    bookings = db.relationship('Booking', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.customer_id}>"

# Model for Bookings (Room bookings and other service records)
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # Room, Restaurant, Spa, etc.
    item_id = db.Column(db.Integer, nullable=False)  # ID of the item booked (from other tables)
    quantity = db.Column(db.Integer, default=1)
    total_cost = db.Column(db.Float, nullable=False)
    date_of_booking = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Booking {self.service_type} - {self.total_cost}>"
