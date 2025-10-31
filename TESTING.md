# Plex-Auto-Prune GUI - Testing Checklist

Complete this checklist before deploying to production.

## Pre-Deployment Testing

### ✅ Build & Start

- [ ] Docker image builds without errors
  ```bash
  cd plex-auto-prune-gui
  docker-compose build
  ```

- [ ] Container starts successfully
  ```bash
  docker-compose up -d
  docker-compose logs -f
  ```

- [ ] Web interface accessible at http://localhost:8080

### ✅ Setup Wizard

- [ ] Setup wizard loads and displays correctly
- [ ] Step 1: Plex connection test succeeds
- [ ] Step 2: Tautulli connection test succeeds
- [ ] Step 3: Test email sends successfully
- [ ] Step 4: Discord test messages sent (if configured)
- [ ] Step 5: All thresholds and settings saved
- [ ] "Complete Setup" redirects to dashboard

### ✅ Dashboard Page

- [ ] Dashboard loads without errors
- [ ] All stat cards display correct counts:
  - Total Users
  - Active Users
  - Warned Users
  - Removed Users
- [ ] System status shows daemon running
- [ ] Operating mode displays (DRY RUN or LIVE)
- [ ] Recent activity feed shows daemon logs
- [ ] Quick actions buttons work:
  - Manage Users → redirects to /users
  - Settings → redirects to /settings
  - Logs → redirects to /logs
  - Toggle DRY_RUN → shows confirmation, updates config
- [ ] WebSocket connection indicator shows "Connected"
- [ ] Stats auto-refresh every 30 seconds

### ✅ Users Page

- [ ] User table loads all Plex users
- [ ] User count badges show correct totals
- [ ] Search bar filters users by name/email/username
- [ ] Status filter dropdown works (all, active, warned, removed, new)
- [ ] Table sorting works (click column headers)
- [ ] Status badges display correctly with colors
- [ ] VIP indicators show for protected users
- [ ] Action buttons work (in DRY_RUN mode, check logs):
  - Welcome → sends welcome email
  - Warn → sends warning email
  - Remove → removes user + sends email
  - Reset → clears user state
  - VIP toggle → adds/removes from VIP list
- [ ] Confirmation modals appear for destructive actions
- [ ] Export CSV downloads user list correctly
- [ ] Refresh button reloads user data

### ✅ Settings Page

- [ ] All configuration fields populated from .env
- [ ] Sensitive fields masked (show last 4 chars)
- [ ] Test connection buttons work:
  - Test Plex → shows success with username and user count
  - Test Tautulli → shows success with user count
  - Test Email → sends email to admin address
  - Test Discord → sends test messages to webhook
- [ ] Form validation prevents invalid values
- [ ] Save Configuration button:
  - Saves all changes to .env
  - Shows success message
  - Reloads page to apply changes
- [ ] Cancel button reloads without saving
- [ ] DRY_RUN toggle checkbox works

### ✅ Logs Page

- [ ] Log viewer loads initial logs
- [ ] Real-time logs stream via WebSocket
- [ ] Filter buttons work (ALL, INFO, SUCCESS, WARNING, ERROR)
- [ ] Search box filters logs by text
- [ ] Auto-scroll checkbox controls scrolling behavior
- [ ] Log level badges display with correct colors
- [ ] Timestamps formatted correctly
- [ ] Export button downloads logs as .txt file
- [ ] Clear button clears all logs (with confirmation)
- [ ] Stats counters update in real-time

### ✅ Daemon Functionality

- [ ] Daemon starts automatically with web server
- [ ] New user detection works:
  - Add a new Plex user
  - Wait 120 seconds
  - Check logs for "new user detected"
  - Welcome email sent (if not in DRY_RUN)
- [ ] Rejoined user detection works:
  - User in "removed" state joins again
  - Gets moved to "welcomed" with new welcome email
- [ ] Inactivity checking works:
  - Check logs for periodic inactivity checks
  - Users past WARN_DAYS get warning email
  - Users past KICK_DAYS get removed (if not in DRY_RUN)
- [ ] VIP protection works:
  - Add user to VIP list
  - Verify they're never warned or removed
- [ ] State persistence:
  - Check /app/state/state.json updates
  - Restart container, verify state loaded

### ✅ WebSocket Real-Time Updates

- [ ] Dashboard stats update without page refresh
- [ ] New logs appear in Logs page instantly
- [ ] User status changes reflect immediately
- [ ] Connection indicator shows status

### ✅ Error Handling

- [ ] Invalid Plex token shows error message
- [ ] Unreachable Tautulli URL shows error
- [ ] Invalid email credentials show error
- [ ] Broken Discord webhook shows error
- [ ] Network errors display user-friendly messages
- [ ] 404 pages redirect to dashboard

## Production Readiness

### ✅ Security

- [ ] Change DRY_RUN to `false` only after testing
- [ ] Use strong Gmail app password
- [ ] Restrict port 8080 to local network
- [ ] Consider HTTPS reverse proxy for external access
- [ ] Review VIP protection list

### ✅ Monitoring

- [ ] Dashboard accessible
- [ ] Logs streaming properly
- [ ] Email notifications working
- [ ] Discord notifications working (if enabled)
- [ ] No errors in container logs

### ✅ Backup

- [ ] State file backed up: `/app/state/state.json`
- [ ] Configuration documented
- [ ] Test restore from backup

## DRY_RUN Testing

**CRITICAL**: Keep DRY_RUN enabled while testing!

### What DRY_RUN Does:
- ✅ Logs all actions (welcome, warn, remove)
- ✅ Detects all users and inactivity
- ✅ Updates state file
- ❌ Does NOT send emails
- ❌ Does NOT remove users from Plex

### Testing in DRY_RUN:
1. Enable DRY_RUN in Settings
2. Perform all actions (welcome, warn, remove)
3. Check Logs page for "DRY_RUN" messages
4. Verify no actual emails sent
5. Verify no users actually removed from Plex

### Going Live:
1. Verify all tests pass in DRY_RUN mode
2. Monitor logs for 24 hours in DRY_RUN
3. Disable DRY_RUN in Settings page
4. Monitor closely for first few days
5. Check email inbox for notifications
6. Review Users page daily

## Common Issues

### Container Won't Start
```bash
docker-compose logs -f
# Check for:
# - Missing environment variables
# - Invalid Plex token
# - Port 8080 already in use
```

### Users Not Detected
- Verify Plex token is valid
- Check Tautulli URL is accessible
- Ensure network_mode: host is set
- Review daemon logs in Logs page

### Emails Not Sending
- Use Gmail app password (not regular password)
- Check SMTP settings match Gmail
- Test via Settings page
- Review logs for email errors

### WebSocket Not Connecting
- Check browser console for errors
- Verify port 8080 is accessible
- Check firewall settings
- Try different browser

## Sign-Off

Once all checks pass:

- [ ] All web pages load correctly
- [ ] All API endpoints respond
- [ ] Daemon monitoring active
- [ ] Real-time updates working
- [ ] Configuration persists
- [ ] Ready for production deployment

**Tested by:** _______________  
**Date:** _______________  
**Ready for Production:** ☐ Yes  ☐ No (see notes)

**Notes:**
