from flask import Flask, render_template, redirect, url_for, request, flash, session, send_file, jsonify, make_response
from config import Config
from model import db, Room, RestaurantItem, Service, GameStoreItem, FashionStoreItem, SouvenirItem, Customer
from database import init_db
from datetime import datetime
from fpdf import FPDF
import logging

app = Flask(__name__)
app.config.from_object(Config)

init_db(app)


logger = logging.getLogger('app_logger')
handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)




# Cart initialization (session-based cart dictionary)
@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {
            'rooms': [],
            'restaurant_items': [],
            'services': [],
            'game_store_items': [],
            'fashion_store_items': [],
            'souvenir_items': []
        }
# Sample data for amenities 
amenities = [ 
             {"name": "Free Wi-Fi", "icon": "fa-wifi"}, 
             {"name": "Swimming Pool", "icon": "fa-swimming-pool"}, 
             {"name": "Spa", "icon": "fa-spa"}, 
             {"name": "Gym", "icon": "fa-dumbbell"}, 
             {"name": "Restaurant", "icon": "fa-mug-saucer"},
             {"name": "Camp", "icon": "fa-campground"},
             {"name": "Travel Desk", "icon": "fa-car"},
             {"name": "Indoor Games", "icon": "fa-bowling-ball"},
             {"name": "Beach", "icon": "fa-umbrella-beach"},
             {"name": "Walking Pathway", "icon": "fa-walking"},
             {"name": "Room Service", "icon": "fa-broom"},
             {"name": "Event Hall", "icon": "fa-house"},
             {"name": "Bonfire", "icon": "fa-fire"},
             {"name": "Soccer Turf", "icon": "fa-soccer-ball"},
             {"name": "Basket Ball Indoor", "icon": "fa-basketball"},
             {"name": "WheelChair", "icon": "fa-wheelchair"},
             {"name": "Kid's Area", "icon": "fa-child"}
             ]
# Add more amenities as needed
# Homepage with hotel overview and amenities
@app.route('/')
def about_us():
    
    return render_template('about_us.html', amenities=amenities)

# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '11416':
            session['admin'] = True
            logging.info("Admin logged in successfully")
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect username or password')
            logging.warning("Admin login attempt failed")
    return render_template('admin_login.html')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    customers = Customer.query.all() # Fetch customers from the database 
    return render_template('admin_dashboard.html', customers=customers)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("You have been logged out.")
    return redirect(url_for('about_us'))

@app.route('/store')
def store():
    return render_template('store.html')

# Room Booking page
@app.route('/room_booking')
def room_booking():
    rooms = Room.query.all()
    for room in rooms: 
        print(f"Room {room.room_type}: {room.image_url}") # Debug statement to check paths 
    return render_template('room_booking.html', rooms=rooms)

# Room booking details and confirmation
@app.route('/book_room/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        email = request.form['email']
        contact_number = request.form['contact_number']
        days = int(request.form['days'])
        total_cost = room.price_per_night * days
        
        customer = Customer(customer_id=customer_id, email=email, contact_number=contact_number)
        db.session.add(customer)
        db.session.commit()

        flash(f'Room {room.room_type} booked successfully for {days} days! Total cost: {total_cost}')
        session['cart']['rooms'].append({'room_type': room.room_type, 'cost': total_cost})
        logging.info(f"Room {room.room_type} booked for {customer_id}")
        return redirect(url_for('admin_dashboard'))

    return render_template('book_room.html', room=room)

# Restaurant menu page
@app.route('/restaurant')
def restaurant():
    items = RestaurantItem.query.all()
    # Organize items by cuisine
    menu = {} 
    for item in items: 
        if item.cuisine not in menu: 
            menu[item.cuisine] = [] 
        menu[item.cuisine].append(item) 
    return render_template('restaurant_booking.html', menu=menu)

# Add item to restaurant cart
@app.route('/add_to_cart/restaurant/<int:item_id>', methods=['POST'])
def add_restaurant_item_to_cart(item_id):
    item = RestaurantItem.query.get_or_404(item_id)
    session['cart']['restaurant_items'].append({'name': item.name, 'price': item.price})
    flash(f'{item.name} added to cart!')
    logging.info(f"Restaurant item {item.name} added to cart")
    return redirect(url_for('restaurant_booking'))

# Services page
@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

# Add service to cart
@app.route('/add_to_cart/service/<int:service_id>', methods=['POST'])
def add_service_to_cart(service_id):
    service = Service.query.get_or_404(service_id)
    session['cart']['services'].append({'name': service.name, 'price': service.price})
    flash(f'{service.name} added to cart!')
    logging.info(f"Service {service.name} added to cart")
    return redirect(url_for('services'))

# Game Store page
@app.route('/game_store')
def game_store():
    games = GameStoreItem.query.all()
    game_items = {} 
    for game in games:
        category = game.category 
        if category not in game_items: 
            game_items[category] = [] 
        game_items[category].append(game)
    return render_template('game_store.html', game_items=game_items)

# Add game store item to cart
@app.route('/add_to_cart/game_store/<int:item_id>', methods=['POST'])
def add_game_item_to_cart(item_id):
    game = GameStoreItem.query.get_or_404(item_id)
    session['cart']['game_store_items'].append({'name': game.name, 'price': game.price})
    flash(f'{game.name} added to cart!')
    logging.info(f"Game store item {game.name} added to cart")
    return redirect(url_for('game_store'))

# Fashion Store page
@app.route('/fashion_store') 
def fashion_store(): 
    fashion_items = FashionStoreItem.query.all() 
    categorized_items = {} 
    for item in fashion_items: 
        if item.category not in categorized_items: 
            categorized_items[item.category] = [] 
            categorized_items[item.category].append(item) 
    return render_template('fashion_store.html', fashion_items=categorized_items)

# Add fashion item to cart
@app.route('/add_to_cart/fashion_store/<int:item_id>', methods=['POST'])
def add_fashion_item_to_cart(item_id):
    fashion_item = FashionStoreItem.query.get_or_404(item_id)
    session['cart']['fashion_store_items'].append({'name': fashion_item.name, 'price': fashion_item.price})
    flash(f'{fashion_item.name} added to cart!')
    logging.info(f"Fashion item {fashion_item.name} added to cart")
    return redirect(url_for('fashion_store'))

# Souvenir Store page
@app.route('/souvenir_store')
def souvenir_store():
    souvenirs = SouvenirItem.query.all()
    return render_template('souvenir_store.html', souvenirs=souvenirs)

# Add souvenir item to cart
@app.route('/add_to_cart/souvenir/<int:item_id>', methods=['POST'])
def add_souvenir_item_to_cart(item_id):
    souvenir = SouvenirItem.query.get_or_404(item_id)
    session['cart']['souvenir_items'].append({'name': souvenir.name, 'price': souvenir.price})
    flash(f'{souvenir.name} added to cart!')
    logging.info(f"Souvenir item {souvenir.name} added to cart")
    return redirect(url_for('souvenir_store'))

# View Booking History
@app.route('/history', defaults={'customer_id': None})
@app.route('/history/<int:customer_id>')
def history(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        flash("No history found for this customer.")
        logging.warning(f"No history found for customer ID {customer_id}")
        return redirect(url_for('admin_dashboard'))
    
    bookings = Booking.query.filter_by(customer_id=customer_id).all()
    room_bookings = RoomBooking.query.filter_by(customer_id=customer_id).all()
    restaurant_orders = RestaurantOrder.query.filter_by(customer_id=customer_id).all()
    store_orders = StoreOrder.query.filter_by(customer_id=customer_id).all()

    return render_template('history.html', customer=customer, bookings=bookings, 
                           room_bookings=room_bookings, restaurant_orders=restaurant_orders, 
                           store_orders=store_orders)

class PDF(FPDF): 
    def header(self): # Hotel logo 
        self.image('static/images/hotel_logo.png', 10, 8, 33) 
        self.set_font('Arial', 'B', 16) 
        self.cell(0, 10, 'Luxury Peaks - Invoice', 0, 1, 'C') 
        self.set_font('Arial', 'I', 12) 
        self.cell(0, 10, 'Your dream stay with us!', 0, 1, 'C') 
        self.ln(20)
    def footer(self): 
        self.set_y(-15) 
        self.set_font('Arial', 'I', 8) 
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')
    def chapter_title(self, title): 
        self.set_font('Arial', 'B', 12) 
        self.cell(0, 10, title, 0, 1, 'L') 
        self.ln(5) 
    def chapter_body(self, body): 
        self.set_font('Arial', '', 12) 
        self.multi_cell(0, 10, body) 
        self.ln() 
def generate_invoice(customer_id, customer_name, customer_room, items, subtotals, tax, grand_total): 
    pdf = PDF() 
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    # Hotel contact details
    pdf.chapter_title("Luxury Peaks Contact Details") 
    pdf.chapter_body("123 Dreamland Avenue\nHotel City, HC 12345\nPhone: +1 234 567 890\nEmail: contact@luxurypeaks.com")
    # Customer details 
    pdf.chapter_title("Customer Details") 
    pdf.chapter_body(f"Customer ID: {customer_id}\nName: {customer_name}\nRoom Number: {customer_room}") 
    # Order details 
    pdf.chapter_title("Order Summary") 
    for category, items_list in items.items(): 
        if items_list: 
            pdf.chapter_body(f"{category.capitalize()} Items") 
            for item in items_list: 
                pdf.chapter_body(f"{item['name']} - Rs. {item['price']} x {item['quantity']}") 
    # Subtotals and totals 
    pdf.chapter_body(f"Room Subtotal: Rs. {subtotals['room']}") 
    pdf.chapter_body(f"Restaurant Subtotal: Rs. {subtotals['restaurant']}")
    pdf.chapter_body(f"Service Subtotal: Rs. {subtotals['service']}") 
    pdf.chapter_body(f"Store Subtotal: Rs. {subtotals['store']}") 
    pdf.chapter_body(f"Tax (12%): Rs. {tax}") 
    pdf.chapter_body(f"Grand Total: Rs. {grand_total}") 
    # Tagline 
    pdf.chapter_body("Thank you for choosing Luxury Peaks. We hope you enjoyed your stay. Please visit us again!") 
    # Save the PDF 
    pdf_output = f'invoice_{customer_id}.pdf' 
    pdf.output(pdf_output) 
    return pdf_output
@app.route('/checkout', methods=['GET', 'POST']) 
def checkout(): 
    if request.method == 'POST': 
        cart = session.get('cart', {}) 
        customer_id = request.form.get('customer_id', 'N/A') 
        customer_name = request.form.get('customer_name', 'N/A') 
        customer_room = request.form.get('customer_room', 'N/A') 
        # Calculate subtotals and total cost 
        subtotals = { 
                     'room': sum(room['cost'] for room in cart['rooms']), 
                     'restaurant': sum(item['price'] for item in cart['restaurant_items']), 
                     'service': sum(item['price'] for item in cart['services']), 
                     'store': sum(item['price'] for item in cart['game_store_items'] + cart['fashion_store_items'] + cart['souvenir_items']) } 
        sub_total = sum(subtotals.values()) 
        tax = sub_total * 0.12 # 12% tax 
        grand_total = sub_total + tax
        # Generate the PDF invoice 
        invoice_path = generate_invoice( 
                    customer_id, customer_name, customer_room, cart, subtotals, tax, grand_total
                                                )
        response = make_response(send_file(invoice_path, as_attachment=True)) 
        response.headers.set('Content-Disposition', 'attachment', filename='invoice.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        flash("Checkout complete. Your invoice is ready for download.") 
        logging.info("Checkout completed with invoice generated") 
        # Reset the cart after checkout 
        session.pop('cart', None) 
        return response
    return render_template('checkout.html')

@app.route('/manage_customer', defaults={'customer_id': None})
@app.route('/manage_customer/<int:customer_id>')
def manage_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'update':
            customer.email = request.form['email']
            customer.contact_number = request.form['contact_number']
            db.session.commit()
            flash("Customer information updated successfully.")
            logging.info(f"Customer ID {customer_id} information updated")
        
        elif action == 'delete':
            db.session.delete(customer)
            db.session.commit()
            flash("Customer record deleted successfully.")
            logging.info(f"Customer ID {customer_id} record deleted")
            return redirect(url_for('admin_dashboard'))

    return render_template('manage_customer.html', customer=customer)


if __name__ == '__main__':
    app.run(debug=True)
