# Plex-Auto-Prune GUI - Deployment Guide

This guide covers deploying the Plex-Auto-Prune GUI web application to TrueNAS Scale using Portainer.

## Prerequisites

- TrueNAS Scale installed and running
- Portainer installed on TrueNAS
- Plex Media Server running
- Tautulli installed and configured
- Gmail account with app password (for email notifications)
- Discord webhook (optional)

## Option 1: Portainer Stack Deployment (Recommended)

### Step 1: Create Storage Location

1. Log into TrueNAS
2. Create a dataset for Plex-Auto-Prune GUI:
   - Navigate to **Storage** → **Pools**
   - Select your pool (e.g., `app-pool`)
   - Click **Add Dataset**
  - Name: `plex-auto-prune-gui`
   - Click **Save**

3. Create the state directory:
  ```bash
  mkdir -p /mnt/app-pool/plex-auto-prune-gui/state
  chmod 777 /mnt/app-pool/plex-auto-prune-gui/state
  ```

### Step 2: Create Portainer Stack

1. Open Portainer web interface
2. Navigate to **Stacks** → **Add Stack**
3. Name: `plex-auto-prune-gui`
4. Web editor: Paste the following stack configuration:

```yaml
version: '3.8'

services:
  plex-auto-prune-gui:
    image: ghcr.io/infamousmorningstar/plex-auto-prune-gui:latest  # Replace with your image
    container_name: plex-auto-prune-gui
    network_mode: host
    restart: unless-stopped
    
    environment:
      # Plex Configuration
      PLEX_TOKEN: ${PLEX_TOKEN}
      PLEX_SERVER_NAME: ${PLEX_SERVER_NAME:-My Plex Server}
      
      # Tautulli Configuration
      # Email Configuration
      SMTP_HOST: ${SMTP_HOST:-smtp.gmail.com}
      SMTP_PORT: ${SMTP_PORT:-587}
      SMTP_USERNAME: ${SMTP_USERNAME}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
      SMTP_FROM: ${SMTP_FROM}
      ADMIN_EMAIL: ${ADMIN_EMAIL}
      
      # Discord (Optional)
      DISCORD_WEBHOOK: ${DISCORD_WEBHOOK:-}
      LINK_DISCORD: ${LINK_DISCORD:-}
      
      # Thresholds
      WARN_DAYS: ${WARN_DAYS:-27}
      KICK_DAYS: ${KICK_DAYS:-30}
      
      # Check Intervals (seconds)
      CHECK_NEW_USERS_SECS: ${CHECK_NEW_USERS_SECS:-120}
      CHECK_INACTIVITY_SECS: ${CHECK_INACTIVITY_SECS:-1800}
      
      # VIP Protection
      VIP_NAMES: ${VIP_NAMES:-}
      
      # Operating Mode
      DRY_RUN: ${DRY_RUN:-true}
    
    volumes:
      - /mnt/app-pool/plex-auto-prune-gui/state:/app/state
    
    ports:
      - "8080:8080"
```

5. Click **Deploy the stack**

### Step 3: Configure Environment Variables

2. Click **Editor** tab
3. Scroll down to **Environment variables**
4. Click **Add environment variable** for each required variable:
- `PLEX_TOKEN`: Your Plex authentication token
  - Get from: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
  
  - Get from: Tautulli → Settings → Web Interface → API Key
  
- `SMTP_USERNAME`: Your Gmail address
  
- `ADMIN_EMAIL`: Where to send admin notifications
  
- `SMTP_FROM`: Display name for emails (e.g., `"Plex Admin" <you@gmail.com>`)

#### Optional Variables:

- `DISCORD_WEBHOOK`: Discord webhook URL for notifications
- `LINK_DISCORD`: Your Discord profile URL
- `VIP_NAMES`: Comma-separated list of protected usernames
- `DRY_RUN`: Set to `false` when ready for live operation (default: `true`)

5. Click **Update the stack**

### Step 4: Initial Setup

1. Access the web interface at `http://your-truenas-ip:8080`
2. You'll be redirected to the setup wizard
3. Complete all 5 steps:
   - **Step 1**: Plex configuration (test connection)
   - **Step 2**: Tautulli configuration (test connection)
   - **Step 3**: Email configuration (send test email)
   - **Step 4**: Discord integration (optional, test webhook)
   - **Step 5**: Thresholds, VIP list, intervals, DRY_RUN mode
4. Click **Complete Setup**
5. You'll be redirected to the dashboard

## Option 2: Docker Compose Deployment

### Step 1: Clone Repository

```bash
cd /mnt/app-pool
git clone https://github.com/InfamousMorningstar/Plex-Auto-Prune.git
cd Plex-Auto-Prune/guardian-web
```

### Step 2: Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
nano .env
```

Fill in all required values (same as Portainer environment variables above).

### Step 3: Build and Run

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

## Post-Deployment

### Accessing the Interface

Open your browser to: `http://your-truenas-ip:8080`

### Security Recommendations

1. **Use HTTPS**: Set up a reverse proxy (nginx, traefik) with SSL
2. **Add Authentication**: Configure basic auth or OAuth
3. **Firewall**: Restrict access to your local network
4. **Strong Passwords**: Use complex app passwords for email

### Monitoring

- **Dashboard**: Shows real-time stats and system status
- **Logs Page**: View daemon activity in real-time
- **WebSocket**: Live updates without page refresh

### Testing Before Going Live

1. **DRY_RUN Mode**: Keep enabled initially
   - All actions are logged but NOT executed
   - No emails sent, no users removed
   
2. **Verify Detection**:
   - Check Users page to ensure all Plex users are detected
   - Verify activity dates are accurate
   
3. **Test Actions**:
   - Settings → Test all connections (Plex, Tautulli, Email, Discord)
   - Try "Welcome" action on a test user (email sent in DRY_RUN)
   - Check logs to see what would happen
   
4. **Go Live**:
   - When ready, disable DRY_RUN in Settings
   - Save configuration
   - Monitor logs and dashboard closely

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs plex-auto-prune-gui

# Common issues:
# - Invalid Plex token
# - Tautulli URL not reachable
# - Missing required environment variables
```

### Users Not Detected

- Verify Plex token is correct
- Check Tautulli URL is accessible from container
- Ensure network_mode: host is set (for local Tautulli)

### Emails Not Sending

- Gmail requires app password (not regular password)
- Enable "Less secure app access" if using app password
- Check SMTP settings match Gmail requirements

### WebSocket Not Connecting

- Ensure port 8080 is accessible
- Check browser console for connection errors
- Verify firewall allows WebSocket connections

### Configuration Not Persisting

- Environment variables in Portainer override .env file
- Make changes in Settings page or Portainer environment variables
- Changes via Settings page write to .env file in container

## Updating the Application

### Portainer Stack Method

1. Navigate to **Stacks** → **plex-auto-prune-gui**
2. Click **Update the stack**
3. Enable **Re-pull image**
4. Click **Update**

**IMPORTANT**: Environment variables persist across updates!

### Docker Compose Method

docker-compose up --build -d
```bash
cd /mnt/app-pool/Plex-Auto-Prune/guardian-web
git pull
docker-compose down
docker-compose up --build -d
```

## Backup and Restore

### Backup State File

```bash
# Backup
cp /mnt/app-pool/plex-auto-prune-gui/state/state.json ~/plex-auto-prune-backup.json

# Restore
cp ~/plex-auto-prune-backup.json /mnt/app-pool/plex-auto-prune-gui/state/state.json
```

### Export Configuration

1. Open Settings page
2. Copy all values to a secure location
3. Or backup `.env` file from container

## Advanced Configuration

### Custom Check Intervals

Adjust in Settings or environment variables:

- `CHECK_NEW_USERS_SECS`: How often to check for new users (default: 120s)
- `CHECK_INACTIVITY_SECS`: How often to check inactivity (default: 1800s)

### VIP Protection

Protected users are never removed, even with inactivity:

```
VIP_NAMES=friend1,family_member,bestfriend
```

Or manage via Users page → VIP toggle button.

### Thresholds

- `WARN_DAYS`: Days of inactivity before warning (default: 27)
- `KICK_DAYS`: Days of inactivity before removal (default: 30)

## Support

- **GitHub Issues**: https://github.com/InfamousMorningstar/Plex-Auto-Prune/issues
- **Documentation**: See README.md for API reference
- **Logs**: Check Logs page in web interface for debugging

## Network Modes

### Host Mode (Recommended for Local Tautulli)

```yaml
network_mode: host
```

- Container shares host network
- Can access Tautulli on `http://192.168.x.x:8181`
- Web UI accessible on host IP at port 8080

### Bridge Mode (For Remote Tautulli)

```yaml
# Remove network_mode: host
# Add:
ports:
  - "8080:8080"
```

- Container has its own network
- Tautulli must be accessible via hostname/domain
- More isolated but requires proper networking
