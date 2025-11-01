# 🚀 Quick Setup Guide

This guide will help you set up Plex-Auto-Prune GUI in **under 10 minutes**.

> [!WARNING]
> **Remember:** This is BETA software. Always start with `DRY_RUN=true` for testing!

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ **Docker** installed and running
- ✅ **Plex Media Server** running and accessible
- ✅ **Tautulli** installed and configured with Plex
- ✅ **Email account** (Gmail recommended for easy setup)
- ⏱️ **10 minutes** of your time

---

## 🎯 Step-by-Step Setup

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/InfamousMorningstar/plex-autoprune-GUI.git
cd plex-autoprune-GUI
```

### **Step 2: Create Your Configuration File**

Copy the example file to create your own `.env`:

**Linux/Mac:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

### **Step 3: Get Your Plex Token**

1. Open Plex Web (https://app.plex.tv)
2. Play any movie/show
3. Click the **ⓘ** icon (Get Info)
4. Click **"View XML"** at the bottom
5. Look at the URL - your token is after `X-Plex-Token=`

**Example URL:**
```
https://app.plex.tv/.../file.xml?X-Plex-Token=AbCdEf123456789
                                              └─ This is your token
```

📋 **Copy your token** - you'll need it in Step 6!

> 💡 **Alternative Method:** [Official Plex Guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

### **Step 4: Get Your Tautulli API Key**

1. Open Tautulli web interface
2. Go to **Settings** (⚙️ icon)
3. Click **Web Interface** tab
4. Find **"API Key"** section
5. Click **"Show"** to reveal your key

📋 **Copy your API key** - you'll need it in Step 6!

### **Step 5: Get Gmail App Password** (if using Gmail)

> ⚠️ **Important:** Regular Gmail passwords won't work with SMTP. You MUST create an App Password.

1. Go to your [Google Account](https://myaccount.google.com/)
2. Click **Security** (left sidebar)
3. Enable **2-Step Verification** (if not already enabled)
4. Search for **"App passwords"** and click it
5. Create new app password:
   - App: **Mail**
   - Device: **Other** (type "Plex Auto Prune")
6. Click **Generate**
7. **Copy the 16-character password** shown

📋 **Save this password** - you can't see it again!

> 💡 **Full Guide:** [Google App Passwords Help](https://support.google.com/accounts/answer/185833)

### **Step 6: Edit Your .env File**

Open `.env` in your favorite text editor and fill in your values:

```bash
# Minimum required configuration:

PLEX_TOKEN=paste_your_plex_token_here
PLEX_SERVER_NAME=YourServerName

TAUTULLI_URL=http://192.168.1.100:8181  # Your Tautulli URL
TAUTULLI_API_KEY=paste_your_tautulli_api_key_here

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=paste_your_app_password_here
SMTP_FROM=Your Plex Server <your_email@gmail.com>
ADMIN_EMAIL=your_email@gmail.com

# IMPORTANT: Keep this true for testing!
DRY_RUN=true
```

> 💡 **Tip:** The `.env.example` file has detailed comments explaining each setting.

#### **Optional Settings:**

```bash
# Discord notifications (optional)
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
LINK_DISCORD=https://discord.gg/your_invite

# VIP users who won't be auto-removed (comma-separated)
VIP_NAMES=FriendName,FamilyMember,TrustedUser

# Customize thresholds
WARN_DAYS=27  # Days before warning
KICK_DAYS=30  # Days before removal
```

### **Step 7: Validate Your Configuration** (Optional but Recommended)

Before starting, you can validate your `.env` file:

```bash
python3 validate_config.py
```

This will check:
- ✅ All required fields are filled in
- ✅ No placeholder values remain
- ✅ Email formats are valid
- ✅ SMTP port is correct
- ✅ DRY_RUN is enabled for safety

Fix any errors reported before proceeding!

### **Step 8: Start the Application**

```bash
docker-compose up -d
```

This will:
- ✅ Build the Docker image
- ✅ Start the container
- ✅ Launch the web UI on port 8080

### **Step 9: Access the Web Interface**

Open your browser and go to:
```
http://localhost:8080
```

Or if accessing from another computer:
```
http://your-server-ip:8080
```

🎉 **You should see the Plex-Auto-Prune GUI dashboard!**

---

## ✅ Verification Checklist

After setup, verify everything is working:

### **1. Check Container is Running**

```bash
docker ps | grep plex-auto-prune-gui
```

You should see a running container.

### **2. Check Logs**

```bash
docker logs plex-auto-prune-gui --tail 50
```

Look for:
- ✅ `[LAUNCHER] Starting Plex-Auto-Prune GUI daemon...`
- ✅ `[LAUNCHER] Web interface starting on port 8080...`
- ✅ `[join] loop thread started`
- ❌ No error messages or tracebacks

### **3. Test Plex Connection**

In the web UI:
1. Go to **Dashboard**
2. Check that users are being detected
3. Verify your VIP users show the VIP badge

### **4. Test Email (Optional but Recommended)**

In the web UI:
1. Go to **Settings**
2. Find a test user
3. Click **"Send Test Email"**
4. Check your inbox

### **5. Monitor in DRY_RUN Mode**

> ⚠️ **CRITICAL:** Leave `DRY_RUN=true` for at least 1-2 weeks!

Watch the logs to verify:
- ✅ Users are being detected correctly
- ✅ VIP users are being protected
- ✅ Inactivity tracking is accurate
- ✅ No unexpected behavior

Check logs regularly:
```bash
docker logs plex-auto-prune-gui -f  # Follow mode - Ctrl+C to exit
```

---

## 🎮 Going Live (After Testing)

**Only after 1-2 weeks of successful testing in DRY_RUN mode:**

1. Edit `.env` and change:
   ```bash
   DRY_RUN=false
   ```

2. Restart the container:
   ```bash
   docker-compose restart
   ```

3. **Monitor closely** for the first few days!

---

## 🔧 Troubleshooting

### **Problem: Container won't start**

```bash
# Check logs for errors
docker logs plex-auto-prune-gui

# Common issues:
# - Missing required env vars (PLEX_TOKEN, TAUTULLI_URL, etc.)
# - Invalid credentials
# - Port 8080 already in use
```

**Solution:** Check your `.env` file for typos or missing values.

### **Problem: Web UI not accessible**

```bash
# Check if container is running
docker ps

# Check which ports are exposed
docker port plex-auto-prune-gui
```

**Solutions:**
- Verify port 8080 isn't blocked by firewall
- Try accessing via `http://127.0.0.1:8080`
- Check Docker networking: `docker network ls`

### **Problem: Can't connect to Plex**

**Solutions:**
- Verify PLEX_TOKEN is correct (try getting a new one)
- Check PLEX_SERVER_NAME matches exactly (case-sensitive!)
- Ensure Plex server is running and accessible

### **Problem: Can't connect to Tautulli**

**Solutions:**
- Verify TAUTULLI_URL is correct (include `http://`)
- Test URL in browser: `http://your-tautulli-url:8181`
- Check TAUTULLI_API_KEY is correct

### **Problem: Emails not sending**

**Gmail Users:**
- ✅ Using App Password (NOT regular password)?
- ✅ 2FA enabled on Google account?
- ✅ App Password is 16 characters without spaces?

**All Users:**
- ✅ SMTP_HOST correct? (`smtp.gmail.com` for Gmail)
- ✅ SMTP_PORT correct? (587 for TLS, 465 for SSL)
- ✅ SMTP_USERNAME is your full email?

### **Problem: Users not being detected**

**Solutions:**
- Check Tautulli is tracking Plex activity
- Verify users have watched something recently
- Check logs: `docker logs plex-auto-prune-gui -f`
- Try restarting: `docker-compose restart`

---

## 📊 Understanding the Dashboard

### **Dashboard Sections:**

- **📈 Statistics**: Total users, active, warned, VIP count
- **👥 User List**: All Plex users with activity status
- **⚠️ Warnings**: Users approaching inactivity threshold
- **🔄 Recent Activity**: Latest daemon actions

### **User Status Badges:**

- 🟢 **Active**: Watched content recently
- 🟡 **Warning**: Inactive for WARN_DAYS (default: 27)
- 🔴 **Inactive**: Inactive for KICK_DAYS (default: 30)
- 👑 **VIP**: Protected from auto-removal
- 🆕 **New**: Recently joined

---

## 🎯 Next Steps

After successful setup:

1. ✅ **Monitor logs daily** while in DRY_RUN mode
2. ✅ **Join the community** (if you have Discord setup)
3. ✅ **Star the repo** on GitHub if you find it useful! ⭐
4. ✅ **Report bugs** if you find any issues
5. ✅ **Share feedback** to help improve the project

---

## 📚 Additional Resources

- **README.md**: Full feature list and documentation
- **TRUENAS.md**: TrueNAS SCALE deployment guide
- **.env.example**: Detailed configuration reference
- **GitHub Issues**: Bug reports and feature requests

---

## ⚠️ Important Reminders

> [!CAUTION]
> - This is **BETA software** - expect bugs!
> - **Always test with DRY_RUN=true** first
> - **Monitor logs carefully** before going live
> - **Back up your VIP_NAMES** list
> - **Test email notifications** before relying on them
> - Report bugs on GitHub: [Issues](https://github.com/InfamousMorningstar/plex-autoprune-GUI/issues)

---

## 🎉 You're All Set!

If you followed all steps, you should have:
- ✅ Plex-Auto-Prune GUI running
- ✅ Web UI accessible at http://localhost:8080
- ✅ Monitoring daemon checking users
- ✅ DRY_RUN mode enabled for safe testing

**Need help?** Open an issue on GitHub with:
- Your logs (docker logs command output)
- Your .env file (with secrets removed!)
- Description of the problem

Happy monitoring! 🎬
