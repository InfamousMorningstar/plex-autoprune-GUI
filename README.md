# 🎬 Plex Auto-Prune# Plex-Auto-Prune GUI - Plex User Management



**Automatically manage your Plex server users based on watch activity.**  > [!WARNING]

Beautiful terminal-themed UI. Zero configuration files. One-click deploy.> **⚠️ BETA SOFTWARE - NOT READY FOR PRODUCTION USE ⚠️**

> 

[![Docker Pulls](https://img.shields.io/docker/pulls/infamousmorningstar/plex-auto-prune)](https://hub.docker.com/r/infamousmorningstar/plex-auto-prune)> This application is in **early beta testing phase**. It contains known bugs and incomplete features. 

[![GitHub Stars](https://img.shields.io/github/stars/InfamousMorningstar/plex-autoprune-GUI)](https://github.com/InfamousMorningstar/plex-autoprune-GUI)> 

[![License](https://img.shields.io/github/license/InfamousMorningstar/plex-autoprune-GUI)](LICENSE)> **DO NOT use this in a live production environment without thorough testing in DRY_RUN mode first.**

> 

---> - ❌ Not feature-complete

> - ❌ Contains known bugs

## ✨ Features> - ❌ Some functionality still in planning phase

> - ✅ Testing and feedback welcome

- 🎨 **Beautiful Terminal UI** - Retro comp-sci themed interface> - ✅ Use DRY_RUN=true for safe evaluation

- 🔐 **Plex OAuth Login** - Secure authentication with your Plex account

- 📊 **User Analytics** - Track watch activity and inactivityA sophisticated web interface for automated Plex user management. Plex-Auto-Prune GUI monitors user activity via Tautulli and automatically manages access based on inactivity, with a beautiful terminal-themed web dashboard.

- 📧 **Email Notifications** - Welcome, warning, and removal emails

- 🎯 **Auto-Management** - Automatically remove inactive users## Features

- 🛡️ **VIP Protection** - Protect specific users from removal

- 🔔 **Discord Webhooks** - Get notifications in Discord### 🎯 Complete Web Interface

- 💾 **Backup & Restore** - One-click backup/restore- **Setup Wizard** - Easy first-time configuration with connection testing

- 🧪 **Dry Run Mode** - Test everything before going live- **Dashboard** - Real-time statistics and system overview

- 📈 **Real-time Monitoring** - Live logs and health checks- **User Management** - View, filter, and manually manage all users

- **Settings** - Live configuration with validation

---- **Log Viewer** - Real-time log streaming via WebSockets



## 🚀 Quick Start### 🤖 Automated Management

- **New User Welcome** - Automatically welcome new users (configurable with optional delay)

### Option 1: One-Command Install (Recommended)- **Inactivity Warnings** - Warning emails at configurable threshold

- **Auto-Removal** - Remove inactive users after grace period

```bash- **Rejoined Detection** - Re-welcome users who return after removal

curl -sSL https://raw.githubusercontent.com/InfamousMorningstar/plex-autoprune-GUI/master/install.sh | bash- **VIP Protection** - Protect friends/family from auto-removal

```

### 🎨 Beautiful UI

That's it! Open your browser to `http://localhost:5000` and login with Plex.- **Terminal Theme** - Centauri-inspired dark mode design

- **Responsive** - Works on desktop, tablet, and mobile

### Option 2: Docker Compose- **Real-time Updates** - Live statistics and logs via WebSockets

- **One-Click Actions** - Manual welcome/warn/remove from GUI

```bash

mkdir plex-auto-prune && cd plex-auto-prune### ✉️ Customizable Email Templates

curl -sSL https://raw.githubusercontent.com/InfamousMorningstar/plex-autoprune-GUI/master/docker-compose.yml -o docker-compose.yml- **Default Templates** - Professional, terminal-themed email designs included

docker-compose up -d- **Custom HTML** - Replace with your own email templates

```- **Variable Branding** - Customize colors, server name, and footer links

- **Easy to Use** - Drop HTML files in `email_templates/` directory

### Option 3: Docker Run- **Automatic Attribution** - Designer credit footer automatically added



```bash## Quick Start (Docker)

docker run -d \

  --name plex-auto-prune \> [!TIP]

  -p 5000:5000 \> **� First Time Setup?** Follow the detailed **[SETUP.md Guide](SETUP.md)** for step-by-step instructions!

  -v ./state:/app/state \> 

  -e TZ=America/New_York \> **�📦 TrueNAS SCALE Users?** See **[TRUENAS.md](TRUENAS.md)** for container deployment guide.

  --restart unless-stopped \

  infamousmorningstar/plex-auto-prune:latest### 1. Clone the Repository

```

```bash

### Option 4: Portainer (TrueNAS SCALE)git clone https://github.com/InfamousMorningstar/plex-autoprune-GUI.git

cd plex-autoprune-GUI

1. **Portainer** → **App Templates** → **Custom Templates**```

2. **Add template URL**: `https://raw.githubusercontent.com/InfamousMorningstar/plex-autoprune-GUI/master/portainer-template.json`

3. **Deploy** → **Plex Auto-Prune**### 2. Configure Environment

4. Done!

Copy the example configuration and edit with your values:

---

```bash

## 📖 First-Time Setup# Linux/Mac

cp .env.example .env

1. **Open the web UI** at `http://localhost:5000`

2. **Login with Plex** - One click OAuth authentication# Windows PowerShell

3. **Complete the setup wizard**:Copy-Item .env.example .env

   - ✅ Plex credentials (auto-filled from login)```

   - 📊 Tautulli API connection

   - 📧 Email SMTP settings**Edit `.env` with your credentials:**

   - 🔔 Discord webhook (optional)- 🔑 Plex Token ([How to find](https://support.plex.tv/articles/204059436))

   - ⚙️ Inactivity thresholds- 🔑 Tautulli API Key (Tautulli Settings → Web Interface)

- 📧 Email SMTP settings ([Gmail App Password](https://support.google.com/accounts/answer/185833))

**Setup takes 2 minutes. All configuration is done through the web UI.**- 👥 VIP usernames (comma-separated)

- ⚠️ Keep `DRY_RUN=true` for testing!

---

> 💡 See **[SETUP.md](SETUP.md)** for detailed configuration help

## 🎯 How It Works

### 3. Start the Application

1. **Monitor** - Checks Tautulli for user watch activity

2. **Warn** - Sends email warning when user is approaching inactivity threshold> [!CAUTION]

3. **Remove** - Automatically removes inactive users (with email notification)> **Always start with DRY_RUN=true to test without making real changes!**

4. **Welcome** - Welcomes new users with customizable emails

```bash

### Inactivity Thresholdsdocker-compose up -d

```

- **Warning** - Default: 27 days inactive

- **Removal** - Default: 30 days inactive### 4. Access Web Interface

- **Check Frequency** - Every 30 minutes

Open your browser to: **http://localhost:8080**

All configurable through the web UI.

You'll see the dashboard with:

---- Real-time user monitoring

- Activity statistics  

## 🛡️ Safety Features- VIP user protection

- Automated warning/removal logs

- **Dry Run Mode** - Test everything without making changes (enabled by default)

- **VIP Protection** - Protect admin and VIP users from auto-removal### 5. Test Thoroughly Before Going Live

- **Manual Controls** - Daemon starts disabled, you control when it runs

- **Backup/Restore** - One-click state backup> [!IMPORTANT]

- **Health Monitoring** - Dashboard shows service health> **BETA TESTING CHECKLIST:**

> 

---> - ✅ Keep `DRY_RUN=true` for at least 1-2 weeks

> - ✅ Monitor logs daily for errors or unexpected behavior

## 📸 Screenshots> - ✅ Verify VIP users are properly protected

> - ✅ Test email notifications are working correctly

### Dashboard> - ✅ Check that user detection is accurate

![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)> - ✅ Review all automated actions in logs before enabling live mode

> - ⚠️ Report any bugs or issues on GitHub

### User Management> 

![Users](https://via.placeholder.com/800x400?text=Users+Page+Screenshot)> **Only set DRY_RUN=false after extensive testing and validation!**



### Setup WizardOnce setup is complete, Plex-Auto-Prune GUI will:

![Setup](https://via.placeholder.com/800x400?text=Setup+Wizard+Screenshot)- Run the monitoring daemon in the background

- Provide a web dashboard at port 8080

---- Log all actions (but not execute them in DRY_RUN mode)



## 🔧 Configuration## Configuration



### Environment Variables (Optional)All configuration is done through the web interface during setup, or via the Settings page.



All configuration can be done through the web UI. These are optional overrides:### Required Settings



| Variable | Description | Default || Setting | Description |

|----------|-------------|---------||---------|-------------|

| `TZ` | Timezone | `America/New_York` || **PLEX_TOKEN** | Your Plex authentication token |

| `WARN_DAYS` | Days before warning | `27` || **TAUTULLI_URL** | Full URL to your Tautulli instance |

| `KICK_DAYS` | Days before removal | `30` || **TAUTULLI_API_KEY** | Tautulli API key |

| `DRY_RUN` | Enable dry run mode | `true` || **SMTP Settings** | Gmail SMTP configuration |

| **ADMIN_EMAIL** | Where to send admin notifications |

### Custom Email Templates

### Optional Settings

Drop HTML files in `email_templates/` directory:

| Setting | Default | Description |

- `welcome.html` - New user welcome email|---------|---------|-------------|

- `warning.html` - Inactivity warning email| **WARN_DAYS** | 27 | Days before warning email |

- `removal.html` - Removal notification email| **KICK_DAYS** | 30 | Days before removal |

| **AUTO_WELCOME_NEW_USERS** | true | Automatically send welcome emails to new users |

See `email_templates/README.md` for template documentation.| **AUTO_WELCOME_DELAY_HOURS** | 0 | Delay (in hours) before sending welcome email |

| **VIP_NAMES** | - | Comma-separated usernames to protect |

---| **DISCORD_WEBHOOK** | - | Discord webhook URL for notifications |

| **DRY_RUN** | true | Test mode (no actual removals) |

## 📊 API Endpoints

## Docker Deployment

The app exposes REST API endpoints:

### TrueNAS Scale / Portainer

- `GET /api/users` - List all users

- `GET /api/stats` - Get statisticsSee **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide including:

- `POST /api/daemon/start` - Start daemon- Portainer stack configuration

- `POST /api/daemon/stop` - Stop daemon- Volume setup and permissions

- `GET /api/backup` - Download backup- Environment variable configuration

- `POST /api/restore` - Restore from backup- Security recommendations

- Troubleshooting common issues

---- Backup and update procedures



## 🐛 Troubleshooting**Quick Deploy:**



### Container won't start1. Create persistent volume for state:

```bash  ```bash

docker-compose logs -f  mkdir -p /mnt/app-pool/plex-auto-prune-gui/state

```  ```



### Health check failing2. Deploy stack using `docker-compose.yml`

```bash

curl http://localhost:5000/health3. Access at `http://your-server-ip:8080`

```

### Environment Variables

### Reset everything

```bashYou can pre-configure via environment variables or use the web setup wizard:

docker-compose down

rm -rf state/```yaml

docker-compose up -denvironment:

```  PLEX_TOKEN: your_token

  TAUTULLI_URL: http://192.168.1.100:8181

### View daemon logs  TAUTULLI_API_KEY: your_key

Check the **Logs** page in the web UI for real-time daemon activity.  # ... etc

```

---

## Web Interface Pages

## 🤝 Contributing

### Dashboard

Contributions are welcome! Please:- Total users, active, warned, removed counts

- System status (daemon, dry run mode)

1. Fork the repository- Recent activity timeline

2. Create a feature branch- Quick stats at a glance

3. Submit a pull request

### Users

---- Sortable table of all Plex users

- Status badges (Active, Warned, At Risk, Removed)

## 📜 License- Last activity and days inactive

- One-click actions:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  - Send welcome email

  - Send warning

---  - Remove user

  - Reset state

## ⚠️ Disclaimer  - Add/remove from VIP list



This software automatically removes users from your Plex server. **Use at your own risk.**### Settings

- Live configuration editor

- Always start with **DRY_RUN=true**- Test connections (Plex, Tautulli, Email, Discord)

- Test thoroughly before enabling automatic removals- Adjust thresholds

- Keep backups of your user data- Manage VIP list

- Review logs regularly- Toggle dry run mode



---### Logs

- Real-time log streaming

## 🙏 Credits- Filter by level (INFO, SUCCESS, WARNING, ERROR)

- Search logs

Built with ❤️ by [InfamousMorningstar](https://github.com/InfamousMorningstar)- Auto-scroll



Powered by:## Email Templates

- [Plex](https://www.plex.tv/)

- [Tautulli](https://tautulli.com/)Plex-Auto-Prune GUI sends beautiful HTML emails with a terminal aesthetic:

- [Flask](https://flask.palletsprojects.com/)- **Welcome** - Sent to new users

- [Docker](https://www.docker.com/)- **Warning** - Inactivity warning before removal

- **Removal** - Sent when user is removed

---- **Admin Notifications** - Detailed alerts for admins



## 📞 Support## API Endpoints



- 🐛 [Report a bug](https://github.com/InfamousMorningstar/plex-autoprune-GUI/issues)The web interface exposes a REST API:

- 💬 [Discussions](https://github.com/InfamousMorningstar/plex-autoprune-GUI/discussions)

- ⭐ [Star this repo](https://github.com/InfamousMorningstar/plex-autoprune-GUI)```

GET  /api/stats          - Dashboard statistics

---GET  /api/users          - List all users with status

GET  /api/config         - Current configuration

<div align="center">POST /api/config         - Update configuration

  <strong>Made with 💜 for the Plex community</strong>POST /api/users/:id/welcome  - Send welcome email

</div>POST /api/users/:id/warn     - Send warning

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

## Auto-Welcome Configuration

By default, the application **automatically sends welcome emails** to new Plex users as soon as they're detected. You can customize this behavior:

### Disable Auto-Welcome

To manually welcome users from the web interface instead:

```bash
AUTO_WELCOME_NEW_USERS=false
```

With this setting, new users will appear in the Users page but won't receive welcome emails until you click the "✉ Welcome" button.

### Add Welcome Delay

To give users time to set up their account before receiving the welcome email:

```bash
AUTO_WELCOME_NEW_USERS=true
AUTO_WELCOME_DELAY_HOURS=24
```

This will wait 24 hours after a user joins before sending the welcome email. Useful for:
- Letting users complete their profile first
- Avoiding overwhelming new users immediately
- Giving yourself time to verify the user before they get welcomed

**Note:** The daemon checks every `CHECK_NEW_USERS_SECS` (default 2 minutes), so delays are approximate.

## Customizing Email Templates

Want to personalize the emails sent to your users? You have two options:

### Option 1: Use Environment Variables (Simple Customization)

Customize colors, server name, and footer links without touching HTML. Add these to your `.env` file:

```bash
# Server branding
SERVER_NAME=My Awesome Plex Server
BRAND_COLOR=#e5a00d              # Primary color (hex)
BRAND_ACCENT_WARN=#ff9800        # Warning color
BRAND_ACCENT_DANGER=#f44336      # Removal color

# Footer links (optional - leave blank to hide)
LINK_OVERSEERR=https://requests.yourdomain.com
LINK_PORTFOLIO=https://yourwebsite.com
LINK_DISCORD=https://discord.gg/your_invite
```

### Option 2: Custom HTML Templates (Full Control)

Replace the entire email design with your own HTML templates:

1. **Create your template** in the `email_templates/` directory:
   - `welcome.html` - New user welcome email
   - `warning.html` - Inactivity warning email
   - `removal.html` - Account removal notice

2. **Use placeholders** in your HTML:
   ```html
   <h1>Welcome, {display_name}!</h1>
   <p>You've been inactive for {days} days.</p>
   <p>You have {days_left} days remaining.</p>
   ```

3. **Restart the container** to apply changes:
   ```bash
   docker-compose restart
   ```

**📖 See `email_templates/README.md` for detailed examples and best practices.**

**⚖️ Attribution:** All emails automatically include a small designer credit footer. This helps support the project and is appreciated!

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

## Known Issues & Limitations

> [!WARNING]
> **BETA SOFTWARE - Known Issues:**
> 
> - 🐛 Some edge cases in user detection not fully tested
> - 🐛 Email template customization not yet implemented
> - 🐛 Multi-server support incomplete
> - 🐛 Performance with 100+ users not validated
> - 🐛 Some error handling needs improvement
> - 📋 Advanced analytics dashboard (planned)
> - 📋 Mobile app (planned)
> - 📋 Multi-channel notifications (planned)
> 
> **Please report bugs on GitHub Issues!**

## Support

> [!NOTE]
> This is beta software. Support is best-effort only.

For issues specific to the web interface:
1. Check browser console for JavaScript errors
2. Check Docker logs for API errors
3. Verify port 8080 is accessible
4. Ensure state directory is writable
5. **Report bugs**: https://github.com/InfamousMorningstar/plex-autoprune-GUI/issues

## Contributing

This project is in active development. Contributions, bug reports, and feature requests are welcome!

- 🐛 **Bug Reports**: Use GitHub Issues
- 💡 **Feature Requests**: Use GitHub Discussions
- 🔧 **Pull Requests**: Always welcome (target `develop` branch)
- 📖 **Documentation**: Help improve docs and guides

## Credits

Built with:
- Flask - Web framework
- Flask-SocketIO - Real-time updates
- PlexAPI - Plex integration
- Centauri Design - Terminal-themed UI

## License

Same as the Plex-Auto-Prune daemon project.

---

> [!CAUTION]
> **Final Reminder: This is BETA software!**
> 
> - Always use DRY_RUN=true for testing
> - Monitor logs carefully
> - Report bugs and issues
> - Do NOT deploy to production without extensive testing
> - Author assumes no responsibility for data loss or unintended user removals
