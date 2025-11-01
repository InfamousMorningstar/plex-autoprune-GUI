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
    # Start worker threads (marked as daemon so they won't block program exit)
    t1 = threading.Thread(target=daemon_module.fast_join_watcher, daemon=True, name="JoinWatcher")
    t2 = threading.Thread(target=daemon_module.slow_inactivity_watcher, daemon=True, name="InactivityWatcher")
    
    t1.start()
    t2.start()
    
    print("[LAUNCHER] Daemon threads started")
    
    # Keep this thread alive to prevent it from exiting
    # This thread itself is a daemon thread, so it won't prevent the main process from exiting
    while True:
        time.sleep(1)
        # Check if worker threads are still alive
        if not t1.is_alive() or not t2.is_alive():
            print("[LAUNCHER WARNING] A daemon worker thread died!")
            break

def run_web():
    """Run the web interface"""
    try:
        import web
        print("[LAUNCHER] Web module imported successfully", flush=True)
        print(f"[LAUNCHER] Flask app: {web.app}", flush=True)
        print(f"[LAUNCHER] SocketIO: {web.socketio}", flush=True)
        print(f"[LAUNCHER] SocketIO async_mode: {web.socketio.async_mode}", flush=True)
        print("[LAUNCHER] Starting web interface on 0.0.0.0:8080...", flush=True)
        
        # Call web_log to announce startup
        web.web_log("=" * 60)
        web.web_log("Plex-Auto-Prune GUI Web Interface Starting")
        web.web_log("Listening on http://0.0.0.0:8080")
        web.web_log("=" * 60)
        
        # Start the server with explicit logging
        print("[LAUNCHER] Calling socketio.run()...", flush=True)
        web.socketio.run(
            web.app, 
            host='0.0.0.0', 
            port=8080, 
            debug=False,  # PRODUCTION: Debug disabled for security
            use_reloader=False,  # Disable reloader in production
            log_output=True  # Enable logging
        )
        print("[LAUNCHER] socketio.run() returned (should never happen)", flush=True)
    except Exception as e:
        print(f"[LAUNCHER ERROR] Failed to import or start web module: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    print("=" * 70)
    print("Plex-Auto-Prune GUI - Plex User Management System")
    print("=" * 70)
    print()
    
    # Start daemon in background thread
    daemon_thread = threading.Thread(target=run_daemon, daemon=True, name="DaemonMain")
    daemon_thread.start()
    
    print(f"[LAUNCHER] Daemon thread started, is alive: {daemon_thread.is_alive()}", flush=True)
    
    # Give daemon a moment to initialize
    print("[LAUNCHER] Entering sleep...", flush=True)
    time.sleep(0.1)  # Reduce to 0.1 seconds for testing
    print("[LAUNCHER] Sleep completed", flush=True)
    
    print(f"[LAUNCHER] After sleep, daemon thread is alive: {daemon_thread.is_alive()}", flush=True)
    print("[LAUNCHER] About to start web server...", flush=True)
    
    # Start web server (blocks on main thread)
    try:
        run_web()
    except KeyboardInterrupt:
        print("\n[LAUNCHER] Shutdown requested")
        os._exit(0)
    except Exception as e:
        print(f"\n[LAUNCHER ERROR] Web server failed to start: {e}")
        import traceback
        traceback.print_exc()
        os._exit(1)
