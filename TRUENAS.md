# TrueNAS SCALE Deployment Guide

> [!WARNING]
> **⚠️ BETA SOFTWARE - TESTING ONLY ⚠️**
> 
> This application is in **early beta** and should **NOT** be used in production environments.
> 
> - ❌ Not feature-complete
> - ❌ Contains known bugs
> - ❌ Some functionality incomplete
> - ✅ **ALWAYS use DRY_RUN=true for testing**
> - ✅ Monitor logs carefully before going live
> 
> **Use at your own risk. Test thoroughly before enabling live mode!**

## Quick Deployment on TrueNAS SCALE

This guide will help you deploy Plex-Auto-Prune GUI on TrueNAS SCALE using Docker Compose.

### Prerequisites

- TrueNAS SCALE installed and running
- Docker service enabled on TrueNAS
- Network access to your Plex server
- Tautulli installed and accessible

### Installation Steps

#### 1. Create Application Directory

SSH into your TrueNAS server and create a directory for the application:

```bash
mkdir -p /mnt/tank/apps/plex-auto-prune-gui
cd /mnt/tank/apps/plex-auto-prune-gui
```

#### 2. Clone the Repository

```bash
git clone https://github.com/InfamousMorningstar/plex-autoprune-GUI.git .
```

#### 3. Configure Environment Variables

Create a `.env` file with your configuration:

```bash
nano .env
```

Add the following (replace with your actual values):

```env
# Plex Configuration
PLEX_TOKEN=your_plex_token_here
PLEX_SERVER_NAME=YourServerName

# Tautulli Configuration
TAUTULLI_URL=http://your-truenas-ip:8181
TAUTULLI_API_KEY=your_tautulli_api_key

# Email Configuration (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=Your Plex Server <your_email@gmail.com>
ADMIN_EMAIL=admin@example.com

# Discord Configuration (optional)
DISCORD_WEBHOOK=your_discord_webhook_url
LINK_DISCORD=https://discord.gg/your_invite

# VIP Users (comma-separated, case-sensitive)
VIP_NAMES=AdminUser,VIPUser1,VIPUser2

# Monitoring Settings
WARN_DAYS=27
KICK_DAYS=30
CHECK_NEW_USERS_SECS=120
CHECK_INACTIVITY_SECS=1800

# Safety Mode - Set to false for production
DRY_RUN=true
```

**Important Notes:**
- Get your Plex token from: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
- Get Tautulli API key from: Tautulli Settings → Web Interface → API Key
- For Gmail, use an App Password: https://support.google.com/accounts/answer/185833
- Keep `DRY_RUN=true` until you've tested thoroughly

#### 4. Configure Port (Optional)

By default, the web UI runs on port 8080. To change it, edit `docker-compose.yml`:

```yaml
ports:
  - "9090:8080"  # Changes external port to 9090
```

#### 5. Deploy the Container

```bash
docker-compose up -d
```

> [!IMPORTANT]
> **BETA TESTING REQUIRED:**
> 
> After deployment, you MUST:
> - ✅ Verify `DRY_RUN=true` in your .env file
> - ✅ Monitor logs for at least 1-2 weeks: `docker logs plex-auto-prune-gui -f`
> - ✅ Verify VIP users are being protected
> - ✅ Check that user detection is working correctly
> - ✅ Test email notifications manually
> - ⚠️ Report any bugs or unexpected behavior
> 
> **DO NOT set DRY_RUN=false until you've validated everything works as expected!**

#### 6. Access the Web UI

Open your browser and navigate to:
```
http://your-truenas-ip:8080
```

Or if you changed the port:
```
http://your-truenas-ip:9090
```

### Web UI Features

- **Dashboard**: Overview of monitoring status and recent activity
- **Users**: View all Plex users, their activity, and manage them manually
- **Settings**: Configure monitoring parameters, VIP lists, and notification settings
- **Logs**: Real-time log viewing with filtering

### Monitoring Behavior

The daemon runs two monitoring loops:

1. **Join Watcher** (every 120 seconds):
   - Detects new Plex users
   - Sends welcome emails
   - Detects and notifies about rejoined users

2. **Inactivity Watcher** (every 1800 seconds / 30 minutes):
   - Checks last activity for all users
   - Sends warning emails at WARN_DAYS (default: 27 days)
   - Removes inactive users at KICK_DAYS (default: 30 days)
   - VIP users are never removed

### DRY_RUN Mode

When `DRY_RUN=true`:
- All actions are logged but NOT executed
- No users are actually removed
- No emails are actually sent
- Perfect for testing your configuration

Set `DRY_RUN=false` in your `.env` file once you're confident in your setup.

### Useful Commands

```bash
# View logs
docker logs plex-auto-prune-gui -f

# Restart container
docker-compose restart

# Stop container
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Check container status
docker ps | grep plex-auto-prune-gui
```

### Firewall Configuration

If you need to access the web UI from outside your network:
1. TrueNAS UI → System → Services → SSH (if not already enabled)
2. Configure your router/firewall to forward the chosen port
3. Consider using a reverse proxy (nginx, traefik) for HTTPS

### Troubleshooting

**Container won't start:**
```bash
docker logs plex-auto-prune-gui
```

**Web UI not accessible:**
- Check firewall rules on TrueNAS
- Verify port isn't already in use: `netstat -tulpn | grep 8080`
- Check container is running: `docker ps`

**Plex connection issues:**
- Verify PLEX_TOKEN is correct
- Ensure TrueNAS can reach Plex server
- Check Plex server allows local network connections

**Email not sending:**
- Verify SMTP credentials
- For Gmail, ensure "Less secure app access" is enabled OR use App Password
- Check SMTP_PORT (587 for TLS, 465 for SSL)

### Backup & Restore

The application stores its state in the `./state` directory, which includes:
- User tracking database
- Setup completion flag

To backup:
```bash
tar -czf plex-auto-prune-backup.tar.gz state/ .env
```

To restore:
```bash
tar -xzf plex-auto-prune-backup.tar.gz
```

### Updating

To update to the latest version:

```bash
cd /mnt/tank/apps/plex-auto-prune-gui
docker-compose down
git pull
docker-compose up -d --build
```

### Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/InfamousMorningstar/plex-autoprune-GUI/issues
- Check logs first: `docker logs plex-auto-prune-gui --tail 100`

## Security Recommendations

1. **Never expose port 8080 directly to the internet** without HTTPS
2. Use strong passwords for SMTP
3. Keep your `.env` file permissions restrictive: `chmod 600 .env`
4. Regularly review the logs and user activity
5. Start with `DRY_RUN=true` and monitor for at least a week before going live
6. Keep VIP_NAMES list updated with users who should never be removed

## Network Requirements

The container needs access to:
- Plex Server (typically port 32400)
- Tautulli (typically port 8181)
- SMTP server (port 587 or 465)
- Discord (if using webhooks)

Ensure TrueNAS firewall allows these connections.
