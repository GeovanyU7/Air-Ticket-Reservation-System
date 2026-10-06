from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import hashlib
from datetime import datetime, timedelta
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this_in_production'

# Configure MySQL
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='Airline',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Helper function to hash passwords
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Helper to determine the correct home page based on session
def get_home_url():
    if 'email' in session:  # Customer is logged in
        return url_for('customer_home')
    elif 'username' in session:  # Staff is logged in
        return url_for('staff_home')
    else:  # No one is logged in (public view)
        return url_for('index')

# HOME PAGE - Public
@app.route('/')
def index():
    return render_template('airline_index.html')

# PUBLIC FLIGHT SEARCH
@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    home_url = get_home_url()
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')
        trip_type = request.form.get('trip_type', 'oneway')
        return_date = request.form.get('return_date') if trip_type == 'roundtrip' else None
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search outbound flights
        query = '''
            SELECT f.*, 
                   dep_airport.city as dep_city, dep_airport.country as dep_country,
                   arr_airport.city as arr_city, arr_airport.country as arr_country,
                   a.seat_capacity,
                   (a.seat_capacity - IFNULL((SELECT COUNT(*) FROM Ticket t 
                    WHERE t.airline_name = f.airline_name 
                    AND t.flight_number = f.flight_number 
                    AND t.departure_datetime = f.departure_datetime), 0)) as available_seats
            FROM Flight f
            JOIN Airport dep_airport ON f.departure_airport_code = dep_airport.airport_code
            JOIN Airport arr_airport ON f.arrival_airport_code = arr_airport.airport_code
            JOIN Airplane a ON f.airline_name = a.airline_name AND f.plane_id = a.plane_id
            WHERE (dep_airport.city LIKE %s OR f.departure_airport_code LIKE %s)
            AND (arr_airport.city LIKE %s OR f.arrival_airport_code LIKE %s)
            AND DATE(f.departure_datetime) = %s
            AND f.departure_datetime > NOW()
        '''
        
        search_source = f'%{source}%'
        search_dest = f'%{destination}%'
        cursor.execute(query, (search_source, search_source, search_dest, search_dest, departure_date))
        outbound_flights = cursor.fetchall()
        
        return_flights = []
        if trip_type == 'roundtrip' and return_date:
            cursor.execute(query, (search_dest, search_dest, search_source, search_source, return_date))
            return_flights = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('search_results.html', 
                             outbound_flights=outbound_flights,
                             return_flights=return_flights,
                             trip_type=trip_type,
                             home_url=home_url)
    
    return render_template('search_flights.html', home_url=home_url)

# CUSTOMER REGISTRATION
@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        name = request.form['name']
        phone = request.form['phone_number']
        passport_num = request.form['passport_number']
        passport_exp = request.form['passport_expiration']
        passport_country = request.form['passport_country']
        dob = request.form['date_of_birth']
        building = request.form['building_number']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute('SELECT * FROM Customer WHERE email = %s', (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash('Email already exists', 'error')
            return render_template('register_customer.html', error='Email already exists')
        
        # Insert new customer
        query = '''INSERT INTO Customer (email, c_password, name, phone_number, 
                   passport_number, passport_expiration, passport_country, date_of_birth,
                   building_number, street, city, state) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
        cursor.execute(query, (email, password, name, phone, passport_num, 
                              passport_exp, passport_country, dob, building, 
                              street, city, state))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_customer'))
    
    return render_template('register_customer.html')

# AIRLINE STAFF REGISTRATION
@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        airline_name = request.form['airline_name']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['date_of_birth']
        phone_numbers = request.form.getlist('phone_number')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username exists
        cursor.execute('SELECT * FROM Airline_Staff WHERE username = %s', (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template('register_staff.html', error='Username already exists')
        
        # Check if airline exists
        cursor.execute('SELECT * FROM Airline WHERE airline_name = %s', (airline_name,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template('register_staff.html', error='Airline does not exist')
        
        # Insert staff
        query = '''INSERT INTO Airline_Staff (username, airline_name, a_password, 
                   email, first_name, last_name, date_of_birth) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (username, airline_name, password, email, 
                              first_name, last_name, dob))
        
        # Insert phone numbers
        for phone in phone_numbers:
            if phone.strip():
                cursor.execute('INSERT INTO Staff_Phone (phone_number, username) VALUES (%s, %s)',
                             (phone.strip(), username))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_staff'))
    
    # Get list of airlines
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT airline_name FROM Airline')
    airlines = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('register_staff.html', airlines=airlines)

# CUSTOMER LOGIN
@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Customer WHERE email = %s AND c_password = %s', 
                      (email, password))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if customer:
            session['user_type'] = 'customer'
            session['email'] = email
            session['name'] = customer['name']
            return redirect(url_for('customer_home'))
        else:
            return render_template('login_customer.html', error='Invalid credentials')
    
    return render_template('login_customer.html')

# STAFF LOGIN
@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Airline_Staff WHERE username = %s AND a_password = %s', 
                      (username, password))
        staff = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if staff:
            session['user_type'] = 'staff'
            session['username'] = username
            session['airline_name'] = staff['airline_name']
            session['name'] = f"{staff['first_name']} {staff['last_name']}"
            return redirect(url_for('staff_home'))
        else:
            return render_template('login_staff.html', error='Invalid credentials')
    
    return render_template('login_staff.html')

# CUSTOMER HOME
@app.route('/customer_home')
def customer_home():
    if 'user_type' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login_customer'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get upcoming flights
    query = '''
        SELECT t.ticket_id, f.*, 
               dep.city as dep_city, arr.city as arr_city
        FROM Ticket t
        JOIN Flight f ON t.airline_name = f.airline_name 
                     AND t.flight_number = f.flight_number 
                     AND t.departure_datetime = f.departure_datetime
        JOIN Airport dep ON f.departure_airport_code = dep.airport_code
        JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
        WHERE t.email = %s AND f.departure_datetime > NOW()
        ORDER BY f.departure_datetime
        LIMIT 5
    '''
    cursor.execute(query, (session['email'],))
    upcoming_flights = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('customer_home.html', upcoming_flights=upcoming_flights)

# STAFF HOME
@app.route('/staff_home')
def staff_home():
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get upcoming flights for next 30 days
    query = '''
        SELECT f.*, 
               dep.city as dep_city, arr.city as arr_city,
               a.seat_capacity,
               (SELECT COUNT(*) FROM Ticket t 
                WHERE t.airline_name = f.airline_name 
                AND t.flight_number = f.flight_number 
                AND t.departure_datetime = f.departure_datetime) as tickets_sold
        FROM Flight f
        JOIN Airport dep ON f.departure_airport_code = dep.airport_code
        JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
        JOIN Airplane a ON f.airline_name = a.airline_name AND f.plane_id = a.plane_id
        WHERE f.airline_name = %s 
        AND f.departure_datetime BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
        ORDER BY f.departure_datetime
    '''
    cursor.execute(query, (session['airline_name'],))
    upcoming_flights = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('staff_home.html', flights=upcoming_flights)

# CUSTOMER: VIEW MY FLIGHTS
@app.route('/my_flights')
def my_flights():
    if 'user_type' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login_customer'))
    
    filter_type = request.args.get('filter', 'future')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filter_type == 'past':
        time_condition = 'f.departure_datetime < NOW()'
    else:
        time_condition = 'f.departure_datetime >= NOW()'
    
    query = f'''
        SELECT t.ticket_id, t.purchase_datetime, f.*, 
               dep.city as dep_city, dep.airport_code as dep_code,
               arr.city as arr_city, arr.airport_code as arr_code
        FROM Ticket t
        JOIN Flight f ON t.airline_name = f.airline_name 
                     AND t.flight_number = f.flight_number 
                     AND t.departure_datetime = f.departure_datetime
        JOIN Airport dep ON f.departure_airport_code = dep.airport_code
        JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
        WHERE t.email = %s AND {time_condition}
        ORDER BY f.departure_datetime DESC
    '''
    cursor.execute(query, (session['email'],))
    flights = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('my_flights.html', flights=flights, filter_type=filter_type)

# CUSTOMER: PURCHASE TICKET
@app.route('/purchase_ticket/<airline>/<flight_num>/<departure_time>', methods=['GET', 'POST'])
def purchase_ticket(airline, flight_num, departure_time):
    if 'user_type' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login_customer'))
    
    if request.method == 'POST':
        card_type = request.form['card_type']
        card_number = request.form['card_number']
        name_on_card = request.form['name_on_card']
        card_exp = request.form['card_expiration']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate ticket ID
        cursor.execute('SELECT MAX(ticket_id) as max_id FROM Ticket')
        result = cursor.fetchone()
        if result['max_id']:
            last_num = int(result['max_id'].replace('TCKT', ''))
            ticket_id = f'TCKT{last_num + 1}'
        else:
            ticket_id = 'TCKT10001'
        
        # Insert ticket
        query = '''INSERT INTO Ticket (ticket_id, email, airline_name, flight_number, 
                   departure_datetime, card_type, card_number, name_on_card, 
                   card_expiration_date, purchase_datetime)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())'''
        
        cursor.execute(query, (ticket_id, session['email'], airline, flight_num,
                              departure_time, card_type, card_number, name_on_card, card_exp))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash(f'Ticket purchased successfully! Ticket ID: {ticket_id}', 'success')
        return redirect(url_for('my_flights'))
    
    # GET: Show flight details and purchase form
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT f.*, 
               dep.city as dep_city, dep.airport_code as dep_code,
               arr.city as arr_city, arr.airport_code as arr_code,
               a.seat_capacity,
               (a.seat_capacity - IFNULL((SELECT COUNT(*) FROM Ticket t 
                WHERE t.airline_name = f.airline_name 
                AND t.flight_number = f.flight_number 
                AND t.departure_datetime = f.departure_datetime), 0)) as available_seats
        FROM Flight f
        JOIN Airport dep ON f.departure_airport_code = dep.airport_code
        JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
        JOIN Airplane a ON f.airline_name = a.airline_name AND f.plane_id = a.plane_id
        WHERE f.airline_name = %s AND f.flight_number = %s AND f.departure_datetime = %s
    '''
    
    cursor.execute(query, (airline, flight_num, departure_time))
    flight = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not flight or flight['available_seats'] <= 0:
        flash('Flight not available or sold out', 'error')
        return redirect(url_for('search_flights'))
    
    return render_template('purchase_ticket.html', flight=flight)

# CUSTOMER: RATE FLIGHT
@app.route('/rate_flight/<airline>/<flight_num>/<departure_time>', methods=['GET', 'POST'])
def rate_flight(airline, flight_num, departure_time):
    if 'user_type' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login_customer'))
    
    # Flask automatically decodes the URL parameters, so 'Jet%20Blue' becomes 'Jet Blue'
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        
        # Check if already rated
        cursor.execute('''SELECT * FROM Rating WHERE email = %s AND flight_number = %s 
                         AND departure_datetime = %s AND airline_name = %s''',
                      (session['email'], flight_num, departure_time, airline))
        
        if cursor.fetchone():
            flash('You have already rated this flight', 'error')
        else:
            try:
                # Explicit check: Does the flight exist?
                check_flight = '''SELECT * FROM Flight WHERE airline_name=%s AND flight_number=%s AND departure_datetime=%s'''
                cursor.execute(check_flight, (airline, flight_num, departure_time))
                if not cursor.fetchone():
                     flash(f'Error: Could not find flight {airline} {flight_num}.', 'error')
                else:
                    query = '''INSERT INTO Rating (email, flight_number, departure_datetime, 
                               airline_name, rate, r_comment) VALUES (%s, %s, %s, %s, %s, %s)'''
                    cursor.execute(query, (session['email'], flight_num, departure_time, 
                                          airline, rating, comment))
                    conn.commit()
                    flash('Rating submitted successfully!', 'success')
            except Exception as e:
                flash(f'Database Error: {str(e)}', 'error')
        
        cursor.close()
        conn.close()
        return redirect(url_for('my_flights', filter='past'))
    
    # GET: Show rating form
    query = '''
        SELECT f.*, dep.city as dep_city, arr.city as arr_city
        FROM Flight f
        JOIN Airport dep ON f.departure_airport_code = dep.airport_code
        JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
        WHERE f.airline_name = %s AND f.flight_number = %s AND f.departure_datetime = %s
    '''
    cursor.execute(query, (airline, flight_num, departure_time))
    flight = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('rate_flight.html', flight=flight)

# STAFF: VIEW FLIGHTS
@app.route('/staff_flights')
def staff_flights():
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    filter_type = request.args.get('filter', 'future')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filter_type == 'past':
        time_condition = 'f.departure_datetime < NOW()'
    elif filter_type == 'all':
        time_condition = '1=1'
    else:  # future
        time_condition = 'f.departure_datetime >= NOW()'
    
    query = f'''
        SELECT f.*, 
               dep.city as dep_city, arr.city as arr_city,
               a.seat_capacity,
               (SELECT COUNT(*) FROM Ticket t 
                WHERE t.airline_name = f.airline_name 
                AND t.flight_number = f.flight_number 
                AND t.departure_datetime = f.departure_datetime) as tickets_sold
        FROM Flight f
        JOIN Airport dep ON f.departure_airport_code = dep.airport_code
        JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
        JOIN Airplane a ON f.airline_name = a.airline_name AND f.plane_id = a.plane_id
        WHERE f.airline_name = %s AND {time_condition}
        ORDER BY f.departure_datetime DESC
    '''
    cursor.execute(query, (session['airline_name'],))
    flights = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('staff_flights.html', flights=flights, filter_type=filter_type)

# STAFF: VIEW FLIGHT CUSTOMERS
@app.route('/flight_customers/<airline>/<flight_num>/<departure_time>')
def flight_customers(airline, flight_num, departure_time):
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT c.name, c.email, c.phone_number, t.ticket_id, t.purchase_datetime
        FROM Ticket t
        JOIN Customer c ON t.email = c.email
        WHERE t.airline_name = %s AND t.flight_number = %s AND t.departure_datetime = %s
    '''
    cursor.execute(query, (airline, flight_num, departure_time))
    customers = cursor.fetchall()
    
    # Get flight info
    cursor.execute('''SELECT f.*, dep.city as dep_city, arr.city as arr_city
                     FROM Flight f
                     JOIN Airport dep ON f.departure_airport_code = dep.airport_code
                     JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
                     WHERE f.airline_name = %s AND f.flight_number = %s 
                     AND f.departure_datetime = %s''',
                  (airline, flight_num, departure_time))
    flight = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('flight_customers.html', customers=customers, flight=flight)

# STAFF: CREATE FLIGHT
@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        departure_datetime = request.form['departure_datetime']
        plane_id = request.form['plane_id']
        dep_airport = request.form['departure_airport']
        arr_airport = request.form['arrival_airport']
        arrival_datetime = request.form['arrival_datetime']
        base_price = request.form['base_price']
        status = request.form.get('flight_status', 'On-Time')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''INSERT INTO Flight (airline_name, flight_number, departure_datetime,
                   plane_id, departure_airport_code, arrival_airport_code, 
                   arrival_datetime, base_price, flight_status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        
        try:
            cursor.execute(query, (session['airline_name'], flight_number, departure_datetime,
                                  plane_id, dep_airport, arr_airport, arrival_datetime,
                                  base_price, status))
            conn.commit()
            flash('Flight created successfully!', 'success')
        except Exception as e:
            flash(f'Error creating flight: {str(e)}', 'error')
        
        cursor.close()
        conn.close()
        return redirect(url_for('staff_flights'))
    
    # GET: Show form with airports and airplanes
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Airport')
    airports = cursor.fetchall()
    
    cursor.execute('SELECT plane_id, manufacturer, seat_capacity FROM Airplane WHERE airline_name = %s',
                  (session['airline_name'],))
    airplanes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('create_flight.html', airports=airports, airplanes=airplanes)

# STAFF: CHANGE FLIGHT STATUS
@app.route('/change_status/<airline>/<flight_num>/<departure_time>', methods=['POST'])
def change_status(airline, flight_num, departure_time):
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    new_status = request.form['new_status']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''UPDATE Flight SET flight_status = %s 
               WHERE airline_name = %s AND flight_number = %s AND departure_datetime = %s'''
    cursor.execute(query, (new_status, airline, flight_num, departure_time))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Flight status updated successfully!', 'success')
    return redirect(url_for('staff_flights'))

# STAFF: ADD AIRPLANE
@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    if request.method == 'POST':
        plane_id = request.form['plane_id']
        manufacturer = request.form['manufacturer']
        seat_capacity = request.form['seat_capacity']
        plane_age = request.form['plane_age']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = '''INSERT INTO Airplane (airline_name, plane_id, manufacturer, 
                       seat_capacity, plane_age) VALUES (%s, %s, %s, %s, %s)'''
            cursor.execute(query, (session['airline_name'], plane_id, manufacturer,
                                  seat_capacity, plane_age))
            conn.commit()
            flash('Airplane added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding airplane: {str(e)}', 'error')
        
        cursor.close()
        conn.close()
        return redirect(url_for('view_airplanes'))
    
    return render_template('add_airplane.html')

# STAFF: VIEW AIRPLANES
@app.route('/view_airplanes')
def view_airplanes():
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Airplane WHERE airline_name = %s', (session['airline_name'],))
    airplanes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('view_airplanes.html', airplanes=airplanes)

# STAFF: VIEW RATINGS
@app.route('/view_ratings/<flight_num>/<departure_time>')
def view_ratings(flight_num, departure_time):
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get average rating
    cursor.execute('''SELECT AVG(rate) as avg_rating, COUNT(*) as total_ratings
                     FROM Rating WHERE flight_number = %s AND departure_datetime = %s 
                     AND airline_name = %s''',
                  (flight_num, departure_time, session['airline_name']))
    avg_data = cursor.fetchone()
    
    # Get all ratings
    cursor.execute('''SELECT r.*, c.name FROM Rating r
                     JOIN Customer c ON r.email = c.email
                     WHERE r.flight_number = %s AND r.departure_datetime = %s 
                     AND r.airline_name = %s
                     ORDER BY r.rate DESC''',
                  (flight_num, departure_time, session['airline_name']))
    ratings = cursor.fetchall()
    
    # Get flight info
    cursor.execute('''SELECT f.*, dep.city as dep_city, arr.city as arr_city
                     FROM Flight f
                     JOIN Airport dep ON f.departure_airport_code = dep.airport_code
                     JOIN Airport arr ON f.arrival_airport_code = arr.airport_code
                     WHERE f.flight_number = %s AND f.departure_datetime = %s 
                     AND f.airline_name = %s''',
                  (flight_num, departure_time, session['airline_name']))
    flight = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template('view_ratings.html', ratings=ratings, avg_data=avg_data, flight=flight)

# STAFF: VIEW REPORTS
@app.route('/view_reports')
def view_reports():
    if 'user_type' not in session or session['user_type'] != 'staff':
        return redirect(url_for('login_staff'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Last month ticket sales
    cursor.execute('''SELECT COUNT(*) as count FROM Ticket 
                     WHERE airline_name = %s 
                     AND purchase_datetime >= DATE_SUB(NOW(), INTERVAL 1 MONTH)''',
                  (session['airline_name'],))
    last_month = cursor.fetchone()
    
    # Last year ticket sales
    cursor.execute('''SELECT COUNT(*) as count FROM Ticket 
                     WHERE airline_name = %s 
                     AND purchase_datetime >= DATE_SUB(NOW(), INTERVAL 1 YEAR)''',
                  (session['airline_name'],))
    last_year = cursor.fetchone()
    
    # Month-wise breakdown for last 6 months
    cursor.execute('''SELECT DATE_FORMAT(purchase_datetime, '%%Y-%%m') as month,
                     COUNT(*) as count
                     FROM Ticket 
                     WHERE airline_name = %s 
                     AND purchase_datetime >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
                     GROUP BY month
                     ORDER BY month''',
                  (session['airline_name'],))
    monthly_sales = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('view_reports.html', 
                         last_month=last_month['count'],
                         last_year=last_year['count'],
                         monthly_sales=monthly_sales)

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)