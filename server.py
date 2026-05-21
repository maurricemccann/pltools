#!/usr/bin/env python3
"""
Psyched Luxuries — LAN test server.
Run on your computer, visit from your iPhone over Wi-Fi, Add to Home Screen.

Usage:  python3 server.py [port]
"""
import http.server, socketserver, socket, sys, os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".js": "application/javascript",
    }
    def end_headers(self):
        # No-cache on sw.js so updates flow during testing
        if self.path.endswith("sw.js"):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Service-Worker-Allowed", "/")
        super().end_headers()
    def log_message(self, *a, **k): pass  # quiet

ip = lan_ip()
print()
print("  \033[38;5;179m  P S Y C H E D   L U X U R I E S  \033[0m")
print("  \033[2m" + "─"*46 + "\033[0m")
print(f"  Local:    http://localhost:{PORT}/")
print(f"  Network:  \033[38;5;179mhttp://{ip}:{PORT}/\033[0m   ← on your iPhone")
print("  \033[2m" + "─"*46 + "\033[0m")
print()
print("  iPhone:  Safari → that URL → Share → Add to Home Screen")
print("  Stop:    Ctrl+C")
print()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), H) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Closed.")
