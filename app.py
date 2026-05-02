"""
Emergency Tracking System - Streamlit App
Free hosting on Streamlit Cloud
With Twilio WhatsApp Integration
"""

import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import json
import requests

# Page config
st.set_page_config(
    page_title="SafeTrack Emergency System",
    page_icon="🚨",
    layout="centered"
)

# Database setup
DATABASE = 'emergency_tracker.db'

# Twilio Configuration (from your account)
TWILIO_ACCOUNT_SID = 'AC7805201a7d1b72498fd703d556c0a44d'
TWILIO_MESSAGING_SERVICE_SID = 'MGf107df8ea7fec85bd7cc03e1d3734342'
TWILIO_AUTH_TOKEN = st.secrets.get("TWILIO_AUTH_TOKEN", "")  # Store in Streamlit secrets

# Emergency contact number
EMERGENCY_RECEIVER = '+2349063348353'  # Your number

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        blood_group TEXT,
        address TEXT,
        password_hash TEXT NOT NULL,
        medical_info TEXT,
        created_at TEXT
    )''')
    
    # Contacts table
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        relationship TEXT NOT NULL,
        priority TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Alerts table
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        ended_at TEXT,
        lat REAL,
        lng REAL,
        address TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

def send_whatsapp_twilio(to_number, message):
    """Send WhatsApp message via Twilio"""
    try:
        if not TWILIO_AUTH_TOKEN:
            st.warning("⚠️ Twilio Auth Token not configured. Add it to Streamlit secrets.")
            st.info(f"📱 Would send to: {to_number}")
            st.code(message)
            return True
        
        url = f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json'
        
        data = {
            'To': f'whatsapp:{to_number}',
            'MessagingServiceSid': TWILIO_MESSAGING_SERVICE_SID,
            'Body': message
        }
        
        response = requests.post(
            url,
            data=data,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        )
        
        if response.status_code == 201:
            st.success(f"✅ WhatsApp sent to {to_number}")
            return True
        else:
            st.error(f"❌ Failed: {response.text}")
            return False
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def hash_password(password):
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(email):
    """Get user by email"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(name, email, phone, blood_group, address, password, medical_info):
    """Create new user"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    user_id = f"u_{datetime.now().timestamp()}"
    password_hash = hash_password(password)
    created_at = datetime.now().isoformat()
    
    try:
        c.execute('''INSERT INTO users 
            (id, name, email, phone, blood_group, address, password_hash, medical_info, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, name, email, phone, blood_group, address, password_hash, medical_info, created_at)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def get_contacts(user_id):
    """Get user's emergency contacts"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM contacts WHERE user_id = ? ORDER BY priority', (user_id,))
    contacts = c.fetchall()
    conn.close()
    return contacts

def add_contact(user_id, name, phone, relationship, priority):
    """Add emergency contact"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    contact_id = f"c_{datetime.now().timestamp()}"
    c.execute('''INSERT INTO contacts 
        (id, user_id, name, phone, relationship, priority)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (contact_id, user_id, name, phone, relationship, priority)
    )
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    """Delete emergency contact"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

def create_alert(user_id, lat, lng, address):
    """Create emergency alert and send WhatsApp"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Get user info
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    # Create alert
    alert_id = f"a_{datetime.now().timestamp()}"
    started_at = datetime.now().isoformat()
    
    c.execute('''INSERT INTO alerts 
        (id, user_id, status, started_at, lat, lng, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (alert_id, user_id, 'active', started_at, lat, lng, address)
    )
    
    # Get contacts
    c.execute('SELECT * FROM contacts WHERE user_id = ?', (user_id,))
    contacts = c.fetchall()
    
    conn.commit()
    conn.close()
    
    # Send WhatsApp messages
    map_link = f"https://www.google.com/maps?q={lat},{lng}" if lat and lng else "Location unavailable"
    
    message = f"""🚨 EMERGENCY ALERT

Name: {user[1]}
Phone: {user[3]}
Blood: {user[4]}

Location: {address or 'Locating...'}
Map: {map_link}

Medical: {user[7] or 'None'}

Time: {datetime.now().strftime('%d %b %Y, %H:%M:%S')}

⚠️ This is an automated emergency alert. Please respond immediately."""
    
    # Send to emergency receiver
    send_whatsapp_twilio(EMERGENCY_RECEIVER, message)
    
    # Send to all contacts
    for contact in contacts:
        send_whatsapp_twilio(contact[3], message)
    
    return alert_id

def get_alerts(user_id):
    """Get user's alerts"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM alerts WHERE user_id = ? ORDER BY started_at DESC', (user_id,))
    alerts = c.fetchall()
    conn.close()
    return alerts

# Initialize database
init_db()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Custom CSS
st.markdown("""
<style>
.big-button {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff6b6b, #e11d48);
    color: white;
    font-size: 32px;
    font-weight: bold;
    border: 6px solid white;
    box-shadow: 0 20px 50px rgba(225, 29, 72, 0.5);
    cursor: pointer;
    margin: 20px auto;
    display: block;
}
.stat-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 10px 0;
}
.contact-card {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# Main App
if not st.session_state.logged_in:
    # Login/Register Page
    st.title("🛡️ SafeTrack")
    st.subheader("Emergency Tracking System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Sign In")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Sign In", use_container_width=True):
            user = get_user(email)
            if user and user[6] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid email or password")
    
    with tab2:
        st.markdown("### Create Account")
        name = st.text_input("Full Name")
        reg_email = st.text_input("Email", key="reg_email")
        phone = st.text_input("Phone (e.g., +2348012345678)")
        blood = st.selectbox("Blood Group", ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        address = st.text_area("Home Address")
        medical = st.text_area("Medical Info (allergies, conditions, medications)")
        reg_password = st.text_input("Password (min 8 characters)", type="password", key="reg_password")
        
        if st.button("Create Account", use_container_width=True):
            if len(reg_password) < 8:
                st.error("Password must be at least 8 characters")
            elif not name or not reg_email or not phone:
                st.error("Please fill in all required fields")
            else:
                if create_user(name, reg_email, phone, blood, address, reg_password, medical):
                    st.success("✅ Account created! Please sign in.")
                else:
                    st.error("Email already registered")

else:
    # Dashboard
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {user[1].split()[0]}")
        st.write(f"📧 {user[2]}")
        st.write(f"📞 {user[3]}")
        st.write(f"🩸 Blood: {user[4]}")
        
        st.markdown("---")
        
        page = st.radio("Navigation", ["🏠 Home", "👥 Contacts", "🕒 History", "👤 Profile"])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Main content
    if page == "🏠 Home":
        st.title("🏠 Dashboard")
        
        # Stats
        col1, col2 = st.columns(2)
        contacts = get_contacts(user[0])
        alerts = get_alerts(user[0])
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h3>{len(contacts)}</h3>
                <p>Emergency Contacts</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h3>{len(alerts)}</h3>
                <p>Total Alerts</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Emergency Button
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🚨 Emergency Alert")
        st.info("⚠️ Press the button below to send emergency alerts to all your contacts")
        
        if st.button("🚨 SEND SOS ALERT", key="sos", help="Click to send emergency alert"):
            if len(contacts) == 0:
                st.error("⚠️ Add at least one emergency contact first!")
            else:
                with st.spinner("Sending emergency alerts..."):
                    # Get location (mock for now - in production use browser geolocation)
                    address = user[5] or "Location not available"
                    
                    alert_id = create_alert(user[0], None, None, address)
                    
                    st.success(f"""
                    ✅ **EMERGENCY ALERT SENT!**
                    
                    📱 WhatsApp messages sent to:
                    - Emergency receiver: {EMERGENCY_RECEIVER}
                    - {len(contacts)} emergency contact(s)
                    
                    🆔 Alert ID: {alert_id}
                    ⏰ Time: {datetime.now().strftime('%H:%M:%S')}
                    """)
        
        # Recent contacts
        st.markdown("---")
        st.markdown("### 👥 Your Emergency Contacts")
        if contacts:
            for contact in contacts[:3]:
                st.markdown(f"""
                <div class="contact-card">
                    <strong>{contact[2]}</strong> ({contact[4]})<br>
                    📞 {contact[3]}<br>
                    <span style="background:#667eea;color:white;padding:2px 8px;border-radius:10px;font-size:11px">{contact[5].upper()}</span>
                </div>
                """, unsafe_allow_html=True)
            
            if len(contacts) > 3:
                st.info(f"+ {len(contacts) - 3} more contacts")
        else:
            st.warning("⚠️ No emergency contacts added yet")
    
    elif page == "👥 Contacts":
        st.title("👥 Emergency Contacts")
        
        # Add contact form
        with st.expander("➕ Add New Contact", expanded=False):
            c_name = st.text_input("Contact Name")
            c_phone = st.text_input("Phone Number")
            c_rel = st.selectbox("Relationship", ["", "Parent", "Sibling", "Spouse", "Child", "Friend", "Doctor", "Neighbour"])
            c_priority = st.selectbox("Priority", ["", "primary", "normal"])
            
            if st.button("Add Contact"):
                if c_name and c_phone and c_rel and c_priority:
                    add_contact(user[0], c_name, c_phone, c_rel, c_priority)
                    st.success(f"✅ {c_name} added!")
                    st.rerun()
                else:
                    st.error("Please fill all fields")
        
        # List contacts
        st.markdown("---")
        contacts = get_contacts(user[0])
        
        if contacts:
            st.write(f"**{len(contacts)} contact(s) saved**")
            for contact in contacts:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div class="contact-card">
                        <strong>{contact[2]}</strong><br>
                        {contact[4]} • {contact[3]}<br>
                        <span style="background:#{'#fee2e2' if contact[5]=='primary' else '#ede9fe'};color:#{'#b91c1c' if contact[5]=='primary' else '#6d28d9'};padding:2px 8px;border-radius:10px;font-size:11px">{contact[5].upper()}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️", key=f"del_{contact[0]}"):
                        delete_contact(contact[0])
                        st.rerun()
        else:
            st.info("No contacts yet. Add your first emergency contact above.")
    
    elif page == "🕒 History":
        st.title("🕒 Alert History")
        
        alerts = get_alerts(user[0])
        
        if alerts:
            for alert in alerts:
                status_color = "#28a745" if alert[2] == "resolved" else "#dc3545"
                st.markdown(f"""
                <div style="background:white;padding:15px;border-radius:10px;margin:10px 0;border-left:4px solid {status_color}">
                    <strong>Alert #{alert[0][-8:]}</strong><br>
                    Status: <span style="color:{status_color}">{alert[2].upper()}</span><br>
                    Time: {alert[3]}<br>
                    Location: {alert[7] or 'N/A'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No emergency alerts yet. Stay safe!")
    
    elif page == "👤 Profile":
        st.title("👤 My Profile")
        
        st.markdown("### Personal Information")
        st.write(f"**Name:** {user[1]}")
        st.write(f"**Email:** {user[2]}")
        st.write(f"**Phone:** {user[3]}")
        st.write(f"**Blood Group:** {user[4]}")
        st.write(f"**Address:** {user[5]}")
        
        st.markdown("---")
        st.markdown("### Medical Information")
        st.write(user[7] or "No medical information provided")
        
        st.markdown("---")
        st.markdown("### Account")
        st.write(f"**Created:** {user[8]}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;font-size:12px">
    <p>SafeTrack Emergency System • Powered by Nathan ICT Solutions</p>
    <p>📞 08147754855 • nathanict.com.ng</p>
</div>
""", unsafe_allow_html=True)
