# Creovate — Freelancer Service Marketplace

Creovate is a professional, Django-powered freelance marketplace web application designed to seamlessly connect customers with skilled freelance professionals. The platform specializes in three core categories: **Home Design**, **Logo Design**, and **Software Development**, providing a complete end-to-end flow for service listing, profile management, and order transactions.

---

## 🚀 Key Features

### 👤 User Roles & Authentication
*   **Dual Portal Access:** Separate and tailored user experiences for **Customers** and **Freelancers**.
*   **Secure Authentication:** User registration, login, logout, and password management.
*   **Password Recovery:** Complete forgot-password and reset-password confirmation flow via SMTP email integration.
*   **Account Deletion:** Users can safely delete their profiles and all associated data.

### 💼 Service Management (Freelancers)
*   **Service CRUD:** Freelancers can easily add, view, update, and delete the services they offer.
*   **Rich Details:** Include title, description, category, pricing, and high-quality images.
*   **SEO-Friendly URLs:** Automatically generated slugs for clean, readable service detail pages.

### 💳 Creovate Wallet System
*   **Personal Virtual Wallets:** Every registered profile is automatically provisioned with a virtual wallet.
*   **Balance Top-ups:** Customers can top up their wallets to pay for services.
*   **Earnings Tracking:** Freelancers receive payouts directly to their wallets and can monitor their earnings.

### 🛒 Checkout & Order Lifecycle
*   **Service Checkout:** One-click checkout using wallet balances.
*   **Order Cancellation:** Customers can cancel pending orders.
*   **Order History:** Comprehensive order history logs for customers.
*   **Freelancer Order Dashboard:** Freelancers can view incoming orders, track their progress, and view details.

---

## 🛠️ Technology Stack

*   **Backend:** Python 3 & Django 5.1.3
*   **Database:** PostgreSQL (with SQLite legacy support)
*   **Frontend:** Django Templates, Semantic HTML5, Custom JavaScript, and Vanilla CSS
*   **UI Framework & Styles:** Bootstrap 5.3, Google Fonts (Megrim, Rubik Vinyl, Londrina Sketch, Luckiest Guy, Dosis), custom styles (`style.css`, `service.css`)
*   **Animations & Plugins:** AOS (Animate on Scroll), Owl Carousel, Magnific Popup, jQuery
*   **Image Processing:** Pillow (PIL) for automated image compression and resizing (500x500 max) on upload

---

## 📂 Project Structure

```text
creovate/
├── creovate/                   # Core Project Configuration
│   ├── account/                # User Auth, Wallet, and Order App
│   │   ├── models.py           # Profile, Wallet, and Order models
│   │   ├── views.py            # Registration, Login, Wallet, Order views
│   │   └── urls.py             # Auth and customer/freelancer dashboards
│   ├── service/                # Service Catalog App
│   │   ├── models.py           # Service and ServiceCategory models
│   │   ├── views.py            # Service CRUD views
│   │   └── urls.py             # Service listing, adding, and details
│   ├── settings.py             # Global settings (DB, SMTP, Media)
│   ├── urls.py                 # Main URL routing
│   └── views.py                # Landing, About, and Error views
├── static/                     # Static assets (CSS, JS, Images)
│   ├── css/                    # Custom CSS files (style.css, service.css)
│   ├── images/                 # Theme graphics and default images
│   └── js/                     # jQuery, Bootstrap, and animation scripts
├── templates/                  # Django HTML templates
│   ├── common/                 # Landing, About, and catalog templates
│   ├── footer/ & header/       # Layout partials
│   ├── resetPassword/          # Password reset template files
│   ├── service/                # Service creation and modification templates
│   ├── user/                   # Portals, login, and wallet templates
│   └── base.html               # Main base template
├── db.sqlite3                  # Local SQLite database (development)
├── manage.py                   # Django management script
└── .gitignore                  # Git ignore file (virtualenvs, media uploads, etc.)
```

---

## 💻 Getting Started

### Prerequisites
Make sure you have the following installed on your system:
*   [Python 3.10+](https://www.python.org/downloads/)
*   [PostgreSQL](https://www.postgresql.org/download/)
*   [Git](https://git-scm.com/)

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd creovate
    ```

2.  **Create and Activate a Virtual Environment:**
    *   **Windows:**
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```
    *   **macOS / Linux:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install Dependencies:**
    Install Django, Pillow, and the PostgreSQL driver:
    ```bash
    pip install django pillow psycopg2-binary
    ```

4.  **Database Configuration:**
    Ensure PostgreSQL is running and you have created a database named `creovate`.
    Open [settings.py](file:///c:/Stupen/creovate/creovate/settings.py) and update the `DATABASES` setting with your credentials:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'creovate',
            'USER': 'your_postgres_user',
            'PASSWORD': 'your_postgres_password',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
    ```

5.  **Run Migrations:**
    Create database tables and apply migrations:
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin Account):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```
    Access the application at `http://127.0.0.1:8000/`.

---

## ✉️ SMTP Email Setup

To enable the password reset email features, update the SMTP details in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 🔒 Gitignore Policy

The project includes a root `.gitignore` configured to keep the repository clean and secure. It ignores:
*   Virtual environments (`.venv/`, `env/`)
*   Local database files (`db.sqlite3`)
*   IDE settings (`.idea/`, `.vscode/`)
*   Bytecode cache files (`__pycache__/`)
*   User-uploaded images in `static/images/` while maintaining standard template design assets.
