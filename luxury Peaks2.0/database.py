from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_data()
        

    # Predefined Rooms
def seed_data():
    from model import db, Room, RestaurantItem, Service, GameStoreItem, FashionStoreItem, SouvenirItem
    # Clear existing data 
    db.session.query(Room).delete() 
    db.session.query(RestaurantItem).delete() 
    db.session.query(Service).delete() 
    db.session.query(GameStoreItem).delete() 
    db.session.query(FashionStoreItem).delete() 
    db.session.query(SouvenirItem).delete()
    
    #seeding the data
    rooms = [
        Room(room_type='Twin Bed', price_per_night=2000.0, description='Comfortable twin bed room', image_url='images/rooms/Twin_bed.jpg'),
        Room(room_type='Standard', price_per_night=4000.0, description='Spacious standard room with amenities', image_url='images/rooms/Standard.jpg'),
        Room(room_type='Deluxe', price_per_night=10000.0, description='Deluxe room with balcony view', image_url='images/rooms/Deluxe.jpg'),
        Room(room_type='Suite', price_per_night=17000.0, description='Luxury suite with living area', image_url='images/rooms/Suite.jpg'),
        Room(room_type='Presidential', price_per_night=25000.0, description='Top-tier suite with exclusive services', image_url='images/rooms/Presidential.jpg')
    ]
    

    # Predefined Restaurant Items
    restaurant_items = [
        # Main Courses
        RestaurantItem(name='Butter Panner Masala', cuisine='Indian', price=200.0, description='Creamy butter panner with spices', image_url='/static/images/restaurant/butter_panner.jpg'),
        RestaurantItem(name='Pad Thai', cuisine='Thai', price=150.0, description='Traditional Thai stir-fried noodles', image_url='/static/images/restaurant/pad_thai.jpg'),
        # Soups
        RestaurantItem(name='Tom Yum Soup', cuisine='Thai', price=60.0, description='Spicy Thai soup with tofu', image_url='/static/images/restaurant/tom_yum.jpg'),
        RestaurantItem(name='Minestrone', cuisine='Italian', price=70.0, description='Vegetable-rich Italian soup', image_url='/static/images/restaurant/minestrone.jpg'),
        # Starters
        RestaurantItem(name='Spring Rolls', cuisine='Chinese', price=100.0, description='Crispy vegetable spring rolls', image_url='/static/images/restaurant/spring_rolls.jpg'),
        RestaurantItem(name='Panner Tikka', cuisine='Indian', price=180.0, description='Marinated panner skewers', image_url='/static/images/restaurant/panner_tikka.jpg'),
        # Desserts
        RestaurantItem(name='Gulab Jamun', cuisine='Indian', price=40.0, description='Sweet milk-solid-based dessert', image_url='/static/images/restaurant/gulab_jamun.jpg'),
        RestaurantItem(name='Cheesecake', cuisine='American', price=80.0, description='Creamy cheesecake', image_url='/static/images/restaurant/cheesecake.jpg')
    ]
    

    # Predefined Services
    services = [
        Service(name='Spa - Relaxing', service_type='Spa', price=250.0, description='A relaxing spa experience'),
        Service(name='Massage - Head', service_type='Massage', price=230.0, description='Soothing head massage'),
        Service(name='Camping', service_type='Outdoor', price=1000.0, description='Camping trip with guide'),
        Service(name='Travel Advisory - 1 Day', service_type='Travel', price=1500.0, description='One-day travel advisory service'),
        Service(name='Bonfire', service_type='Outdoor', price=200.0, description='Evening bonfire setup')
    ]
    

    # Predefined Game Store Items
    game_store_items = [
        GameStoreItem(name='God of War Ragnarok', category='PS5', price=2600.0, description='Latest God of War title', image_url='/static/images/games/god_of_war_ragnarok.jpg'),
        GameStoreItem(name='FIFA 23', category='PC', price=1500.0, description='Popular soccer game', image_url='/static/images/games/fifa_23.jpg'),
        GameStoreItem(name='Xbox Series X Console', category='Consoles', price=49000.0, description='High-performance gaming console', image_url='/static/images/games/xbox_series_x.jpg'),
        GameStoreItem(name='MacBook Pro', category='Laptops', price=106000.0, description='High-performance Apple laptop', image_url='/static/images/games/macbook_pro.jpg')
    ]
    

    # Predefined Fashion Store Items
    fashion_store_items = [
        FashionStoreItem(name='Men\'s Tuxedo', category='Men', price=150.0, description='Elegant tuxedo for men', image_url='/static/images/fashion/mens_tuxedo.jpg'),
        FashionStoreItem(name='Women\'s Evening Gown', category='Women', price=200.0, description='Classy evening gown', image_url='/static/images/fashion/evening_gown.jpg'),
        FashionStoreItem(name='Children\'s Formal Wear', category='Children', price=50.0, description='Stylish children\'s formal wear', image_url='/static/images/fashion/child_formal.jpg')
    ]
    

    # Predefined Souvenir Items
    souvenir_items = [
        SouvenirItem(name='Wooden Elephant Carving', category='Artifacts', price=30.0, description='Hand-carved wooden elephant', image_url='/static/images/souvenirs/wooden_elephant.jpg'),
        SouvenirItem(name='Silver Photo Frame', category='Home Decor', price=40.0, description='Decorative silver photo frame', image_url='/static/images/souvenirs/photo_frame.jpg'),
        SouvenirItem(name='Vintage Compass', category='Antiques', price=80.0, description='Antique brass compass', image_url='/static/images/souvenirs/compass.jpg')
    ]
    
    db.session.bulk_save_objects(rooms)
    db.session.bulk_save_objects(restaurant_items)
    db.session.bulk_save_objects(services)
    db.session.bulk_save_objects(game_store_items)
    db.session.bulk_save_objects(fashion_store_items)
    db.session.bulk_save_objects(souvenir_items)
    db.session.commit()
    print("Database seeded with predefined data.")
