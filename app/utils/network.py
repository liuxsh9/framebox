"""Network utility functions."""

import socket
from typing import Optional


def get_local_ip() -> Optional[str]:
    """
    Get the local IP address of the machine.
    Returns the IP address used for LAN connectivity, not localhost.
    """
    try:
        # Connect to a public DNS server (doesn't actually send packets)
        # This helps us determine which network interface is used for external connections
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            # Only return if it's not localhost
            if local_ip and local_ip != "127.0.0.1":
                return local_ip
    except Exception:
        pass

    # Fallback: try to get hostname IP
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if local_ip and local_ip != "127.0.0.1":
            return local_ip
    except Exception:
        pass

    return None
