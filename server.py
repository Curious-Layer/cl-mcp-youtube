import os
import json
import argparse
import requests

from fastmcp import FastMCP
from pathlib import Path
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from typing import Dict, Any
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import time
from datetime import datetime, timedelta


# Create an mcp
mcp = FastMCP("CL YouTube MCP Server")

# API Keys
YOUTUBE_API_KEY = None
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
BASE_DIR = Path(__file__).parent
CLIENT_SECRETS_FILE = BASE_DIR / "YOUTUBE_CLIENT_SECRETS_FILE.json"
YOUTUBE_AUTH_TOKEN_FILE = BASE_DIR / "YOUTUBE_AUTH_TOKEN_FILE.json"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
has_credentials = False
credentials = None


def save_credentials(credentials):
    """Save credentials to token.json file."""
    creds_dict = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
    }

    with open(YOUTUBE_AUTH_TOKEN_FILE, "w") as f:
        json.dump(creds_dict, f, indent=2)

    print(f"✅ Credentials saved to {YOUTUBE_AUTH_TOKEN_FILE}")


def load_credentials():
    """Load credentials from token.json if exists."""
    if not os.path.exists(YOUTUBE_AUTH_TOKEN_FILE):
        return None

    try:
        with open(YOUTUBE_AUTH_TOKEN_FILE, "r") as f:
            creds_dict = json.load(f)

        credentials = Credentials(
            token=creds_dict.get("token"),
            refresh_token=creds_dict.get("refresh_token"),
            token_uri=creds_dict.get("token_uri"),
            client_id=creds_dict.get("client_id"),
            client_secret=creds_dict.get("client_secret"),
            scopes=creds_dict.get("scopes"),
        )

        # Refresh token if expired
        if (
            credentials.expired
            and credentials.refresh_token
            and is_token_expiring_soon(credentials)
        ):
            print("🔄 Token expired, refreshing...")
            credentials.refresh(Request())
            save_credentials(credentials)

        return credentials

    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        if os.path.exists(YOUTUBE_AUTH_TOKEN_FILE):
            os.remove(YOUTUBE_AUTH_TOKEN_FILE)
        return None


def has_valid_credentials():
    """Check if we have valid credentials."""
    credentials = load_credentials()
    return credentials is not None and credentials.valid


def is_token_expiring_soon(credentials, minutes_before=10):
    """Check if token will expire soon."""
    if not credentials.expiry:
        return False

    # Check if token expires in next X minutes
    time_until_expiry = credentials.expiry - datetime.utcnow()
    return time_until_expiry.total_seconds() < (minutes_before * 60)


@mcp.tool(
    name="get_my_channel_activities_tool",
    description="This tool provides the recent activities of the user's own youtube channel",
)
def get_my_channel_activities_tool(max_results: int):
    # Get credentials and create an API client
    try:
        # First, try to load saved credentials
        credentials = load_credentials()

        # Check if we have valid credentials
        if credentials is None or not credentials.valid:
            print("🔐 No valid credentials found, authenticating...")

            if not os.path.exists(CLIENT_SECRETS_FILE):
                return {
                    "error": "Client secrets file not found",
                    "message": f"Please save OAuth credentials as {CLIENT_SECRETS_FILE}",
                }

            # Create OAuth flow
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, scopes
            )

            # Run local server for authentication
            print("🌐 Opening browser for authentication...")
            credentials = flow.run_local_server(port=8080)

            # Save credentials for future use
            save_credentials(credentials)
            print("✅ Authentication successful!")

        youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials
        )
        print("credentials : ", credentials)
        request = youtube.activities().list(
            part="snippet,contentDetails", maxResults=max_results, mine=True
        )
        response = request.execute()
        return response
    except googleapiclient.errors.HttpError as e:
        error_msg = f"YouTube API Error: {e.reason}"
        if e.resp.status == 401:
            error_msg += "\nCredentials expired. Please authenticate again."
            # Clear invalid credentials
            if os.path.exists(YOUTUBE_AUTH_TOKEN_FILE):
                os.remove(YOUTUBE_AUTH_TOKEN_FILE)
        return {"error": "API Error", "message": error_msg}
    except Exception as e:
        return {"error": str(e), "message": "Failed to get channel activities"}


@mcp.tool(
    name="get_video_summary_tool",
    description="This tool creates a summary of the youtube video url provided",
)
def get_video_summary_tool(
    part: str, channel_id: str, max_results: int, api_key: str
) -> str:
    """This tool creates a summary of the youtube video url provided"""
    return "no summary"


@mcp.tool(
    name="get_channel_activity_tool",
    description="This tool creates a summary of the youtube video url provided",
)
def get_channel_activity_tool(channel_id: str, max_results: int, api_key: str):
    """This tool creates a summary of the youtube video url provided"""
    # API endpoint
    url = "https://www.googleapis.com/youtube/v3/activities"

    # Required parameters
    params = {
        "part": "snippet,contentDetails",
        "channelId": channel_id,
        "maxResults": max_results,
        "key": api_key,
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None


@mcp.tool(
    name="get_list_by_video_ids_tool",
    description="This tool provides a list of youtube videos by the provided video ids",
)
def get_list_by_video_ids_tool(video_ids: str, api_key: str):
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_ids,
        "key": api_key,
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None


@mcp.tool(
    name="get_most_popular_videos_by_region_code_tool",
    description="This tool returns all the videos in the Most Popular Videos category by region code",
)
def get_most_popular_videos_by_region_code_tool(region_code: str, api_key: str):
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,contentDetails,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "key": api_key,
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None


# Function for parsing the cmd-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Maths MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', 'sse', or 'http')",
        default=None,
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Build kwargs for mcp.run() only with provided values
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
    if args.host:
        run_kwargs["host"] = args.host
    if args.port:
        run_kwargs["port"] = args.port

    # Start the MCP server with optional transport/host/port
    mcp.run(**run_kwargs)
