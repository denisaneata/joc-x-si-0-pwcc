#!/usr/bin/env python3
"""
Server Web Local pentru Jocul X și 0 (Tic-Tac-Toe).
Folosește librăria standard Python (http.server) fără dependențe externe.
"""

import http.server
import socket
import socketserver
import sys
import os
from pathlib import Path


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP cu setări optimizate pentru dezvoltare locală."""

    def end_headers(self) -> None:
        # Previne stocarea în cache în timpul testării locale
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:
        """Afișaj compact pentru log-urile de cereri HTTP."""
        sys.stdout.write(f"  [HTTP] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


def find_available_port(start_port: int = 8000, max_attempts: int = 20) -> int:
    """Găsește primul port disponibil începând de la start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"Nu s-a găsit niciun port liber în intervalul {start_port}-{start_port + max_attempts}.")


def start_server(port: int = 8000, host: str = "0.0.0.0") -> None:
    """Pornește serverul web local."""
    base_dir = Path(__file__).resolve().parent
    os.chdir(base_dir)

    selected_port = find_available_port(port)

    # Permite reutilizarea rapidă a portului
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer((host, selected_port), CustomHTTPRequestHandler) as httpd:
        local_url = f"http://localhost:{selected_port}"
        network_url = f"http://127.0.0.1:{selected_port}"

        print("=" * 64)
        print("🎮 SERVER WEB LOCAL ACTIV - JOCUL X ȘI 0")
        print("=" * 64)
        print(f"  👉 Deschide în browser: \033[1;96m{local_url}\033[0m")
        print(f"  👉 Alternativă:         \033[1;92m{network_url}\033[0m")
        print(f"  📁 Director rădăcină:   {base_dir}")
        print("=" * 64)
        print("  Apasă Ctrl + C în terminal pentru a opri serverul.\n")
        sys.stdout.flush()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Oprire server web... La revedere! 👋")
            httpd.shutdown()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    try:
        start_server(port_arg)
    except KeyboardInterrupt:
        print("\nServer oprit.")
        sys.exit(0)
