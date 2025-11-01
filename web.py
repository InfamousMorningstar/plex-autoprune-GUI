"""
Plex-Auto-Prune GUI Web Interface
A sophisticated web GUI for managing Plex user access automation
Runs alongside the daemon with a web dashboard on port 8080
"""
import os
import json
import sys
import threading
import time
import uuid
import requests
import smtplib
import socket
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import Flask, render_template, jsonify, request, send_from_directory, session, redirect, url_for, send_file
from flask_socketio import SocketIO, emit
import secrets
from plexapi.myplex import MyPlexAccount

# Ensure UTF-8 encoding for stdout to handle Unicode characters
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass  # Already UTF-8 or not supported

# Import daemon module
import daemon

# File lock for VIP operations to prevent race conditions
vip_lock = threading.Lock()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# PRODUCTION: Restrict CORS to localhost only (change to your domain in production)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:8080", "http://127.0.0.1:8080"], async_mode='eventlet')

# Configuration file path
CONFIG_FILE = "/app/.env"
SETUP_FLAG = "/app/state/.setup_complete"
PLEX_AUTH_FILE = "/app/state/.plex_auth.json"

# Plex OAuth Configuration
PLEX_CLIENT_ID = "plex-auto-prune-gui"
PLEX_PRODUCT = "Plex-Auto-Prune GUI"

# In-memory log buffer for real-time streaming
log_buffer = []
MAX_LOG_BUFFER = 1000

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('plex_token'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# API login decorator
def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('plex_token'):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def save_plex_auth(token, username, email):
    """Save Plex authentication data"""
    auth_data = {
        'token': token,
        'username': username,
        'email': email,
        'authenticated_at': datetime.now(timezone.utc).isoformat()
    }
    os.makedirs(os.path.dirname(PLEX_AUTH_FILE), exist_ok=True)
    with open(PLEX_AUTH_FILE, 'w') as f:
        json.dump(auth_data, f, indent=2)
    web_log(f"Plex authentication saved for {username}", "SUCCESS")

def load_plex_auth():
    """Load saved Plex authentication"""
    if os.path.exists(PLEX_AUTH_FILE):
        try:
            with open(PLEX_AUTH_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            web_log(f"Failed to load Plex auth: {e}", "ERROR")
    return None

def verify_plex_token(token):
    """Verify a Plex token is valid"""
    try:
        account = MyPlexAccount(token=token)
        return {
            'valid': True,
            'username': account.username,
            'email': account.email,
            'thumb': account.thumb
        }
    except Exception as e:
        web_log(f"Plex token verification failed: {e}", "ERROR")
        return {'valid': False}

def web_log(msg, level="INFO"):
    """Log message and broadcast to connected clients"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"timestamp": ts, "level": level, "message": msg}
    log_buffer.append(log_entry)
    if len(log_buffer) > MAX_LOG_BUFFER:
        log_buffer.pop(0)
    socketio.emit('log', log_entry, namespace='/')
    print(f"[{ts}] [{level}] {msg}", flush=True)

def is_setup_complete():
    """Check if initial setup wizard has been completed"""
    return os.path.exists(SETUP_FLAG)

def is_plex_configured():
    """Check if Plex credentials are configured"""
    plex_token = os.environ.get('PLEX_TOKEN', '')
    return bool(plex_token and plex_token.strip())

def is_tautulli_configured():
    """Check if Tautulli is configured"""
    tautulli_url = os.environ.get('TAUTULLI_URL', '')
    tautulli_key = os.environ.get('TAUTULLI_API_KEY', '')
    return bool(tautulli_url and tautulli_url.strip() and tautulli_key and tautulli_key.strip())

def is_email_configured():
    """Check if email is configured"""
    smtp_host = os.environ.get('SMTP_HOST', '')
    smtp_user = os.environ.get('SMTP_USERNAME', '')
    smtp_pass = os.environ.get('SMTP_PASSWORD', '')
    smtp_from = os.environ.get('SMTP_FROM', '')
    admin_email = os.environ.get('ADMIN_EMAIL', '')
    return bool(smtp_host and smtp_user and smtp_pass and smtp_from and admin_email)

def is_fully_configured():
    """Check if all required configuration is present"""
    return is_plex_configured() and is_tautulli_configured() and is_email_configured()

def mark_setup_complete():
    """Mark setup wizard as complete"""
    os.makedirs(os.path.dirname(SETUP_FLAG), exist_ok=True)
    with open(SETUP_FLAG, 'w') as f:
        f.write(datetime.now().isoformat())

def get_env_config():
    """Read current environment configuration"""
    return {
        'PLEX_TOKEN': os.environ.get('PLEX_TOKEN', ''),
        'PLEX_SERVER_NAME': os.environ.get('PLEX_SERVER_NAME', ''),
        'TAUTULLI_URL': os.environ.get('TAUTULLI_URL', ''),
        'TAUTULLI_API_KEY': os.environ.get('TAUTULLI_API_KEY', ''),
        'SMTP_HOST': os.environ.get('SMTP_HOST', 'smtp.gmail.com'),
        'SMTP_PORT': os.environ.get('SMTP_PORT', '587'),
        'SMTP_USERNAME': os.environ.get('SMTP_USERNAME', ''),
        'SMTP_PASSWORD': os.environ.get('SMTP_PASSWORD', ''),
        'SMTP_FROM': os.environ.get('SMTP_FROM', ''),
        'ADMIN_EMAIL': os.environ.get('ADMIN_EMAIL', ''),
        'DISCORD_WEBHOOK': os.environ.get('DISCORD_WEBHOOK', ''),
        'LINK_DISCORD': os.environ.get('LINK_DISCORD', ''),
        'WARN_DAYS': os.environ.get('WARN_DAYS', '27'),
        'KICK_DAYS': os.environ.get('KICK_DAYS', '30'),
        'CHECK_NEW_USERS_SECS': os.environ.get('CHECK_NEW_USERS_SECS', '120'),
        'CHECK_INACTIVITY_SECS': os.environ.get('CHECK_INACTIVITY_SECS', '1800'),
        'VIP_NAMES': os.environ.get('VIP_NAMES', ''),
        'DRY_RUN': os.environ.get('DRY_RUN', 'true')
    }

def save_env_config(config):
    """Save configuration to .env file"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        f.write("# Plex-Auto-Prune GUI Configuration\n")
        f.write("# Generated by Plex-Auto-Prune GUI\n\n")
        for key, value in config.items():
            if value:
                f.write(f'{key}={value}\n')
    
    # Reload environment
    daemon.load_env_file(CONFIG_FILE)

# ==================== ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with Plex OAuth"""
    # Don't redirect if already logged in - just show login page
    # This prevents redirect loops
    
    # Handle PIN callback from Plex
    if request.args.get('pinID'):
        pin_id = request.args.get('pinID')
        
        # Check if this is a polling request (AJAX from JavaScript)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes.accept_json
        
        try:
            # Check PIN status
            pin_url = f"https://plex.tv/api/v2/pins/{pin_id}"
            headers = {
                'Accept': 'application/json',
                'X-Plex-Client-Identifier': PLEX_CLIENT_ID
            }
            response = requests.get(pin_url, headers=headers)
            data = response.json()
            
            if data.get('authToken'):
                token = data['authToken']
                
                # Verify token and get user info
                verification = verify_plex_token(token)
                if verification['valid']:
                    # Update environment with token first
                    os.environ['PLEX_TOKEN'] = token
                    
                    # Try to get server name BEFORE saving to session
                    server_name = ''
                    try:
                        account = MyPlexAccount(token=token)
                        resources = account.resources()
                        servers = [r for r in resources if r.provides == 'server']
                        if servers:
                            server_name = servers[0].name
                            os.environ['PLEX_SERVER_NAME'] = server_name
                            web_log(f"Plex server detected: {server_name}", "SUCCESS")
                    except Exception as e:
                        web_log(f"Could not fetch server info: {e}", "WARNING")
                    
                    # Save to session (including server_name)
                    session['plex_token'] = token
                    session['plex_username'] = verification['username']
                    session['plex_email'] = verification['email']
                    session['plex_server_name'] = server_name
                    session.permanent = True
                    
                    web_log(f"Saved to session: token={bool(token)}, user={verification['username']}, server={server_name}", "DEBUG")
                    
                    # Save authentication
                    save_plex_auth(token, verification['username'], verification['email'])
                    
                    # Update .env file with both token and server
                    config = get_env_config()
                    config['PLEX_TOKEN'] = token
                    if server_name:
                        config['PLEX_SERVER_NAME'] = server_name
                    save_env_config(config)
                    
                    web_log(f"Plex login successful: {verification['username']}", "SUCCESS")
                    
                    # Return JSON for AJAX requests, redirect for normal requests
                    if is_ajax:
                        return jsonify({'success': True, 'redirect': url_for('index')})
                    return redirect(url_for('index'))
                else:
                    if is_ajax:
                        return jsonify({'success': False, 'error': 'Invalid Plex token'})
                    return render_template('login.html', error='Invalid Plex token')
            else:
                # Still waiting for authentication
                if is_ajax:
                    return jsonify({'success': False, 'pending': True})
                return render_template('login.html', error='Plex authentication pending')
        except Exception as e:
            web_log(f"Plex OAuth error: {e}", "ERROR")
            return render_template('login.html', error=f'Authentication failed: {str(e)}')
    
    # Don't auto-login from saved auth - let user click login button
    # This prevents redirect loops
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout endpoint - clears session and saved auth"""
    username = session.get('plex_username', 'User')
    session.clear()
    
    # Delete saved auth file to force fresh login
    if os.path.exists(PLEX_AUTH_FILE):
        try:
            os.remove(PLEX_AUTH_FILE)
            web_log(f"{username} logged out (auth file deleted)", "INFO")
        except Exception as e:
            web_log(f"Failed to delete auth file: {e}", "ERROR")
    else:
        web_log(f"{username} logged out", "INFO")
    
    return redirect(url_for('login'))

@app.route('/')
def index():
    """Main entry point - smart routing based on configuration state"""
    
    # Simple check: do we have a session token?
    has_session = bool(session.get('plex_token'))
    
    # Check what's configured in environment
    has_plex_config = is_plex_configured()
    has_full_config = has_plex_config and is_tautulli_configured() and is_email_configured()
    
    # Route 1: No session → Must login first
    if not has_session:
        return redirect(url_for('login'))
    
    # Route 2: Has session, but Plex not configured in .env yet → Setup wizard
    if not has_plex_config:
        return render_template('setup.html')
    
    # Route 3: Has Plex but missing Tautulli/Email → Setup wizard
    if not has_full_config:
        return render_template('setup.html')
    
    # Route 4: Everything configured → Dashboard
    return render_template('dashboard.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/users')
@login_required
def users():
    """User management page"""
    return render_template('users.html')

@app.route('/settings')
@login_required
def settings():
    """Settings configuration page"""
    return render_template('settings.html')

@app.route('/logs')
@login_required
def logs_page():
    """Live logs viewer"""
    return render_template('logs.html')

@app.route('/email-history')
@login_required
def email_history_page():
    """Email send history viewer"""
    return render_template('email_history.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/plex/auth/pin', methods=['POST'])
def create_plex_pin():
    """Create a Plex authentication PIN"""
    try:
        pin_url = "https://plex.tv/api/v2/pins"
        headers = {
            'Accept': 'application/json',
            'X-Plex-Client-Identifier': PLEX_CLIENT_ID,
            'X-Plex-Product': PLEX_PRODUCT
        }
        data = {'strong': True}
        
        response = requests.post(pin_url, headers=headers, json=data)
        pin_data = response.json()
        
        return jsonify({
            'pin_id': pin_data['id'],
            'code': pin_data['code'],
            'auth_url': f"https://app.plex.tv/auth#!?clientID={PLEX_CLIENT_ID}&code={pin_data['code']}&context[device][product]={PLEX_PRODUCT}"
        })
    except Exception as e:
        web_log(f"Failed to create Plex PIN: {e}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/setup/complete', methods=['POST'])
def api_setup_complete():
    """Complete initial setup wizard"""
    try:
        config = request.json
        save_env_config(config)
        mark_setup_complete()
        web_log("Setup wizard completed successfully", "SUCCESS")
        return jsonify({'success': True})
    except Exception as e:
        web_log(f"Setup failed: {str(e)}", "ERROR")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/setup/status', methods=['GET'])
def api_setup_status():
    """Check if setup is complete"""
    return jsonify({'complete': is_setup_complete()})

@app.route('/api/session/check', methods=['GET'])
def api_session_check():
    """Check if user is authenticated and return session info"""
    if session.get('plex_token'):
        # User is logged in via Plex OAuth
        session_data = {
            'authenticated': True,
            'plex_token': session.get('plex_token'),
            'plex_username': session.get('plex_username'),
            'plex_email': session.get('plex_email'),
            'server_name': session.get('plex_server_name', '') or os.environ.get('PLEX_SERVER_NAME', '')
        }
        web_log(f"Session check: token={bool(session_data['plex_token'])}, server={session_data['server_name']}", "DEBUG")
        return jsonify(session_data)
    else:
        web_log("Session check: No plex_token in session", "DEBUG")
        return jsonify({'authenticated': False}), 401

@app.route('/api/config', methods=['GET'])
@api_login_required
def api_get_config():
    """Get current configuration (masked sensitive values)"""
    config = get_env_config()
    # Mask sensitive data
    if config['PLEX_TOKEN'] and len(config['PLEX_TOKEN']) > 4:
        config['PLEX_TOKEN'] = '••••' + config['PLEX_TOKEN'][-4:]
    if config['SMTP_PASSWORD']:
        config['SMTP_PASSWORD'] = '••••••••'
    if config['TAUTULLI_API_KEY'] and len(config['TAUTULLI_API_KEY']) > 4:
        config['TAUTULLI_API_KEY'] = '••••' + config['TAUTULLI_API_KEY'][-4:]
    if config['DISCORD_WEBHOOK'] and len(config['DISCORD_WEBHOOK']) > 20:
        config['DISCORD_WEBHOOK'] = config['DISCORD_WEBHOOK'][:50] + '••••'
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
@api_login_required
def api_save_config():
    """Save configuration updates"""
    try:
        new_config = request.json
        current = get_env_config()
        
        # Preserve masked values
        for key in new_config:
            if new_config[key] and '••••' in str(new_config[key]):
                new_config[key] = current[key]
        
        save_env_config(new_config)
        web_log("Configuration updated", "SUCCESS")
        return jsonify({'success': True})
    except Exception as e:
        web_log(f"Config save failed: {str(e)}", "ERROR")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/stats', methods=['GET'])
@api_login_required
def api_stats():
    """Get dashboard statistics"""
    try:
        state = daemon.load_state()
        all_users = daemon.plex_get_users()
        
        welcomed = state.get('welcomed', {})
        warned = state.get('warned', {})
        removed = state.get('removed', {})
        
        # Calculate users at risk (close to warning threshold)
        warn_days = int(os.environ.get('WARN_DAYS', 27))
        at_risk_count = 0
        
        stats = {
            'total_users': len(all_users),
            'active_users': len(welcomed) - len(warned),
            'warned_users': len(warned),
            'removed_users': len(removed),
            'at_risk_users': at_risk_count,  # Will implement proper calculation
            'dry_run_mode': os.environ.get('DRY_RUN', 'true').lower() in ('true', '1', 'yes'),
            'warn_threshold': warn_days,
            'kick_threshold': int(os.environ.get('KICK_DAYS', 30)),
            'daemon_status': 'running'  # Will add actual status check
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
@api_login_required
def api_users():
    """Get list of all users with detailed status"""
    try:
        state = daemon.load_state()
        plex_users = daemon.plex_get_users()
        welcomed = state.get('welcomed', {})
        warned = state.get('warned', {})
        removed = state.get('removed', {})
        
        # Get current VIP names using daemon's dynamic function
        vip_names = daemon.get_vip_names()
        web_log(f"Loaded VIP names: {vip_names}", "DEBUG")
        
        users_data = []
        
        for user in plex_users:
            uid = str(user['id'])
            username = (user.get('username') or '').lower()
            email = (user.get('email') or '').lower()
            
            # Determine user status
            if uid in removed:
                status = 'removed'
                badge_class = 'danger'
            elif uid in warned:
                status = 'warned'
                badge_class = 'warning'
            elif uid in welcomed:
                status = 'active'
                badge_class = 'success'
            else:
                status = 'new'
                badge_class = 'info'
            
            # Check VIP status - match by username OR email (for pending invites)
            is_vip = username in vip_names or email in vip_names
            
            # Debug logging for VIP status
            if is_vip:
                web_log(f"User {username or email} is VIP (found in: {vip_names})", "DEBUG")
            
            # Get last activity
            last_watch = None
            days_inactive = None
            try:
                t_users = daemon.tautulli('get_users')
                for tu in t_users:
                    if (tu.get('email', '') or '').lower() == (user['email'] or '').lower():
                        last_watch = daemon.tautulli_last_watch(tu.get('user_id'))
                        if last_watch:
                            days_inactive = (datetime.now(timezone.utc) - last_watch).days
                        break
            except:
                pass
            
            users_data.append({
                'id': uid,
                'name': user['title'] or user['username'] or 'Unknown',
                'email': user['email'] or '',
                'username': user['username'] or '',
                'status': status,
                'badge_class': badge_class,
                'is_vip': is_vip,
                'last_watch': last_watch.isoformat() if last_watch else None,
                'days_inactive': days_inactive,
                'welcomed_at': welcomed.get(uid),
                'warned_at': warned.get(uid),
                'removed_info': removed.get(uid)
            })
        
        return jsonify(users_data)
    except Exception as e:
        web_log(f"Error fetching users: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/welcome', methods=['POST'])
@api_login_required
def api_user_welcome(user_id):
    """Send welcome email to user"""
    try:
        users = daemon.plex_get_users()
        user = next((u for u in users if str(u['id']) == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        display = user['title'] or user['username'] or 'there'
        email = user['email']
        
        if not email:
            return jsonify({'error': 'User has no email address'}), 400
        
        daemon.send_email(email, "Access confirmed", daemon.welcome_email_html(display))
        
        # Update state
        state = daemon.load_state()
        state['welcomed'][user_id] = datetime.now(timezone.utc).isoformat()
        daemon.save_state(state)
        
        web_log(f"Welcome email sent to {display} ({email})", "SUCCESS")
        return jsonify({'success': True})
    except Exception as e:
        web_log(f"Welcome email failed: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/warn', methods=['POST'])
@api_login_required
def api_user_warn(user_id):
    """Send warning email to user"""
    try:
        users = daemon.plex_get_users()
        user = next((u for u in users if str(u['id']) == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        display = user['title'] or user['username'] or 'there'
        email = user['email']
        days = int(request.json.get('days', 28))
        
        if not email:
            return jsonify({'error': 'User has no email address'}), 400
        
        daemon.send_email(email, "Warning: Account inactivity", daemon.warn_email_html(display, days))
        
        # Update state
        state = daemon.load_state()
        state['warned'][user_id] = datetime.now(timezone.utc).isoformat()
        daemon.save_state(state)
        
        web_log(f"Warning email sent to {display} ({email})", "SUCCESS")
        return jsonify({'success': True})
    except Exception as e:
        web_log(f"Warning email failed: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/remove', methods=['POST'])
@api_login_required
def api_user_remove(user_id):
    """Remove user from Plex"""
    try:
        users = daemon.plex_get_users()
        user = next((u for u in users if str(u['id']) == user_id), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        display = user['title'] or user['username'] or 'there'
        email = user['email']
        
        # Attempt removal
        ok = daemon.remove_friend(daemon.get_plex_account(), user_id)
        
        if ok and email:
            daemon.send_email(email, "Access revoked", daemon.removal_email_html(display))
        
        # Update state
        state = daemon.load_state()
        state['removed'][user_id] = {
            'ok': ok,
            'reason': 'Manual removal via web interface',
            'when': datetime.now(timezone.utc).isoformat()
        }
        state['welcomed'].pop(user_id, None)
        state['warned'].pop(user_id, None)
        daemon.save_state(state)
        
        web_log(f"User removed: {display} - {'success' if ok else 'failed'}", "WARNING" if ok else "ERROR")
        return jsonify({'success': ok})
    except Exception as e:
        web_log(f"User removal failed: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/reset', methods=['POST'])
@api_login_required
def api_user_reset(user_id):
    """Reset user state (clear warnings/removals)"""
    try:
        state = daemon.load_state()
        state['warned'].pop(user_id, None)
        state['removed'].pop(user_id, None)
        daemon.save_state(state)
        
        web_log(f"User state reset for user ID {user_id}", "INFO")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<user_id>/vip', methods=['POST'])
@api_login_required
def api_user_toggle_vip(user_id):
    """Add or remove user from VIP list"""
    # Use threading lock to prevent race conditions during bulk operations
    with vip_lock:
        try:
            users = daemon.plex_get_users()
            user = next((u for u in users if str(u['id']) == user_id), None)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Use username if available, otherwise use email as identifier
            identifier = user.get('username') or user.get('email')
            
            if not identifier:
                return jsonify({'error': 'User has no username or email'}), 404
            
            # Normalize to lowercase for case-insensitive matching
            identifier = identifier.lower()
            
            # CRITICAL: Reload from file first to get latest VIP list (avoid race conditions)
            daemon.load_env_file(CONFIG_FILE)
            
            config = get_env_config()
            vip_names = [n.strip().lower() for n in config['VIP_NAMES'].split(',') if n.strip()]
            
            if identifier in vip_names:
                vip_names.remove(identifier)
                action = "removed from"
            else:
                vip_names.append(identifier)
                action = "added to"
            
            config['VIP_NAMES'] = ','.join(vip_names)
            save_env_config(config)
            
            web_log(f"User {identifier} {action} VIP list", "INFO")
            return jsonify({'success': True, 'is_vip': identifier in vip_names})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/users/import', methods=['POST'])
@api_login_required
def api_import_users():
    """Import all existing Plex users and mark them as welcomed"""
    try:
        # Get all Plex users
        plex_users = daemon.plex_get_users()
        
        # Load current state
        state = daemon.load_state()
        welcomed = state.get('welcomed', {})
        
        # Track imported users
        imported = []
        skipped = []
        
        now = datetime.now(timezone.utc).isoformat()
        
        for user in plex_users:
            uid = str(user['id'])
            display_name = user['title'] or user['username'] or 'Unknown User'
            email = user['email'] or ''
            
            # Skip if already welcomed
            if uid in welcomed:
                skipped.append({
                    'id': uid,
                    'name': display_name,
                    'email': email,
                    'reason': 'Already welcomed'
                })
                continue
            
            # Add to welcomed list
            welcomed[uid] = {
                'timestamp': now,
                'display_name': display_name,
                'email': email,
                'imported': True  # Flag to indicate this was imported, not auto-discovered
            }
            
            imported.append({
                'id': uid,
                'name': display_name,
                'email': email
            })
        
        # Save updated state
        state['welcomed'] = welcomed
        daemon.save_state(state)
        
        web_log(f"Imported {len(imported)} existing Plex users, skipped {len(skipped)}", "INFO")
        
        return jsonify({
            'success': True,
            'imported': imported,
            'skipped': skipped,
            'total_imported': len(imported),
            'total_skipped': len(skipped)
        })
        
    except Exception as e:
        web_log(f"Error importing users: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test/email', methods=['POST'])
def api_test_email():
    """Send test email with improved error handling"""
    try:
        data = request.json or {}
        email = data.get('email') or data.get('ADMIN_EMAIL')
        
        # Get SMTP config from request or environment (support both uppercase and lowercase)
        smtp_host = data.get('SMTP_HOST') or data.get('smtp_host') or os.environ.get('SMTP_HOST')
        smtp_port = data.get('SMTP_PORT') or data.get('smtp_port') or os.environ.get('SMTP_PORT')
        smtp_username = data.get('SMTP_USERNAME') or data.get('smtp_username') or os.environ.get('SMTP_USERNAME')
        smtp_password = data.get('SMTP_PASSWORD') or data.get('smtp_password') or os.environ.get('SMTP_PASSWORD')
        smtp_from = data.get('SMTP_FROM') or data.get('smtp_from') or os.environ.get('SMTP_FROM')
        
        if not email:
            return jsonify({'status': 'error', 'error': 'Email address required'}), 400
        
        if not all([smtp_host, smtp_port, smtp_username, smtp_password, smtp_from]):
            return jsonify({'status': 'error', 'error': 'Complete SMTP configuration required'}), 400
        
        # Temporarily set environment for test
        old_host = os.environ.get('SMTP_HOST')
        old_port = os.environ.get('SMTP_PORT')
        old_user = os.environ.get('SMTP_USERNAME')
        old_pass = os.environ.get('SMTP_PASSWORD')
        old_from = os.environ.get('SMTP_FROM')
        
        os.environ['SMTP_HOST'] = smtp_host
        os.environ['SMTP_PORT'] = str(smtp_port)
        os.environ['SMTP_USERNAME'] = smtp_username
        os.environ['SMTP_PASSWORD'] = smtp_password
        os.environ['SMTP_FROM'] = smtp_from
        
        try:
            daemon.send_email(email, "Plex-Auto-Prune GUI Test Email", daemon.welcome_email_html("Test User"))
            web_log(f"Test email sent to {email}", "SUCCESS")
            return jsonify({'status': 'success', 'success': True})
        finally:
            # Restore original environment
            for key, old_val in [('SMTP_HOST', old_host), ('SMTP_PORT', old_port), 
                                  ('SMTP_USERNAME', old_user), ('SMTP_PASSWORD', old_pass), 
                                  ('SMTP_FROM', old_from)]:
                if old_val:
                    os.environ[key] = old_val
                elif key in os.environ:
                    del os.environ[key]
                    
    except smtplib.SMTPAuthenticationError as e:
        error_msg = 'SMTP authentication failed. Check your username and password.'
        web_log(f"Email test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except smtplib.SMTPConnectError as e:
        error_msg = 'Cannot connect to SMTP server. Check host and port.'
        web_log(f"Email test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except socket.timeout:
        error_msg = 'SMTP connection timeout. Check your network and firewall settings.'
        web_log(f"Email test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except Exception as e:
        error_msg = f'Email test failed: {str(e)}'
        web_log(error_msg, "ERROR")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/test/discord', methods=['POST'])
def api_test_discord():
    """Send test Discord notifications"""
    try:
        data = request.json or {}
        webhook = data.get('DISCORD_WEBHOOK') or data.get('webhook') or os.environ.get('DISCORD_WEBHOOK')
        
        if not webhook:
            return jsonify({'error': 'Discord webhook URL required'}), 400
        
        # Temporarily set environment for test
        old_webhook = os.environ.get('DISCORD_WEBHOOK')
        os.environ['DISCORD_WEBHOOK'] = webhook
        
        try:
            daemon.test_discord_notifications()
            web_log("Test Discord notifications sent", "SUCCESS")
            return jsonify({'success': True})
        finally:
            # Restore original environment
            if old_webhook:
                os.environ['DISCORD_WEBHOOK'] = old_webhook
            elif 'DISCORD_WEBHOOK' in os.environ:
                del os.environ['DISCORD_WEBHOOK']
                
    except Exception as e:
        web_log(f"Discord test failed: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test/plex', methods=['POST'])
def api_test_plex():
    """Test Plex connection with improved error handling"""
    try:
        # Get token from request body (for setup wizard) or environment
        data = request.json or {}
        # Support both formats: uppercase (from form) and lowercase (legacy)
        token = data.get('PLEX_TOKEN') or data.get('token') or os.environ.get('PLEX_TOKEN')
        server_name = data.get('PLEX_SERVER_NAME') or data.get('server_name') or os.environ.get('PLEX_SERVER_NAME', 'MyPlexServer')
        
        if not token:
            return jsonify({'status': 'error', 'error': 'Plex token required'}), 400
        
        # Temporarily set environment for test
        old_token = os.environ.get('PLEX_TOKEN')
        old_server = os.environ.get('PLEX_SERVER_NAME')
        
        os.environ['PLEX_TOKEN'] = token
        os.environ['PLEX_SERVER_NAME'] = server_name
        
        try:
            acct = daemon.get_plex_account()
            users = daemon.plex_get_users()
            web_log(f"Plex connection successful: {len(users)} users", "SUCCESS")
            
            # Safely get username and email (handle encoding issues)
            username = getattr(acct, 'username', 'Unknown')
            email = getattr(acct, 'email', '')
            
            return jsonify({
                'status': 'success',
                'success': True,
                'username': str(username),
                'email': str(email),
                'user_count': len(users)
            })
        finally:
            # Restore original environment
            if old_token:
                os.environ['PLEX_TOKEN'] = old_token
            elif 'PLEX_TOKEN' in os.environ:
                del os.environ['PLEX_TOKEN']
            
            if old_server:
                os.environ['PLEX_SERVER_NAME'] = old_server
            elif 'PLEX_SERVER_NAME' in os.environ:
                del os.environ['PLEX_SERVER_NAME']
            
    except requests.exceptions.Timeout:
        error_msg = 'Plex connection timeout. Check your network connection.'
        web_log(f"Plex test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except requests.exceptions.ConnectionError:
        error_msg = 'Cannot connect to Plex. Check if Plex is running and accessible.'
        web_log(f"Plex test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except Exception as e:
        error_msg = f'Plex test failed: {str(e)}'
        web_log(error_msg, "ERROR")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/test/tautulli', methods=['POST'])
def api_test_tautulli():
    """Test Tautulli connection"""
    try:
        # Get config from request body (for setup wizard) or environment
        data = request.json or {}
        tautulli_url = data.get('TAUTULLI_URL') or data.get('url') or os.environ.get('TAUTULLI_URL')
        tautulli_key = data.get('TAUTULLI_API_KEY') or data.get('api_key') or os.environ.get('TAUTULLI_API_KEY')
        
        if not tautulli_url or not tautulli_key:
            return jsonify({'status': 'error', 'error': 'Tautulli URL and API key required'}), 400
        
        # Temporarily set environment for test
        old_url = os.environ.get('TAUTULLI_URL')
        old_key = os.environ.get('TAUTULLI_API_KEY')
        
        os.environ['TAUTULLI_URL'] = tautulli_url
        os.environ['TAUTULLI_API_KEY'] = tautulli_key
        
        try:
            users = daemon.tautulli('get_users')
            web_log(f"Tautulli connection successful: {len(users)} users", "SUCCESS")
            return jsonify({
                'status': 'success',
                'success': True,
                'user_count': len(users)
            })
        finally:
            # Restore original environment
            if old_url:
                os.environ['TAUTULLI_URL'] = old_url
            elif 'TAUTULLI_URL' in os.environ:
                del os.environ['TAUTULLI_URL']
            
            if old_key:
                os.environ['TAUTULLI_API_KEY'] = old_key
            elif 'TAUTULLI_API_KEY' in os.environ:
                del os.environ['TAUTULLI_API_KEY']
            
    except requests.exceptions.Timeout:
        error_msg = 'Tautulli connection timeout. Check your Tautulli URL and network connection.'
        web_log(f"Tautulli test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except requests.exceptions.ConnectionError:
        error_msg = 'Cannot connect to Tautulli. Verify the URL is correct and Tautulli is running.'
        web_log(f"Tautulli test failed: {error_msg}", "ERROR")
        return jsonify({'status': 'error', 'error': error_msg}), 500
    except Exception as e:
        error_msg = f'Tautulli test failed: {str(e)}'
        web_log(error_msg, "ERROR")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
@api_login_required
def api_get_logs():
    """Get log history"""
    return jsonify({'logs': log_buffer})

@app.route('/api/first-run/import-users', methods=['POST'])
def api_import_existing_users():
    """Import all existing Plex users as already welcomed (first-run setup)"""
    try:
        count = daemon.import_existing_users_as_welcomed()
        web_log(f"Imported {count} existing users as already welcomed", "INFO")
        return jsonify({
            'success': True, 
            'imported_count': count,
            'message': f'Successfully imported {count} existing users'
        })
    except Exception as e:
        web_log(f"Failed to import existing users: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/first-run/skip-import', methods=['POST'])
def api_skip_import():
    """Skip user import and mark first run as complete"""
    try:
        state = daemon.load_state()
        state['first_run_complete'] = True
        daemon.save_state(state)
        web_log("Skipped user import, first run marked as complete", "INFO")
        return jsonify({'success': True})
    except Exception as e:
        web_log(f"Failed to skip import: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/email-history', methods=['GET'])
@api_login_required
def api_get_email_history():
    """Get email send history"""
    try:
        state = daemon.load_state()
        # Return last 100 emails, most recent first
        history = state.get('email_history', [])[-100:]
        history.reverse()
        return jsonify({'emails': history, 'total': len(state.get('email_history', []))})
    except Exception as e:
        web_log(f"Failed to retrieve email history: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/first-run/status', methods=['GET'])
def api_first_run_status():
    """Check if this is the first run"""
    try:
        state = daemon.load_state()
        return jsonify({
            'is_first_run': not state.get('first_run_complete', False),
            'welcomed_count': len(state.get('welcomed', {})),
            'email_count': len(state.get('email_history', []))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/daemon/status', methods=['GET'])
@api_login_required
def api_daemon_status():
    """Get daemon monitoring status"""
    try:
        return jsonify({
            'enabled': daemon.daemon_enabled,
            'dry_run': os.environ.get('DRY_RUN', 'true').lower() in ('true', '1', 'yes')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/daemon/start', methods=['POST'])
@api_login_required
def api_daemon_start():
    """Enable daemon monitoring"""
    try:
        daemon.save_daemon_control(True)
        web_log("Daemon monitoring enabled by user", "SUCCESS")
        return jsonify({'success': True, 'enabled': True})
    except Exception as e:
        web_log(f"Failed to enable daemon: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/daemon/stop', methods=['POST'])
@api_login_required
def api_daemon_stop():
    """Disable daemon monitoring"""
    try:
        daemon.save_daemon_control(False)
        web_log("Daemon monitoring disabled by user", "WARNING")
        return jsonify({'success': True, 'enabled': False})
    except Exception as e:
        web_log(f"Failed to disable daemon: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

# ==================== BACKUP & RESTORE ====================

@app.route('/api/backup', methods=['GET'])
@api_login_required
def api_backup():
    """Create and download a backup of configuration and state"""
    import zipfile
    import io
    from datetime import datetime
    
    try:
        # Create in-memory ZIP file
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add .env file if it exists
            if os.path.exists('.env'):
                zip_file.write('.env', 'config.env')
            
            # Add state.json if it exists
            state_path = os.path.join('state', 'state.json')
            if os.path.exists(state_path):
                zip_file.write(state_path, 'state.json')
            
            # Add a backup manifest
            manifest = {
                'backup_date': datetime.now().isoformat(),
                'version': '1.0',
                'files': ['config.env', 'state.json']
            }
            import json
            zip_file.writestr('manifest.json', json.dumps(manifest, indent=2))
        
        zip_buffer.seek(0)
        
        web_log("Configuration backup created", "INFO")
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'guardian-backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}.zip'
        )
    except Exception as e:
        web_log(f"Backup failed: {str(e)}", "ERROR")
        return jsonify({'error': str(e)}), 500

@app.route('/api/restore', methods=['POST'])
@api_login_required
def api_restore():
    """Restore configuration and state from backup"""
    import zipfile
    import tempfile
    
    try:
        if 'backup' not in request.files:
            return jsonify({'status': 'error', 'message': 'No backup file provided'}), 400
        
        backup_file = request.files['backup']
        
        if not backup_file.filename.endswith('.zip'):
            return jsonify({'status': 'error', 'message': 'Invalid file type. Must be a .zip file'}), 400
        
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            temp_zip = os.path.join(temp_dir, 'backup.zip')
            backup_file.save(temp_zip)
            
            # Extract ZIP
            with zipfile.ZipFile(temp_zip, 'r') as zip_file:
                zip_file.extractall(temp_dir)
            
            # Restore .env
            config_file = os.path.join(temp_dir, 'config.env')
            if os.path.exists(config_file):
                import shutil
                shutil.copy(config_file, '.env')
                web_log("Configuration restored from backup", "INFO")
            
            # Restore state.json
            state_backup = os.path.join(temp_dir, 'state.json')
            if os.path.exists(state_backup):
                import shutil
                os.makedirs('state', exist_ok=True)
                shutil.copy(state_backup, os.path.join('state', 'state.json'))
                web_log("User state restored from backup", "INFO")
        
        # Restart daemon to pick up new configuration
        daemon.save_daemon_control(False)
        web_log("Backup restored successfully. Daemon will restart.", "SUCCESS")
        
        return jsonify({
            'status': 'success',
            'message': 'Backup restored successfully. Daemon restarting...'
        })
    except Exception as e:
        web_log(f"Restore failed: {str(e)}", "ERROR")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/health')
def health_check():
    """Health check endpoint for Docker healthcheck"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now(timezone.utc).isoformat()}), 200

# ==================== WEBSOCKET EVENTS ====================

@socketio.on('connect')
def handle_connect():
    """Handle client connection - send log history"""
    emit('log_history', {'logs': log_buffer})
    web_log("Web client connected", "INFO")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    web_log("Web client disconnected", "INFO")

# ==================== STARTUP ====================

if __name__ == '__main__':
    web_log("=" * 60, "INFO")
    web_log("Plex-Auto-Prune GUI Starting", "INFO")
    web_log("Web UI will be available at http://0.0.0.0:8080", "INFO")
    web_log("=" * 60, "INFO")
    
    # Run web server
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)
