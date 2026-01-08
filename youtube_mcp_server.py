#!/usr/bin/env python3
"""
MCP Server for YouTube API
Provides access to YouTube operations through Model Context Protocol
"""

import json
import logging
import os
import argparse
from typing import Dict
from pathlib import Path

from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Uncomment following line to collect logs in a file
    # handlers=[logging.FileHandler("youtube_mcp_server.log"), logging.StreamHandler()],
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("youtube-mcp-server")

# Create FastMCP instance
mcp = FastMCP("CL YouTube MCP Server")

# Global service instance
_service = None


def _get_token_data(token_data: str) -> Dict:
    """Decode access token JSON string to dictionary"""
    try:
        token_data = json.loads(token_data)
        auth_data = {
            "token": token_data.get("token"),
            "refresh_token": token_data.get("refresh_token"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": token_data.get("client_id"),
            "client_secret": token_data.get("client_secret"),
            "scopes": token_data.get("scopes"),
        }
        return auth_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode access token: {e}")
        return {}


def _get_service(token_data: str):
    """Create YouTube service with provided access token"""
    auth_data = _get_token_data(token_data)
    logger.info("Creating YouTube API service with provided access token")
    # Don't pass scopes - the token already has its authorized scopes
    creds = Credentials(**auth_data)
    service = build("youtube", "v3", credentials=creds)
    logger.info("YouTube API service created successfully")
    return service


# Define MCP Tools


@mcp.tool(
    name="get_my_channel",
    description="Get information about the authenticated user's YouTube channel",
)
def get_my_channel(oauth_token: str) -> Dict:
    """Get my channel information"""
    logger.info("Executing get_my_channel")
    try:
        service = _get_service(oauth_token)

        request = service.channels().list(
            part="snippet,contentDetails,statistics", mine=True
        )
        response = request.execute()

        logger.info("Retrieved channel information")
        return response
    except Exception as e:
        logger.error(f"Error in get_my_channel: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="get_my_playlists",
    description="Get playlists from the authenticated user's channel",
)
def get_my_playlists(oauth_token: str, max_results: int = 25) -> Dict:
    """Get my playlists"""
    logger.info("Executing get_my_playlists")
    try:
        service = _get_service(oauth_token)

        request = service.playlists().list(
            part="snippet,contentDetails", mine=True, maxResults=min(max_results, 50)
        )
        response = request.execute()

        logger.info(f"Retrieved {len(response.get('items', []))} playlists")
        return response
    except Exception as e:
        logger.error(f"Error in get_my_playlists: {e}")
        return {"error": str(e)}


@mcp.tool(name="search_videos", description="Search for videos on YouTube")
def search_videos(
    oauth_token: str, query: str, max_results: int = 10, order: str = "relevance"
) -> Dict:
    """Search for videos"""
    logger.info(f"Executing search_videos with query: {query}")
    try:
        service = _get_service(oauth_token)

        request = service.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=min(max_results, 50),
            order=order,
        )
        response = request.execute()

        logger.info(f"Found {len(response.get('items', []))} videos")
        return response
    except Exception as e:
        logger.error(f"Error in search_videos: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="get_video_details",
    description="Get detailed information about a specific video by ID",
)
def get_video_details(oauth_token: str, video_id: str) -> Dict:
    """Get video details"""
    logger.info(f"Executing get_video_details for video: {video_id}")
    try:
        service = _get_service(oauth_token)

        request = service.videos().list(
            part="snippet,contentDetails,statistics,status", id=video_id
        )
        response = request.execute()

        logger.info("Retrieved video details")
        return response
    except Exception as e:
        logger.error(f"Error in get_video_details: {e}")
        return {"error": str(e)}


@mcp.tool(name="get_channel_videos", description="Get videos from a specific channel")
def get_channel_videos(
    oauth_token: str, channel_id: str, max_results: int = 25
) -> Dict:
    """Get videos from a channel"""
    logger.info(f"Executing get_channel_videos for channel: {channel_id}")
    try:
        service = _get_service(oauth_token)

        request = service.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            maxResults=min(max_results, 50),
            order="date",
        )
        response = request.execute()

        logger.info(f"Retrieved {len(response.get('items', []))} videos")
        return response
    except Exception as e:
        logger.error(f"Error in get_channel_videos: {e}")
        return {"error": str(e)}


@mcp.tool(name="get_playlist_items", description="Get videos from a specific playlist")
def get_playlist_items(
    oauth_token: str, playlist_id: str, max_results: int = 50
) -> Dict:
    """Get playlist items"""
    logger.info(f"Executing get_playlist_items for playlist: {playlist_id}")
    try:
        service = _get_service(oauth_token)

        request = service.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=min(max_results, 50),
        )
        response = request.execute()

        logger.info(f"Retrieved {len(response.get('items', []))} playlist items")
        return response
    except Exception as e:
        logger.error(f"Error in get_playlist_items: {e}")
        return {"error": str(e)}


@mcp.tool(name="get_video_comments", description="Get comments for a specific video")
def get_video_comments(
    oauth_token: str, video_id: str, max_results: int = 20, order: str = "relevance"
) -> Dict:
    """Get video comments"""
    logger.info(f"Executing get_video_comments for video: {video_id}")
    try:
        service = _get_service(oauth_token)

        request = service.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=min(max_results, 100),
            order=order,
        )
        response = request.execute()

        logger.info(f"Retrieved {len(response.get('items', []))} comments")
        return response
    except Exception as e:
        logger.error(f"Error in get_video_comments: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="get_my_subscriptions",
    description="Get the authenticated user's channel subscriptions",
)
def get_my_subscriptions(oauth_token: str, max_results: int = 25) -> Dict:
    """Get my subscriptions"""
    logger.info("Executing get_my_subscriptions")
    try:
        service = _get_service(oauth_token)

        request = service.subscriptions().list(
            part="snippet,contentDetails", mine=True, maxResults=min(max_results, 50)
        )
        response = request.execute()

        logger.info(f"Retrieved {len(response.get('items', []))} subscriptions")
        return response
    except Exception as e:
        logger.error(f"Error in get_my_subscriptions: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="get_my_activities",
    description="Get recent activities on the authenticated user's channel",
)
def get_my_activities(oauth_token: str, max_results: int = 25) -> Dict:
    """Get my channel activities"""
    logger.info("Executing get_my_activities")
    try:
        service = _get_service(oauth_token)

        request = service.activities().list(
            part="snippet,contentDetails", mine=True, maxResults=min(max_results, 50)
        )
        response = request.execute()

        logger.info(f"Retrieved {len(response.get('items', []))} activities")
        return response
    except Exception as e:
        logger.error(f"Error in get_my_activities: {e}")
        return {"error": str(e)}


@mcp.tool(
    name="create_playlist",
    description="Create a new playlist on the authenticated user's channel",
)
def create_playlist(
    oauth_token: str, title: str, description: str = "", privacy_status: str = "private"
) -> Dict:
    """Create a new playlist"""
    logger.info(f"Executing create_playlist: {title}")
    try:
        service = _get_service(oauth_token)

        request = service.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": title, "description": description},
                "status": {"privacyStatus": privacy_status},
            },
        )
        response = request.execute()

        logger.info(f"Created playlist: {response.get('id')}")
        return response
    except Exception as e:
        logger.error(f"Error in create_playlist: {e}")
        return {"error": str(e)}


@mcp.tool(name="add_video_to_playlist", description="Add a video to a playlist")
def add_video_to_playlist(oauth_token: str, playlist_id: str, video_id: str) -> Dict:
    """Add video to playlist"""
    logger.info(f"Executing add_video_to_playlist: {video_id} to {playlist_id}")
    try:
        service = _get_service(oauth_token)

        request = service.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        )
        response = request.execute()

        logger.info("Video added to playlist successfully")
        return response
    except Exception as e:
        logger.error(f"Error in add_video_to_playlist: {e}")
        return {"error": str(e)}


@mcp.tool(name="subscribe_to_channel", description="Subscribe to a YouTube channel")
def subscribe_to_channel(oauth_token: str, channel_id: str) -> Dict:
    """Subscribe to a channel"""
    logger.info(f"Executing subscribe_to_channel: {channel_id}")
    try:
        service = _get_service(oauth_token)

        request = service.subscriptions().insert(
            part="snippet",
            body={
                "snippet": {
                    "resourceId": {"kind": "youtube#channel", "channelId": channel_id}
                }
            },
        )
        response = request.execute()

        logger.info("Subscribed to channel successfully")
        return response
    except Exception as e:
        logger.error(f"Error in subscribe_to_channel: {e}")
        return {"error": str(e)}


@mcp.tool(name="rate_video", description="Rate a video (like or dislike)")
def rate_video(oauth_token: str, video_id: str, rating: str) -> Dict:
    """Rate a video (like, dislike, or none)"""
    logger.info(f"Executing rate_video: {video_id} with rating {rating}")
    try:
        service = _get_service(oauth_token)

        if rating not in ["like", "dislike", "none"]:
            return {"error": "Invalid rating. Must be 'like', 'dislike', or 'none'"}

        request = service.videos().rate(id=video_id, rating=rating)
        request.execute()

        logger.info(f"Video rated successfully: {rating}")
        return {"message": f"Video rated as '{rating}' successfully"}
    except Exception as e:
        logger.error(f"Error in rate_video: {e}")
        return {"error": str(e)}


@mcp.tool(name="post_comment", description="Post a comment on a video")
def post_comment(oauth_token: str, video_id: str, text: str) -> Dict:
    """Post a comment on a video"""
    logger.info(f"Executing post_comment on video: {video_id}")
    try:
        service = _get_service(oauth_token)

        request = service.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {"snippet": {"textOriginal": text}},
                }
            },
        )
        response = request.execute()

        logger.info("Comment posted successfully")
        return response
    except Exception as e:
        logger.error(f"Error in post_comment: {e}")
        return {"error": str(e)}


# Function for parsing the cmd-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="YouTube MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', 'sse', or 'streamable-http')",
        default=None,
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("YouTube MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    # Build kwargs for mcp.run() only with provided values
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        # Start the MCP server with optional transport/host/port
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
