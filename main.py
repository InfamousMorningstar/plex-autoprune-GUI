#!/usr/bin/env python3
"""
Plex-Auto-Prune GUI - Combined daemon + web interface launcher
Starts both the monitoring daemon and web interface in separate threads
"""
import threading
import time
import os

def run_daemon():
    """Run the monitoring daemon"""
    import daemon as d
    print("[LAUNCHER] Starting Plex-Auto-Prune GUI daemon...")
    # The daemon's main() will be called
    d.main() if hasattr(d, 'main') else run_daemon_threads(d)

def run_daemon_threads(daemon_module):
    """Start daemon worker threads"""
    import signal
    
    # Start worker threads
    t1 = threading.Thread(target=daemon_module.fast_join_watcher, daemon=True, name="JoinWatcher")
    t2 = threading.Thread(target=daemon_module.slow_inactivity_watcher, daemon=True, name="InactivityWatcher")
    
    t1.start()
    t2.start()
    
    print("[LAUNCHER] Daemon threads started")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[LAUNCHER] Shutting down daemon...")
        daemon_module.stop_event.set()

def run_web():
    """Run the web interface"""
    import web
    print("[LAUNCHER] Starting web interface on port 8080...")
    # Web server will block on this thread
    web.socketio.run(web.app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    print("=" * 70)
    print("Plex-Auto-Prune GUI - Plex User Management System")
    print("=" * 70)
    print()
    
    # Start daemon in background thread
    daemon_thread = threading.Thread(target=run_daemon, daemon=True, name="DaemonMain")
    daemon_thread.start()
    
    # Give daemon a moment to initialize
    time.sleep(2)
    
    # Start web server (blocks on main thread)
    try:
        run_web()
    except KeyboardInterrupt:
        print("\n[LAUNCHER] Shutdown requested")
        os._exit(0)
