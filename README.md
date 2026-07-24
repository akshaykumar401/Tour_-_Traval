<div align="center">

# ✈️ NextStop

### Discover · Plan · Book · Explore

A modern tour and travel platform for discovering memorable trips and booking your next adventure with confidence.

[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Razorpay](https://img.shields.io/badge/Razorpay-Payments-0C2451)](https://razorpay.com/)

</div>

---

## 🌍 About the project

**NextStop** helps travellers explore tour packages, choose departure dates, and complete secure online bookings. Its goal is to make planning a tour feel simple, reliable, and exciting from the first search to payment confirmation.

> Developed under the internship guidance of **CodeZeal Technology Pvt. Ltd.**

## ✨ Highlights

| 🧭 Explore | 📅 Plan | 💳 Book | ⚙️ Manage |
| --- | --- | --- | --- |
| Browse curated tour packages and details | Choose departure dates and traveller count | Pay securely with Razorpay | Manage packages and bookings through Django Admin |
| View galleries, reviews, FAQs, and contact information | Create accounts and view booking history | Receive booking confirmation emails | Store uploaded images with Cloudinary |

## 🛠️ Built with

| Technology | Purpose |
| --- | --- |
| **Python & Django** | Web application framework |
| **MongoDB** | Application database |
| **Tailwind CSS** | Responsive user interface |
| **Razorpay** | Secure payment processing |
| **Cloudinary** | Cloud image storage and delivery |

## 🚀 Getting started

### 1. Clone the project

```bash
git clone https://github.com/akshaykumar401/Tour_-_Traval.git
cd Tour_-_Traval
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `tour_and_traval/.env` by copying `tour_and_traval/.env.sample`, then add your values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=your-mongodb-connection-url
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
MAIL_SERVICE_URL=your-mail-service-url
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

### 5. Migrate and run

```bash
cd tour_and_traval
python manage.py migrate
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser. 🎉

### 6. Setup and run Mail Service (Required for emails)

The project uses a separate microservice for sending emails. Open a new terminal and run:

```bash
cd Mail_service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `Mail_service/.env` by copying `Mail_service/.env.sample` and add your email credentials:

```env
EMAIL_USER=your-email-address
EMAIL_PASS=your-email-app-password
PORT=8080
```

Run the mail service:

```bash
python wsgi.py
```

The mail service will run on **http://127.0.0.1:8080/**.

## 🗺️ Main routes

| Route | Description |
| --- | --- |
| `/` | Home page |
| `/packages/` | Browse tour packages |
| `/gallery/` | Travel gallery |
| `/booking/` | Booking and payment flow |
| `/user/` | User profile and bookings |
| `/admin/` | Administration dashboard |
| `/help_center/` | Review and FAQ |

## 💳 Razorpay test payment

> [!IMPORTANT]
> Use these details only with Razorpay **test-mode** keys. Never use them for live payments.

| Field | Test value |
| --- | --- |
| Card number | `5267 3181 8797 5449` |
| Expiry date | Any future date |
| CVV | Any number |
| OTP | Any six-digit number |

---

<div align="center">

Made for travellers, one **NextStop** at a time. 🌄

*For educational and personal use.*

</div>
