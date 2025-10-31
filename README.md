# Plex-Auto-Prune GUI - Plex User Management

A sophisticated web interface for automated Plex user management. Plex-Auto-Prune GUI monitors user activity via Tautulli and automatically manages access based on inactivity, with a beautiful terminal-themed web dashboard.

## Features

### 🎯 Complete Web Interface
- **Setup Wizard** - Easy first-time configuration with connection testing
- **Dashboard** - Real-time statistics and system overview
- **User Management** - View, filter, and manually manage all users
- **Settings** - Live configuration with validation
- **Log Viewer** - Real-time log streaming via WebSockets

### 🤖 Automated Management
- **New User Welcome** - Automatic welcome emails for new users
- **Inactivity Warnings** - Warning emails at configurable threshold
- **Auto-Removal** - Remove inactive users after grace period
- **Rejoined Detection** - Re-welcome users who return after removal
- **VIP Protection** - Protect friends/family from auto-removal

### 🎨 Beautiful UI
- **Terminal Theme** - Centauri-inspired dark mode design
- **Responsive** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Live statistics and logs via WebSockets
- **One-Click Actions** - Manual welcome/warn/remove from GUI

## Quick Start (Docker)

### 1. Clone or Download

```bash
cd plex-auto-prune-gui
```

### 2. First-Time Setup

```bash
docker-compose up --build
```

### 3. Access Web Interface

Open your browser to: **http://localhost:8080**

The setup wizard will guide you through configuration:
- Plex authentication
- Tautulli integration
- Email settings (Gmail)
- Discord webhooks (optional)
- Thresholds and VIP users

### 4. Start Managing!

Once setup is complete, Plex-Auto-Prune GUI will:
- Run the monitoring daemon in the background
- Provide a web dashboard at port 8080
- Automatically manage users based on your settings

## Configuration

All configuration is done through the web interface during setup, or via the Settings page.

### Required Settings

| Setting | Description |
|---------|-------------|
| **PLEX_TOKEN** | Your Plex authentication token |
| **TAUTULLI_URL** | Full URL to your Tautulli instance |
| **TAUTULLI_API_KEY** | Tautulli API key |
| **SMTP Settings** | Gmail SMTP configuration |
| **ADMIN_EMAIL** | Where to send admin notifications |

### Optional Settings

| Setting | Default | Description |
|---------|---------|-------------|
| **WARN_DAYS** | 27 | Days before warning email |
| **KICK_DAYS** | 30 | Days before removal |
| **VIP_NAMES** | - | Comma-separated usernames to protect |
| **DISCORD_WEBHOOK** | - | Discord webhook URL for notifications |
| **DRY_RUN** | true | Test mode (no actual removals) |

## Docker Deployment

### TrueNAS Scale / Portainer

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide including:
- Portainer stack configuration
- Volume setup and permissions
- Environment variable configuration
- Security recommendations
- Troubleshooting common issues
- Backup and update procedures

**Quick Deploy:**

1. Create persistent volume for state:
  ```bash
  mkdir -p /mnt/app-pool/plex-auto-prune-gui/state
  ```

2. Deploy stack using `docker-compose.yml`

3. Access at `http://your-server-ip:8080`

### Environment Variables

You can pre-configure via environment variables or use the web setup wizard:

```yaml
environment:
  PLEX_TOKEN: your_token
  TAUTULLI_URL: http://192.168.1.100:8181
  TAUTULLI_API_KEY: your_key
  # ... etc
```

## Web Interface Pages

### Dashboard
- Total users, active, warned, removed counts
- System status (daemon, dry run mode)
- Recent activity timeline
- Quick stats at a glance

### Users
- Sortable table of all Plex users
- Status badges (Active, Warned, At Risk, Removed)
- Last activity and days inactive
- One-click actions:
  - Send welcome email
  - Send warning
  - Remove user
  - Reset state
  - Add/remove from VIP list

### Settings
- Live configuration editor
- Test connections (Plex, Tautulli, Email, Discord)
- Adjust thresholds
- Manage VIP list
- Toggle dry run mode

### Logs
- Real-time log streaming
- Filter by level (INFO, SUCCESS, WARNING, ERROR)
- Search logs
- Auto-scroll

## Email Templates

Plex-Auto-Prune GUI sends beautiful HTML emails with a terminal aesthetic:
- **Welcome** - Sent to new users
- **Warning** - Inactivity warning before removal
- **Removal** - Sent when user is removed
- **Admin Notifications** - Detailed alerts for admins

## API Endpoints

The web interface exposes a REST API:

```
GET  /api/stats          - Dashboard statistics
GET  /api/users          - List all users with status
GET  /api/config         - Current configuration
POST /api/config         - Update configuration
POST /api/users/:id/welcome  - Send welcome email
POST /api/users/:id/warn     - Send warning
POST /api/users/:id/remove   - Remove user
POST /api/users/:id/reset    - Reset user state
POST /api/users/:id/vip      - Toggle VIP status
POST /api/test/email     - Test email
POST /api/test/discord   - Test Discord
POST /api/test/plex      - Test Plex connection
POST /api/test/tautulli  - Test Tautulli connection
```

## Development

### Project Structure

```
plex-auto-prune-gui/
├── daemon.py              # Core monitoring daemon (copy of main.py)
├── web.py                 # Flask web server + API
├── main.py                # Combined launcher
├── templates/             # HTML templates
│   ├── base.html          # Base template with theme
│   ├── setup.html         # Setup wizard
│   ├── dashboard.html     # Main dashboard
│   ├── users.html         # User management
│   ├── settings.html      # Configuration
│   └── logs.html          # Log viewer
├── static/                # CSS, JS, images (if any)
├── Dockerfile             # Docker build
├── docker-compose.yml     # Docker Compose configuration
└── requirements.txt       # Python dependencies
```

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run combined app
python main.py
```

## Troubleshooting

### Setup Wizard Won't Complete
- Check Docker logs: `docker logs plex-auto-prune-gui`
- Verify all required fields are filled
- Test each connection in the wizard

### Users Not Being Detected
- Verify Tautulli connection
- Check Plex token is valid
- Ensure daemon is running (check logs)

### Emails Not Sending
- Use Gmail App Password (not regular password)
- Enable 2FA on Google account first
- Test email in Settings page

### Discord Not Working
- Verify webhook URL is correct
- Check webhook permissions in Discord

## Comparison: Web vs Daemon-Only

| Feature | Daemon Only | Plex-Auto-Prune GUI |
|---------|-------------|--------------|
| User monitoring | ✅ | ✅ |
| Auto-removal | ✅ | ✅ |
| Email notifications | ✅ | ✅ |
| **Web dashboard** | ❌ | ✅ |
| **Setup wizard** | ❌ | ✅ |
| **Manual actions** | ❌ | ✅ |
| **Live logs** | ❌ | ✅ |
| **Test tools** | ❌ | ✅ |
| Configuration | .env file | Web UI |

## Support

For issues specific to the web interface:
1. Check browser console for JavaScript errors
2. Check Docker logs for API errors
3. Verify port 8080 is accessible
4. Ensure state directory is writable

## Credits

Built with:
- Flask - Web framework
- Flask-SocketIO - Real-time updates
- PlexAPI - Plex integration
- Centauri Design - Terminal-themed UI

## License

Same as the Plex-Auto-Prune daemon project.
