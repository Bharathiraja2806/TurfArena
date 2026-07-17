# TurfArena

TurfArena is a Django turf discovery and slot-booking foundation with role-ready users, turf inventory, availability slots, booking history, and REST endpoints.

## Quick start

1. Create and activate a virtual environment.
2. Install packages: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and adjust database values if using MySQL.
4. Run `python manage.py makemigrations users turfs bookings`
5. Run `python manage.py migrate`
6. Create an administrator: `python manage.py createsuperuser`
7. Start: `python manage.py runserver`

Visit `/admin/` to add sports, amenities, turfs, and slots. The storefront is available at `/`; JSON endpoints are at `/api/turfs/` and `/api/bookings/`.

## Key design points

- Custom user roles: Super Admin, Turf Owner, Customer, Staff.
- Normalized sport, amenity, turf, image, slot, and booking relations.
- Conditional unique database constraint prevents duplicate pending/confirmed bookings for one slot and date.
- SQLite runs locally by default; MySQL is enabled through environment variables.

## Next production integrations

Add Razorpay/Stripe webhooks, email/SMS providers, object storage for media, Redis/Celery for background reminders, a payment app, and role-specific dashboards before launch.
