import http.server
import socketserver
import socket
import os
import zipfile
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def create_deploy_zip():
    zip_path = os.path.join(DIRECTORY, "cbse-class12-pyq-nishant.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(DIRECTORY):
            for file in files:
                if file.endswith('.zip') or file.endswith('.pyc') or file == 'package_and_share.py':
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, DIRECTORY)
                zipf.write(file_path, arcname)
    return zip_path

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == "__main__":
    ip = get_local_ip()
    zip_file = create_deploy_zip()
    
    print("=" * 65)
    print("   CBSE CLASS 12 PYQ PORTAL - MENTORED BY NISHANT MISHRA")
    print("=" * 65)
    print("\n[+] 1. OPEN ON MOBILE / TABLET / LAPTOP (SAME WI-FI):")
    print(f"    --> http://{ip}:{PORT}")
    print(f"    --> http://localhost:{PORT} (on this computer)")
    print("\n[+] 2. WANT A FREE WORLDWIDE LINK FOR ANYONE ANYWHERE?")
    print("    A deployment zip file has been created:")
    print(f"    --> {zip_file}")
    print("    You can drag & drop this file or the folder into:")
    print("    - Netlify Drop: https://app.netlify.com/drop (instant 10-second public link)")
    print("    - Tiiny Host:   https://tiiny.host (instant public link without setup)")
    print("\n" + "=" * 65)
    print("Server is RUNNING... (Press Ctrl+C to stop)")
    print("=" * 65 + "\n")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)
