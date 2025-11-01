# Complete Feature List - Plex-Auto-Prune GUI

## 🎯 **WEB INTERFACE**

### **Setup Wizard** (`/` - first run)
- First-time configuration wizard
- Real-time connection testing for all services
- Guided setup with validation
- Automatic `.env` file generation
- Setup completion flag tracking

### **Dashboard** (`/dashboard`)
- **Statistics Cards:**
  - Total users count
  - Active users (recently watched)
  - Warned users count
  - Removed users count
  - VIP users count
- **Real-time System Status:**
  - Daemon running status
  - DRY_RUN mode indicator
  - Configuration status
  - Last activity timestamp
- **Live Updates via WebSockets**

### **User Management** (`/users`)
- **User Table with:**
  - Name and username display
  - Email addresses
  - Status badges (Active/Warned/Removed)
  - Last activity tracking
  - Days inactive calculation
  - VIP status display
- **Filtering & Sorting:**
  - Search by name, email, username
  - Filter by status (Active/Warned/Removed)
  - Sort by any column (name, email, status, last active)
- **Manual Actions:**
  - Send welcome email
  - Send warning email
  - Remove user from Plex
  - Reset user status
  - Add/Remove VIP status

### **Settings** (`/settings`)
- **Live Configuration Editor**
- **Sections:**
  - Plex configuration (token, server name)
  - Tautulli configuration (URL, API key)
  - Email/SMTP configuration
  - Discord webhook (optional)
  - User management thresholds (warn/kick days)
  - Check intervals
  - VIP user list management
  - DRY_RUN mode toggle
- **Connection Testing:**
  - Test Plex connection
  - Test Tautulli API
  - Test email delivery
  - Test Discord webhook
- **Save & Apply** - Updates `.env` and reloads configuration

### **Logs Viewer** (`/logs`)
- Real-time log streaming via WebSockets
- Log level indicators (INFO, WARNING, ERROR, SUCCESS)
- Timestamp display
- Auto-scroll to latest
- In-memory log buffer (1000 entries)

---

## 🤖 **AUTOMATED DAEMON FEATURES**

### **Fast Join Watcher** (Every 2 minutes by default)
- **Detects new Plex users**
- **Auto-Welcome Emails** (configurable):
  - Enabled by default (`AUTO_WELCOME_NEW_USERS=true`)
  - Optional delay (`AUTO_WELCOME_DELAY_HOURS`)
  - Custom HTML templates supported
  - Sends to user's registered email
  - Admin notification email
  - Discord notification
- **Rejoined User Detection:**
  - Detects users who return after removal
  - Automatically re-welcomes them
  - Moves from "removed" to "welcomed" state
  - Admin notification
  - Discord notification
- **State Tracking:**
  - Records join timestamp
  - Maintains welcomed user list
  - Persists to `state.json`

### **Slow Inactivity Watcher** (Every 30 minutes by default)
- **Monitors user activity via Tautulli**
- **Inactivity Warnings:**
  - Calculates days since last watch
  - Sends warning at `WARN_DAYS` threshold (default: 27 days)
  - Beautiful HTML email with countdown
  - Admin notification
  - Discord notification
  - Tracks warned timestamp
- **Auto-Removal:**
  - Removes users at `KICK_DAYS` threshold (default: 30 days)
  - Removes Plex server access
  - Removes from Plex friends
  - Sends removal notification email
  - Admin notification
  - Discord notification
  - Moves to "removed" state
- **VIP Protection:**
  - Admin email always VIP
  - Custom VIP list (`VIP_NAMES` env var)
  - VIP users never auto-removed
  - VIP status visible in UI
- **Smart Skipping:**
  - Skips users without email
  - Skips VIP users
  - Skips already processed users
  - Prevents duplicate emails

---

## 📧 **EMAIL SYSTEM**

### **Email Types**
1. **Welcome Email** - New user onboarding
2. **Warning Email** - Inactivity warning (X days remaining)
3. **Removal Email** - Access revoked notification
4. **Admin Join Email** - Admin notification of new users
5. **Admin Removed Email** - Admin notification of removals

### **Email Features**
- **Beautiful Terminal-Themed Design:**
  - Centauri cyan/purple color scheme
  - Monospace fonts
  - Terminal-style boxes
  - ASCII art server emblem
  - Responsive HTML
- **Customizable Branding:**
  - Server name (`SERVER_NAME`)
  - Brand colors (cyan, purple, accent colors)
  - Footer links (Discord, Overseerr, Portfolio)
  - Text colors and backgrounds
- **Custom HTML Templates:**
  - Drop-in replacement via `email_templates/` folder
  - Supports: `welcome.html`, `warning.html`, `removal.html`
  - Automatic placeholder replacement
  - Designer attribution footer
- **Placeholders Available:**
  - `{{NAME}}` - User's display name
  - `{{SERVER_NAME}}` - Your server name
  - `{{DAYS_REMAINING}}` - Days until removal (warning emails)
  - `{{LINK_DISCORD}}` - Discord invite link
  - `{{LINK_OVERSEERR}}` - Overseerr URL
  - `{{ADMIN_EMAIL}}` - Admin contact email
  - Server emblem SVG inline

---

## 🔔 **DISCORD INTEGRATION** (Optional)

- **Webhook notifications for:**
  - New user joins: `👤 New Plex user joined: {name}`
  - User rejoined: `🔄 User rejoined Plex: {name}`
  - Warning sent: `⚠️ Warning sent to: {name}`
  - User removed: `❌ User removed: {name}`
- **Test command available:** `python daemon.py test-discord`
- **Configurable via:** `DISCORD_WEBHOOK` environment variable
- **Fully optional** - Works without Discord

---

## 🔐 **PLEX INTEGRATION**

### **PlexAPI Features**
- **Authentication** via X-Plex-Token
- **User Management:**
  - List all shared users
  - Get user details (name, email, username, ID)
  - Remove server access
  - Unfriend users
  - Get shared server mappings
- **Server Information:**
  - Get server machine ID
  - Validate server access
  - Server name matching

### **Tautulli Integration**
- **Activity Tracking:**
  - Get last watch timestamp per user
  - Calculate days inactive
  - User history lookup
- **API Commands:**
  - `get_users` - User list
  - `get_user_watch_time_stats` - Activity data
- **Connection Testing:**
  - Validate API key
  - Test connectivity
  - Error handling with retries

---

## 💾 **STATE MANAGEMENT**

### **JSON State File** (`state/state.json`)
```json
{
  "welcomed": {"user_id": "2025-10-31T12:00:00+00:00"},
  "warned": {"user_id": "2025-10-31T12:00:00+00:00"},
  "removed": {"user_id": "2025-10-31T12:00:00+00:00"},
  "vip": ["user_id_1", "user_id_2"]
}
```

### **State Tracking:**
- Welcomed users with timestamp
- Warned users with timestamp
- Removed users with timestamp
- VIP user IDs
- UTF-8 encoding
- Atomic writes
- Auto-creation if missing

---

## ⚙️ **CONFIGURATION**

### **Required Environment Variables**
- `PLEX_TOKEN` - Plex authentication token
- `PLEX_SERVER_NAME` - Exact server name
- `TAUTULLI_URL` - Full Tautulli URL
- `TAUTULLI_API_KEY` - Tautulli API key
- `SMTP_HOST` - SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP port (587 for TLS)
- `SMTP_USERNAME` - SMTP login
- `SMTP_PASSWORD` - SMTP password/app password
- `SMTP_FROM` - From email address
- `ADMIN_EMAIL` - Admin notification email

### **Optional Settings**
- `WARN_DAYS` (default: 27) - Days before warning
- `KICK_DAYS` (default: 30) - Days before removal
- `AUTO_WELCOME_NEW_USERS` (default: true) - Enable auto-welcome
- `AUTO_WELCOME_DELAY_HOURS` (default: 0) - Welcome delay
- `CHECK_NEW_USERS_SECS` (default: 120) - New user check interval
- `CHECK_INACTIVITY_SECS` (default: 1800) - Inactivity check interval
- `VIP_NAMES` - Comma-separated VIP usernames
- `DISCORD_WEBHOOK` - Discord webhook URL
- `LINK_DISCORD` - Discord invite link
- `LINK_OVERSEERR` - Overseerr URL
- `LINK_PORTFOLIO` - Personal portfolio URL
- `DRY_RUN` (default: true) - Test mode
- **Branding Variables:**
  - `SERVER_NAME` - Your server display name
  - `BRAND_COLOR` - Primary brand color (hex)
  - `BRAND_ACCENT_WARN` - Warning color (hex)
  - `BRAND_ACCENT_DANGER` - Danger/removal color (hex)
  - `BRAND_TEXT` - Primary text color (hex)
  - `BRAND_TEXT_MUTED` - Muted text color (hex)
  - `BRAND_BG` - Background color (hex)

---

## 🛡️ **SAFETY FEATURES**

### **DRY_RUN Mode** (Default: Enabled)
- No actual removals performed
- No emails sent
- Logs all actions that WOULD happen
- Safe for testing
- Must explicitly disable for production

### **VIP Protection**
- Admin always protected
- Custom VIP list support
- Never auto-removed
- Never auto-warned
- Clear UI indicators

### **Error Handling**
- Retry logic for Plex API (3 attempts)
- Graceful error logging
- Continues on non-critical errors
- Email failure handling
- Connection validation

### **Validation**
- Required environment variable checking
- Email address validation
- API key validation
- Connection testing before operations
- Configuration validation in setup wizard

---

## 🐳 **DOCKER FEATURES**

- **Multi-stage build** (Python 3.11-slim)
- **Volume mounts:**
  - `.env` file persistence
  - `state/` directory persistence
  - `email_templates/` custom templates
- **Port 8080** - Web interface
- **Health checks** - Container monitoring
- **Auto-restart** - Unless stopped
- **Signal handling** - Graceful shutdown (SIGTERM, SIGINT)
- **Daemon threads** - Background processing

---

## 📊 **API ENDPOINTS**

### **Setup & Config**
- `POST /api/setup/complete` - Complete wizard
- `GET /api/setup/status` - Check setup status
- `GET /api/config` - Get current config (masked)
- `POST /api/config` - Update configuration

### **User Management**
- `GET /api/users` - List all users with status
- `POST /api/users/<id>/welcome` - Manually welcome user
- `POST /api/users/<id>/warn` - Manually warn user
- `POST /api/users/<id>/remove` - Manually remove user
- `POST /api/users/<id>/reset` - Reset user state
- `POST /api/users/<id>/vip` - Toggle VIP status

### **Testing**
- `POST /api/test/plex` - Test Plex connection
- `POST /api/test/tautulli` - Test Tautulli API
- `POST /api/test/email` - Test email delivery
- `POST /api/test/discord` - Test Discord webhook

### **Monitoring**
- `GET /api/stats` - Dashboard statistics
- `GET /api/logs` - Recent logs

### **WebSocket Events**
- `log` - Real-time log streaming
- Auto-reconnect on disconnect

---

## 🎨 **UI/UX FEATURES**

- **Terminal-inspired theme** (Centauri cyan/purple)
- **Responsive design** - Mobile, tablet, desktop
- **Real-time updates** - WebSocket-powered
- **Loading states** - Visual feedback
- **Error notifications** - Toast messages
- **Sort & filter** - User-friendly tables
- **One-click actions** - Confirmation modals
- **Status badges** - Color-coded (green/yellow/red)
- **Monospace fonts** - JetBrains Mono / Consolas
- **Dark mode only** - Terminal aesthetic

---

## 📁 **FILE STRUCTURE**

```
plex-autoprune-GUI/
├── daemon.py              # Background monitoring daemon (1300+ lines)
├── web.py                 # Flask web interface (600+ lines)
├── main.py               # Combined launcher
├── docker-compose.yml    # Docker orchestration
├── Dockerfile            # Container build
├── requirements.txt      # Python dependencies
├── .env.example          # Configuration template
├── README.md             # Main documentation
├── DEPLOYMENT.md         # Deployment guide
├── TESTING.md            # Testing guide
├── FEATURES.md           # This file
├── templates/            # HTML templates
│   ├── base.html        # Base template with CSS/JS
│   ├── dashboard.html   # Dashboard page
│   ├── users.html       # User management page
│   ├── settings.html    # Settings page
│   ├── logs.html        # Logs viewer page
│   └── setup.html       # Setup wizard page
├── static/              # Static assets (if any)
├── state/               # Persistent state (gitignored)
│   ├── state.json       # User state tracking
│   └── .setup_complete  # Setup completion flag
└── email_templates/     # Custom email templates (optional)
    ├── README.md        # Template documentation
    ├── welcome.html     # Custom welcome template
    ├── warning.html     # Custom warning template
    └── removal.html     # Custom removal template
```

---

## 🔧 **TECHNICAL STACK**

### **Backend**
- **Python 3.11** - Core language
- **Flask 3.0.0** - Web framework
- **Flask-SocketIO 5.3.0** - WebSocket support
- **PlexAPI 4.15.0** - Plex integration
- **python-dateutil 2.8.2** - Date/time parsing
- **requests** - HTTP client
- **eventlet** - Async server

### **Frontend**
- **Vanilla JavaScript** - No frameworks
- **WebSocket.io** - Real-time communication
- **Responsive CSS** - Mobile-first design
- **HTML5** - Semantic markup

### **Infrastructure**
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **Volume Mounts** - Data persistence
- **Signal Handling** - Graceful shutdown

---

## 📈 **MONITORING & LOGGING**

- **Structured logging** with timestamps
- **Log levels:** INFO, WARNING, ERROR, SUCCESS
- **Real-time log streaming** to web UI
- **In-memory log buffer** (last 1000 entries)
- **Console output** with flush for Docker logs
- **Error stack traces** for debugging
- **Daemon tick counters** for monitoring
- **Action summaries** (users warned, removed, etc.)

---

## 🚀 **DEPLOYMENT OPTIONS**

1. **Docker Compose** (Recommended)
   - Simple `docker-compose up -d`
   - Automatic restarts
   - Volume persistence

2. **Standalone Docker**
   - Manual container management
   - Direct `docker run` commands

3. **Python Direct** (Development)
   - `python main.py`
   - Requires manual dependency installation
   - For development/testing only

4. **TrueNAS SCALE**
   - Custom app deployment
   - Docker Compose integration
   - See DEPLOYMENT.md

5. **Portainer**
   - Stack deployment
   - Web-based management
   - See DEPLOYMENT.md

---

## 🔄 **WORKFLOW**

### **New User Onboarding**
1. User joins Plex server
2. Fast Join Watcher detects new user (within 2 minutes)
3. Optional delay applied if configured
4. Welcome email sent to user
5. Admin notification email sent
6. Discord notification posted (if configured)
7. User added to "welcomed" state with timestamp

### **Inactivity Management**
1. Slow Inactivity Watcher checks activity (every 30 minutes)
2. Queries Tautulli for last watch time
3. Calculates days inactive
4. At `WARN_DAYS` (default 27):
   - Warning email sent to user
   - Admin notification sent
   - Discord notification posted
   - User added to "warned" state
5. At `KICK_DAYS` (default 30):
   - Removal email sent to user
   - Plex access removed
   - User unfriended
   - Admin notification sent
   - Discord notification posted
   - User moved to "removed" state

### **Manual Management**
1. Admin views user in web UI
2. Admin clicks action button (Welcome/Warn/Remove/Reset)
3. Action performed immediately
4. State updated
5. Emails sent
6. UI refreshed with new status

---

## 🎯 **FEATURE SUMMARY**

- **100+ features** across automation, UI, email, integrations, and safety
- **5 web pages** with real-time updates
- **21 API endpoints** for complete control
- **5 email templates** (3 customizable)
- **2 daemon threads** for continuous monitoring
- **4 integration points** (Plex, Tautulli, Email, Discord)
- **Fully configurable** via environment variables
- **Production-ready** with DRY_RUN safety mode
- **Beautiful UI** with terminal aesthetic
- **Comprehensive documentation** across multiple guides

---

**Built with ❤️ for the Plex community**
