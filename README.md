# ✈️ Air Ticket Reservation System

A full-stack airline booking web application built with **Python (Flask)** and **MySQL**. Customers can search for flights, buy tickets, and rate trips they've taken. Airline staff get a separate portal for managing flights, the fleet, and passenger lists, and for viewing sales reports.

The project started from a relational database design (an ER diagram turned into a normalized schema). The application layer sits on top of that schema and uses multi-table joins, correlated subqueries, and aggregate queries to run every feature.

---

## 📸 Overview

| Role | What they can do |
|------|------------------|
| **Public visitor** | Search one-way or round-trip flights by city or airport code and see live seat availability |
| **Customer** | Register, log in, buy tickets, view upcoming and past flights, rate and review completed flights |
| **Airline staff** | Register under an airline, create flights, update flight status, add airplanes, view passenger lists, read ratings, view sales reports |

---

## 🚀 Features

### Customer portal
- **Flight search:** one-way and round-trip search by city name or airport code, limited to future departures
- **Real-time seat availability:** computed from airplane capacity minus tickets sold
- **Ticket purchase:** checkout form with sequential ticket ID generation; sold-out flights can't be booked
- **My Flights dashboard:** upcoming and past trips shown separately
- **Ratings and reviews:** rate past flights from 1 to 5 with a comment; duplicate ratings are blocked

### Airline staff portal
- **Dashboard:** the airline's flights for the next 30 days, with tickets sold vs. capacity
- **Flight management:** create new flights and change status (On-Time / Delayed)
- **Fleet management:** add airplanes and view the current fleet
- **Passenger manifest:** every customer booked on a given flight
- **Customer feedback:** average rating and individual reviews per flight
- **Sales reports:** tickets sold in the last month and last year, plus a month-by-month breakdown for the last 6 months

### Security and access control
- Role-based, session-backed authentication that keeps customers and staff separate
- Route guards on every protected page
- All user input goes through **parameterized SQL queries** to prevent SQL injection
- Staff can only see and manage data for **their own airline**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Flask |
| Database | MySQL (InnoDB) |
| DB driver | PyMySQL |
| Templating | Jinja2 |
| Frontend | HTML5, CSS3 (custom responsive styling) |

---

## 🗄️ Database Design

The schema has **8 related tables** with composite primary keys and foreign key constraints that enforce referential integrity:

```
Airline ──< Airline_Staff ──< Staff_Phone
   │
   ├──< Airplane ──< Flight >── Airport (departure / arrival)
   │                  │
   │                  ├──< Ticket >── Customer
   │                  └──< Rating >── Customer
```

- **Flight** is identified by the composite key `(airline_name, flight_number, departure_datetime)`
- **Airplane** is identified by `(airline_name, plane_id)`, so different airlines can reuse plane IDs
- **Staff_Phone** is a separate table so a staff member can have several phone numbers (a multivalued attribute)

Full design documents are in [`DOCS/`](DOCS/):
- [ER Diagram](DOCS/ER_Diagram.jpg)
- [Relational Schema](DOCS/Relational_Schema.pdf)

---

## 📁 Project Structure

```
Air-Ticket-Reservation-System/
├── airline_app.py          # Flask application (routes, auth, business logic)
├── airline.sql             # Database schema + sample data
├── requirements.txt        # Python dependencies
├── DOCS/
│   ├── ER_Diagram.jpg
│   └── Relational_Schema.pdf
└── templates/              # Jinja2 HTML templates
    ├── airline_index.html      # Landing page
    ├── search_flights.html     # Public flight search
    ├── search_results.html
    ├── login_*.html / register_*.html
    ├── customer_home.html      # Customer dashboard
    ├── my_flights.html
    ├── purchase_ticket.html
    ├── rate_flight.html
    ├── staff_home.html         # Staff dashboard
    ├── staff_flights.html
    ├── create_flight.html
    ├── add_airplane.html
    ├── view_airplanes.html
    ├── flight_customers.html
    ├── view_ratings.html
    └── view_reports.html
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.8+
- MySQL 8+ (or MAMP / XAMPP / WAMP)

### 1. Clone the repository
```bash
git clone https://github.com/GeovanyU7/Air-Ticket-Reservation-System.git
cd Air-Ticket-Reservation-System
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up the database
Create a database named `Airline` and import the schema and sample data:
```bash
mysql -u root -p -e "CREATE DATABASE Airline;"
mysql -u root -p Airline < airline.sql
```
You can also create the database in phpMyAdmin and import `airline.sql`.

> **Linux users:** the SQL dump uses lowercase table names while the app's queries use capitalized ones. Set `lower_case_table_names=1` in your MySQL config, or run the app on macOS/Windows, where table names are case-insensitive by default.

### 4. Configure the connection
If your MySQL credentials aren't `root` with an empty password, update `get_db_connection()` in `airline_app.py`:
```python
host='localhost', user='root', password='', db='Airline'
```

### 5. Run the app
```bash
python airline_app.py
```
Then open **http://127.0.0.1:5000** in your browser.

---

## 🔑 Demo Accounts

The sample data includes these accounts. The password for all of them is `password`.

| Role | Login |
|------|-------|
| Customer | `natalie.chen@gmail.com` |
| Customer | `emily.wu@outlook.com` |
| Airline Staff (Jet Blue) | `jsantiago` |

---

## 🧠 Key Concepts Demonstrated

- **Relational modeling:** turning an ER diagram into a normalized schema with composite and foreign keys
- **Complex SQL:** multi-table `JOIN`s, correlated subqueries for seat availability, aggregates (`AVG`, `COUNT`, `GROUP BY`) for reports and ratings
- **Web application architecture:** MVC-style separation between Flask routes, SQL data access, and Jinja2 views
- **Authentication and authorization:** session management with role-based access control
- **Secure coding:** parameterized queries to prevent SQL injection

---

## 🔮 Future Improvements

- Replace MD5 password hashing with **bcrypt** or Werkzeug's `generate_password_hash`
- Load the secret key and database credentials from **environment variables**
- Tokenize payment data through a payment processor instead of storing card details
- Use database transactions or row locking when buying tickets, to prevent overbooking under concurrent requests
- Add CSRF protection (Flask-WTF) and server-side form validation
- Add charts to the sales reports and pagination to flight lists
- Containerize with Docker and deploy to the cloud

---

## 👤 Author

**Geovany Urgiles**
GitHub: [@GeovanyU7](https://github.com/GeovanyU7)
