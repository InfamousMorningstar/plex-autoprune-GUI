#!/usr/bin/env python3
"""
Plex-Auto-Prune GUI - Environment Configuration Validator
Validates your .env file before deployment
"""
import os
import sys
import re

def print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_success(msg):
    print(f"✅ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def check_env_file_exists():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print_error(".env file not found!")
        print_info("Please copy .env.example to .env and fill in your values:")
        print_info("  Linux/Mac: cp .env.example .env")
        print_info("  Windows:   copy .env.example .env")
        return False
    print_success(".env file found")
    return True

def load_env_file():
    """Load and parse .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        return env_vars
    except Exception as e:
        print_error(f"Failed to read .env file: {e}")
        return None

def validate_required_fields(env_vars):
    """Validate all required fields are present and not placeholder values"""
    required = {
        'PLEX_TOKEN': 'your_plex_token_here',
        'PLEX_SERVER_NAME': 'My Plex Server',
        'TAUTULLI_URL': 'http://localhost:8181',
        'TAUTULLI_API_KEY': 'your_tautulli_api_key_here',
        'SMTP_HOST': None,  # Has default value
        'SMTP_PORT': None,  # Has default value
        'SMTP_USERNAME': 'your_email@gmail.com',
        'SMTP_PASSWORD': 'your_app_password_here',
        'SMTP_FROM': 'your_email@gmail.com',
        'ADMIN_EMAIL': 'admin@example.com',
    }
    
    all_valid = True
    
    for key, placeholder in required.items():
        if key not in env_vars or not env_vars[key]:
            print_error(f"{key} is missing or empty")
            all_valid = False
        elif placeholder and env_vars[key] == placeholder:
            print_error(f"{key} still has placeholder value: {placeholder}")
            all_valid = False
        else:
            print_success(f"{key} is configured")
    
    return all_valid

def validate_plex_token(token):
    """Validate Plex token format"""
    if not token or len(token) < 10:
        print_warning("PLEX_TOKEN seems too short (typical tokens are 20+ characters)")
        return False
    print_success("PLEX_TOKEN length looks valid")
    return True

def validate_tautulli_url(url):
    """Validate Tautulli URL format"""
    if not url.startswith(('http://', 'https://')):
        print_error("TAUTULLI_URL must start with http:// or https://")
        return False
    print_success("TAUTULLI_URL format looks valid")
    return True

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print_error(f"Invalid email format: {email}")
        return False
    print_success(f"Email format valid: {email}")
    return True

def validate_smtp_port(port):
    """Validate SMTP port"""
    try:
        port_num = int(port)
        if port_num not in [25, 465, 587, 2525]:
            print_warning(f"SMTP_PORT {port_num} is unusual (common: 587, 465, 25)")
        else:
            print_success(f"SMTP_PORT {port_num} is valid")
        return True
    except ValueError:
        print_error(f"SMTP_PORT must be a number, got: {port}")
        return False

def validate_dry_run(value):
    """Validate DRY_RUN setting"""
    if value.lower() == 'false':
        print_warning("DRY_RUN is set to FALSE - this will make REAL changes!")
        print_warning("Make sure you've tested thoroughly first!")
        return True
    elif value.lower() == 'true':
        print_success("DRY_RUN is TRUE - safe testing mode enabled")
        return True
    else:
        print_error(f"DRY_RUN must be 'true' or 'false', got: {value}")
        return False

def validate_vip_names(names):
    """Validate VIP names format"""
    if not names:
        print_info("No VIP users configured (VIP_NAMES is empty)")
        print_info("VIP users are protected from auto-removal")
        return True
    
    vip_list = [n.strip() for n in names.split(',')]
    print_success(f"VIP users configured: {len(vip_list)}")
    for vip in vip_list:
        print_info(f"  - {vip}")
    return True

def check_optional_fields(env_vars):
    """Check optional fields and provide recommendations"""
    print_header("Optional Configuration")
    
    # Discord
    if env_vars.get('DISCORD_WEBHOOK'):
        print_success("Discord webhook configured")
    else:
        print_info("Discord notifications disabled (optional)")
    
    # Thresholds
    warn_days = env_vars.get('WARN_DAYS', '27')
    kick_days = env_vars.get('KICK_DAYS', '30')
    try:
        warn = int(warn_days)
        kick = int(kick_days)
        if warn >= kick:
            print_warning(f"WARN_DAYS ({warn}) should be less than KICK_DAYS ({kick})")
        else:
            print_success(f"Warning at {warn} days, removal at {kick} days")
    except ValueError:
        print_error("WARN_DAYS and KICK_DAYS must be numbers")
    
    # Check intervals
    check_new = env_vars.get('CHECK_NEW_USERS_SECS', '120')
    check_inactive = env_vars.get('CHECK_INACTIVITY_SECS', '1800')
    print_info(f"Checking for new users every {check_new} seconds")
    print_info(f"Checking for inactive users every {check_inactive} seconds")

def main():
    print_header("Plex-Auto-Prune GUI - Configuration Validator")
    
    # Check if .env exists
    if not check_env_file_exists():
        sys.exit(1)
    
    # Load .env file
    env_vars = load_env_file()
    if env_vars is None:
        sys.exit(1)
    
    print_header("Validating Required Configuration")
    
    # Validate required fields
    if not validate_required_fields(env_vars):
        print_error("\n❌ Configuration validation FAILED!")
        print_info("Please fix the errors above and run this script again.")
        sys.exit(1)
    
    print_header("Validating Field Formats")
    
    # Validate specific fields
    all_valid = True
    all_valid &= validate_plex_token(env_vars.get('PLEX_TOKEN', ''))
    all_valid &= validate_tautulli_url(env_vars.get('TAUTULLI_URL', ''))
    all_valid &= validate_email(env_vars.get('SMTP_USERNAME', ''))
    all_valid &= validate_email(env_vars.get('ADMIN_EMAIL', ''))
    all_valid &= validate_smtp_port(env_vars.get('SMTP_PORT', '587'))
    all_valid &= validate_dry_run(env_vars.get('DRY_RUN', 'true'))
    validate_vip_names(env_vars.get('VIP_NAMES', ''))
    
    # Check optional fields
    check_optional_fields(env_vars)
    
    # Final verdict
    print_header("Validation Summary")
    
    if all_valid:
        print_success("✅ Configuration validation PASSED!")
        print_info("\nNext steps:")
        print_info("  1. Start the application: docker-compose up -d")
        print_info("  2. Access web UI: http://localhost:8080")
        print_info("  3. Monitor logs: docker logs plex-auto-prune-gui -f")
        print_info("  4. Keep DRY_RUN=true for 1-2 weeks of testing!")
        print_info("\nFor detailed setup instructions, see: SETUP.md")
        sys.exit(0)
    else:
        print_error("❌ Configuration validation FAILED!")
        print_info("Please fix the errors above and run this script again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
