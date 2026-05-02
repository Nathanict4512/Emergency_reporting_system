# 🚨 SAFETRACK EMERGENCY SYSTEM - STREAMLIT VERSION

## ✨ FREE HOSTING ON STREAMLIT CLOUD!

Complete emergency tracking system with **WhatsApp notifications via Twilio**

---

## 🎯 WHAT YOU GET

✅ **Full Emergency System** - SOS button, contacts, alerts
✅ **WhatsApp Notifications** - Via Twilio (your account is configured!)
✅ **SQLite Database** - Persistent storage
✅ **FREE Hosting** - Deploy to Streamlit Cloud (100% free)
✅ **Mobile Responsive** - Works on any device

---

## 🚀 QUICK START (LOCAL)

### 1. Install Streamlit
```bash
pip install -r requirements.txt
```

### 2. Add Your Twilio Auth Token

Edit `.streamlit/secrets.toml`:
```toml
TWILIO_AUTH_TOKEN = "your_actual_auth_token_here"
```

**Where to find it:**
- Go to: https://console.twilio.com/
- Look for "Auth Token" (next to Account SID)
- Copy and paste it into secrets.toml

### 3. Run the App
```bash
streamlit run app.py
```

**Opens at:** http://localhost:8501

---

## ☁️ DEPLOY TO STREAMLIT CLOUD (FREE!)

### Step 1: Create GitHub Repository

1. Go to: https://github.com/new
2. Name it: `emergency-tracker`
3. Make it **Public**
4. Create repository

### Step 2: Upload Files to GitHub

```bash
# In your project folder
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/emergency-tracker.git
git push -u origin main
```

**OR** upload manually via GitHub web interface:
- Click "Upload files"
- Drag `app.py` and `requirements.txt`
- Commit changes

### Step 3: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub account
4. Select:
   - **Repository:** `emergency-tracker`
   - **Branch:** `main`
   - **Main file:** `app.py`
5. Click "Deploy"

### Step 4: Add Twilio Secret

1. In Streamlit Cloud dashboard
2. Click "⚙️ Settings" → "Secrets"
3. Add this:
```toml
TWILIO_AUTH_TOKEN = "your_actual_auth_token_here"
```
4. Click "Save"

### 🎉 DONE! Your app is live!

URL will be: `https://YOUR_APP_NAME.streamlit.app`

---

## 📱 TWILIO SETUP (Already Configured!)

### Your Twilio Details:
```
Account SID: AC7805201a7d1b72498fd703d556c0a44d
Messaging Service SID: MGf107df8ea7fec85bd7cc03e1d3734342
Emergency Receiver: +2349063348353
```

### What You Need:
✅ Account SID - **Already in code**
✅ Messaging Service SID - **Already in code**
✅ Auth Token - **You need to add this to secrets**

### Is Twilio Free?

**Free Trial:**
- ✅ $15 credit (enough for ~3,000 messages)
- ✅ Can send to verified numbers
- ✅ Perfect for testing

**After Trial:**
- 💰 $0.005 per WhatsApp message (very cheap!)
- 💰 ~200 messages = $1
- 💰 Most affordable option

**How to Get More Credit:**
- Verify your account (add payment method)
- No charge until you use the credit
- Pay-as-you-go pricing

---

## 🔧 HOW IT WORKS

### Emergency Alert Flow:

1. **User clicks SOS button** in dashboard
2. **App captures:**
   - User name, phone, blood group
   - Address
   - Medical info
   - Timestamp
3. **Sends WhatsApp via Twilio to:**
   - Emergency receiver: +2349063348353
   - All user's emergency contacts
4. **Message includes:**
   - User details
   - Location/address
   - Medical information
   - Google Maps link (if GPS available)
   - Timestamp

### WhatsApp Message Example:

```
🚨 EMERGENCY ALERT

Name: Adewale Okonkwo
Phone: +2348012345678
Blood: O+

Location: Victoria Island, Lagos
Map: https://www.google.com/maps?q=6.5244,3.3792

Medical: Diabetic - insulin dependent

Time: 02 May 2026, 14:23:15

⚠️ This is an automated emergency alert. 
Please respond immediately.
```

---

## 📂 PROJECT STRUCTURE

```
emergency_tracker_streamlit/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml           # Twilio Auth Token (gitignored)
├── emergency_tracker.db       # SQLite database (auto-created)
└── README.md                  # This file
```

---

## 💾 DATABASE

**SQLite Database:** `emergency_tracker.db` (auto-created)

**Tables:**
1. **users** - User accounts (name, email, phone, blood, address, medical, password)
2. **contacts** - Emergency contacts (name, phone, relationship, priority)
3. **alerts** - Emergency alerts (status, timestamp, location)

**Sample Account:**
- Email: `test@example.com`
- Password: `password123`
- (Create this on first run)

---

## 🎨 FEATURES

### ✅ User Management
- Registration with email/password
- Login authentication
- Profile management
- Medical information storage

### ✅ Emergency Contacts
- Add unlimited contacts
- Priority levels (primary/normal)
- Phone numbers with relationship
- Delete contacts

### ✅ SOS System
- Big red emergency button
- Instant WhatsApp to all contacts
- Sends to +2349063348353 automatically
- Alert history tracking

### ✅ Dashboard
- Stats (contacts count, alerts count)
- Recent contacts preview
- One-click SOS activation

---

## 🔒 SECURITY

### Passwords:
- SHA256 hashed
- Never stored in plain text
- Secure authentication

### Twilio Token:
- Stored in Streamlit secrets
- Never exposed in code
- Environment-based config

### Database:
- Local SQLite file
- No external access
- Automatic backups (via GitHub)

---

## 🧪 TESTING

### Test Locally:

1. Run app: `streamlit run app.py`
2. Register new account
3. Add test contact with YOUR phone number
4. Click SOS button
5. Check WhatsApp on your phone!

### Test on Streamlit Cloud:

1. Deploy to Streamlit Cloud
2. Open your app URL
3. Register account
4. Add emergency contacts
5. Test SOS functionality

---

## 📱 TWILIO WHATSAPP SANDBOX

### Join Twilio Sandbox:

Before you can receive messages, contacts need to join:

1. Send WhatsApp message to: `+1 415 523 8886`
2. Send this text: `join <your-sandbox-code>`
3. You'll get confirmation
4. Now you can receive emergency alerts!

**Where to find sandbox code:**
- Twilio Console → Messaging → Try it out → Send a WhatsApp message
- Look for "join XXXXXX" code

### For Production:

To send to ANY number without sandbox:
1. Request WhatsApp Business API approval from Twilio
2. Or use Twilio's paid tier
3. Removes sandbox requirement

---

## 🚀 CUSTOMIZATION

### Change Emergency Receiver:

Edit `app.py` line 23:
```python
EMERGENCY_RECEIVER = '+2349063348353'  # Your number
```

### Add Multiple Receivers:

```python
EMERGENCY_RECEIVERS = [
    '+2349063348353',
    '+2348147754855',
    '+2348012345678'
]

# Then loop in create_alert function:
for receiver in EMERGENCY_RECEIVERS:
    send_whatsapp_twilio(receiver, message)
```

### Customize Message:

Edit `app.py` around line 150:
```python
message = f"""🚨 YOUR CUSTOM MESSAGE

...your format here...
"""
```

---

## 💰 COST BREAKDOWN

### FREE:
✅ Streamlit Cloud hosting (unlimited)
✅ SQLite database (unlimited)
✅ GitHub storage (unlimited)
✅ Twilio trial ($15 credit = ~3,000 messages)

### PAID (After Trial):
💰 WhatsApp messages: $0.005 each (~N4 per message)
💰 100 alerts to 3 contacts = 300 messages = $1.50 (~N1,200)
💰 Very affordable!

### Total Cost:
**First 3,000 messages:** FREE
**After that:** ~N4 per message

---

## 🐛 TROUBLESHOOTING

### WhatsApp not sending:

1. **Check Auth Token:**
   - Correct in `.streamlit/secrets.toml`?
   - No extra spaces or quotes?

2. **Check Twilio Console:**
   - Any error messages?
   - Credit balance remaining?

3. **Join Sandbox:**
   - Recipients joined sandbox?
   - Sent "join" message?

### App not deploying:

1. **Check requirements.txt:**
   - All dependencies listed?
   - Correct versions?

2. **Check GitHub:**
   - All files uploaded?
   - Correct branch selected?

3. **Check Streamlit logs:**
   - View logs in dashboard
   - Look for error messages

### Database errors:

```bash
# Delete and recreate
rm emergency_tracker.db
streamlit run app.py
```

---

## 📞 SUPPORT

**Developer:** Nathan ICT Solutions
**Phone:** 08147754855
**Email:** info@nathanict.com.ng
**Website:** nathanict.com.ng

For Twilio support: https://support.twilio.com

---

## 🎓 LEARNING RESOURCES

**Streamlit:**
- Docs: https://docs.streamlit.io/
- Deploy: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app

**Twilio WhatsApp:**
- Quickstart: https://www.twilio.com/docs/whatsapp/quickstart/python
- Pricing: https://www.twilio.com/whatsapp/pricing

**SQLite:**
- Python Docs: https://docs.python.org/3/library/sqlite3.html

---

## ✅ CHECKLIST FOR DEPLOYMENT

- [ ] Install requirements (`pip install -r requirements.txt`)
- [ ] Add Twilio Auth Token to `.streamlit/secrets.toml`
- [ ] Test locally (`streamlit run app.py`)
- [ ] Create GitHub repository
- [ ] Upload files to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Add secrets in Streamlit Cloud dashboard
- [ ] Test WhatsApp delivery
- [ ] Join Twilio sandbox (for recipients)
- [ ] Share app URL with users!

---

**🎉 YOU'RE ALL SET!**

Your emergency tracking system is ready to save lives! 🚨

---

END OF DOCUMENTATION
