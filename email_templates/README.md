# Custom Email Templates

This directory allows you to customize the email notifications sent to your Plex users.

## 📧 Available Templates

You can customize any or all of these email types:

- **`welcome.html`** - Sent when a new user joins your Plex server
- **`warning.html`** - Sent when a user is approaching the inactivity threshold
- **`removal.html`** - Sent when a user is removed for inactivity

## 🎨 How to Use Custom Templates

1. **Create your template file** in this directory (e.g., `welcome.html`)
2. **Use placeholders** that will be automatically replaced:
   - `{display_name}` - The user's name
   - `{days}` - Days inactive (warning email only)
   - `{days_left}` - Days until removal (warning email only)
3. **Restart the container** to apply changes

## ✨ Template Rules

- **HTML Format**: Templates must be valid HTML
- **Attribution Required**: The designer attribution footer will be automatically added to all emails
- **Placeholders**: Use curly braces `{placeholder_name}` for dynamic content
- **Encoding**: Use UTF-8 encoding for your template files

## 📝 Example: Simple Welcome Template

Create `welcome.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Welcome to My Plex Server</title>
</head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
  <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
    <h1 style="color: #e5a00d;">Welcome, {display_name}!</h1>
    <p>Thanks for joining my Plex server. Here are the house rules:</p>
    <ul>
      <li>Use official Plex apps for best experience</li>
      <li>Watch at least once every 30 days to keep your access</li>
      <li>Request content through Overseerr</li>
    </ul>
    <p>Happy streaming!</p>
  </div>
</body>
</html>
```

## 🎯 Example: Warning Email Template

Create `warning.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Inactivity Warning</title>
</head>
<body style="font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5;">
  <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
    <h1 style="color: #ff9800;">Hey {display_name}, We Miss You!</h1>
    <p>You haven't watched anything in <strong>{days} days</strong>.</p>
    <p>You have <strong>{days_left} days</strong> left before your access is automatically removed.</p>
    <p>Just watch something to keep your account active!</p>
    <a href="https://app.plex.tv" style="display: inline-block; background: #e5a00d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">
      Open Plex
    </a>
  </div>
</body>
</html>
```

## 💡 Tips

- **Test your templates** by triggering a test email through the web UI
- **Keep mobile-friendly** - Many email clients have limited CSS support
- **Use inline styles** - External CSS may not work in email clients
- **Preview in multiple clients** - Gmail, Outlook, and Apple Mail all render differently
- **Backup default templates** - If you want to revert, just delete your custom file

## 🔄 Using Default Templates

To revert to the default templates:
- Simply delete or rename your custom template file (e.g., `welcome.html` → `welcome.html.bak`)
- The system will automatically use the built-in default template

## ⚖️ Attribution

All emails will include a small attribution footer crediting the original template designer (Morningstar). This is automatically added and helps support the project. Thank you for respecting this!

---

**Need help?** Check the main README.md or open an issue on GitHub.
