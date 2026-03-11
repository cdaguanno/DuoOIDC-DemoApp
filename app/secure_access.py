"""
secure_access.py
Handles all Cisco Secure Access API interactions.
OAuth2 client credentials token fetch + Network Tunnel Group operations.

API Base: https://api.sse.cisco.com/deployments/v2
Auth:     https://api.sse.cisco.com/auth/v2/token
"""

import os
import requests

# --- Credentials (will move to env vars for production) ---
SA_API_KEY    = 'cbd125afd7d3475b8d38d2d7684e034e'
SA_API_SECRET = '572ccaad44434f7799acbeb855fee2aa'

# --- API Endpoints ---
TOKEN_URL   = 'https://api.sse.cisco.com/auth/v2/token'
TUNNELS_URL = 'https://api.sse.cisco.com/deployments/v2/networktunnelgroups'


def get_access_token():
    """
    Fetches a short-lived OAuth2 bearer token using client credentials flow.
    Returns the token string, or None on failure.
    
    The token endpoint expects HTTP Basic Auth (key:secret) 
    with grant_type=client_credentials in the POST body.
    """
    response = requests.post(
        TOKEN_URL,
        auth=(SA_API_KEY, SA_API_SECRET),        # Basic auth header
        data={'grant_type': 'client_credentials'} # OAuth2 CC grant
    )

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"[SecureAccess] Token fetch failed: {response.status_code} {response.text}")
        return None


def get_tunnel_groups():
    """
    Returns list of all Network Tunnel Groups in the org.
    Includes live tunnel status via includeStatuses=true.
    
    Returns a list of tunnel group dicts, or empty list on failure.
    """
    token = get_access_token()
    if not token:
        return []

    response = requests.get(
        TUNNELS_URL,
        headers={'Authorization': f'Bearer {token}'},
        params={'includeStatuses': 'true', 'limit': 100}
    )

    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"[SecureAccess] Tunnel list failed: {response.status_code} {response.text}")
        return []

REGIONS_URL = 'https://api.sse.cisco.com/deployments/v2/regions'

def get_regions():
    """
    Returns list of available Secure Access regions for tunnel group deployment.
    Each region has: name, region (ID), description, continent.
    Used to populate the provisioning form dropdown.
    """
    token = get_access_token()
    if not token:
        return []

    response = requests.get(
        REGIONS_URL,
        headers={'Authorization': f'Bearer {token}'}
    )

    if response.status_code == 200:
        return response.json().get('regions', [])
    else:
        print(f"[SecureAccess] Regions fetch failed: {response.status_code} {response.text}")
        return []


def create_tunnel_group(name, region, device_type, routing_type, cidrs, auth_id_prefix, passphrase, bgp_as_number=None):
    """
    Creates a new Network Tunnel Group via POST.
    
    cidrs: list of CIDR strings e.g. ['10.1.0.0/24', '192.168.1.0/24']
    routing_type: 'static', 'bgp', or 'nat'
    
    Returns the full API response dict on success, or None on failure.
    """
    token = get_access_token()
    if not token:
        return None

    # Build routing data block — static requires networkCIDRs, nat requires null
    if routing_type == 'static':
        routing = {
            'type': 'static',
            'data': {'networkCIDRs': cidrs}
        }
    elif routing_type == 'bgp':
        routing = {
            'type': 'bgp',
            'data': {'asNumber': bgp_as_number}
        }
    elif routing_type == 'nat':
        routing = {
            'type': 'nat',
            'data': None
        }
    else:
        routing = {
            'type': 'static',
            'data': {'networkCIDRs': cidrs}
        }

    payload = {
            'name': name,
            'region': region,
            'deviceType': device_type,
            'authIdPrefix': auth_id_prefix,
            'passphrase': passphrase,
            'routing': routing
        }

    response = requests.post(
        TUNNELS_URL,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json=payload   # requests serializes dict to JSON and sets Content-Type
    )

    if response.status_code in (200, 201):
        return response.json()
    else:
        print(f"[SecureAccess] Create tunnel failed: {response.status_code} {response.text}")
        return None