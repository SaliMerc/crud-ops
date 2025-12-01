Django M-Pesa STK Push Payments (CRUD Project)

A fully working Django project that lets users pay instantly using STK Push.  
Perfect for shops, donations, school fees, events — anything!

Works 100% on the sandbox.

Features
- Instant M-Pesa STK Push (pop-up on phone)
- Real-time callback → transaction updates automatically
- View all payments 
- Secure — no secrets in the repo

How to Run Locally (Takes 5 Minutes)

1. Clone the repo
```bash
git clone https://github.com/SaliMerc/crud-ops.git
```

2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Set up your environment variables (MOST IMPORTANT)
```bash
Create a .env file in the project root.
Should be on the same level as the app
```

Then edit the new `.env` file and fill in your M-Pesa details:

```bash
DEBUG=True
SECRET_KEY=your-super-secret-django-key-here

# M-PESA CREDENTIALS (get from https://developer.safaricom.co.ke)
MPESA_CONSUMER_KEY=''
MPESA_CONSUMER_SECRET=''
MPESA_SHORTCODE=''
MPESA_PASSKEY=''
MPESA_ENVIRONMENT=''
MPESA_CALLBACK_URL=''

MPESA_ACCOUNT_REFERENCE = ''
MPESA_TRANSACTION_DESC = ''
```

5. Run migrations & create admin
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Start the server
```bash
python manage.py runserver
```

Open → http://127.0.0.1:8000  
Admin → http://127.0.0.1:8000/admin

Testing Callbacks Locally with ngrok (2 Minutes)

Safaricom needs a public URL → use ngrok (free)

1. Download ngrok → https://ngrok.com/download
2. Run in a new terminal:
   ```bash
   ngrok http 8000
   ```
3. Copy the https URL it shows (example: https://a1b2c3d4e5f6.ngrok.io)
4. Update your `.env`:
   ```env
   MPESA_CALLBACK_URL=https://ahsjwjw992.ngrok.io/mpesa/callback/
   ```
5. Restart server → test payment 

Keep ngrok running. New session = new URL → update .env again.

Going Live (Production)
```env
DEBUG=False
MPESA_ENVIRONMENT=production
MPESA_CALLBACK_URL=https://yourrealdomain.com/mpesa/callback/
```

Project Structure
```
crud-ops/
├── Admin/              → main app
├── media/          → media files
├── Shop/             → Project config
├── static/         → Images
├── venv/         → virtual environment
├── .env      → (ignored)
├── requirements.txt   → contains all the dependencies
└── db.sqlite3    → (ignored)
```

Security
`.env` and `db.sqlite3` are never committed thanks to `.gitignore`.

Made with ❤️ by SaliMerc  
Star | Fork | Share | Contribute

Happy coding!
