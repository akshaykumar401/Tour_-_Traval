# NextStop

NextStop is a tour and travel web application that helps travellers discover tour packages, select available departure dates, and securely book their next trip.

## Project goal

Build a simple, friendly platform for exploring travel experiences and completing tour bookings online.

## Acknowledgement

This project was developed under the internship guidance of **CodeZeal Technology Pvt. Ltd.**

## Features

- Browse tour packages and package details
- View galleries, reviews, FAQs, and contact information
- Choose travel dates and the number of travellers
- Create and manage user accounts
- Process secure bookings with Razorpay
- Send booking confirmation emails
- Manage packages, bookings, and content through Django Admin
- Store uploaded images with Cloudinary

## Technology

- Python and Django
- PostgreSQL
- Tailwind CSS
- Razorpay for payments
- Cloudinary for image storage

## Getting started

1. Clone the repository and open the project folder.

2. Create and activate a virtual environment.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create `tour_and_traval/.env` from `tour_and_traval/.env.sample` and add your configuration values.

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=your-postgresql-connection-url
   RAZORPAY_KEY_ID=your-razorpay-key-id
   RAZORPAY_KEY_SECRET=your-razorpay-key-secret
   EMAIL_HOST_USER=your-email-address
   EMAIL_HOST_PASSWORD=your-email-app-password
   CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   CLOUDINARY_API_KEY=your-cloudinary-api-key
   CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   ```

5. Run migrations and start the development server.

   ```bash
   cd tour_and_traval
   python manage.py migrate
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/` in your browser.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Home page |
| `/packages/` | Tour packages |
| `/gallery/` | Travel gallery |
| `/booking/` | Booking and payment flow |
| `/user/` | User profile and bookings |
| `/admin/` | Administration panel |

## Razorpay test payment

Use these details only while the application is using Razorpay **test-mode** keys:

| Field | Test value |
| --- | --- |
| Card number | `5267 3181 8797 5449` |
| Expiry date | Any future date |
| CVV | Any number |
| OTP | Any six-digit number |

Do not use these details for live payments. Switch to live Razorpay keys only when the payment flow is ready for production.

## License

This project is intended for educational and personal use.
