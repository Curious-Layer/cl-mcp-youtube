import logging
from typing import Literal

from fastmcp import FastMCP

from .schemas import (
    ListToolResponse,
    MessageToolResponse,
    OAuthTokenData,
    ResourceToolResponse,
)
from .service import get_service


logger = logging.getLogger("youtube-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        name="get_my_channel",
        description="Get information about the authenticated user's YouTube channel",
    )
    def get_my_channel(oauth_token: OAuthTokenData) -> ListToolResponse:
        logger.info("Executing get_my_channel")
        try:
            service = get_service(oauth_token)

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
    def get_my_playlists(
        oauth_token: OAuthTokenData, max_results: int = 25
    ) -> ListToolResponse:
        logger.info("Executing get_my_playlists")
        try:
            service = get_service(oauth_token)

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
        oauth_token: OAuthTokenData,
        query: str,
        max_results: int = 10,
        order: str = "relevance",
    ) -> ListToolResponse:
        logger.info(f"Executing search_videos with query: {query}")
        try:
            service = get_service(oauth_token)

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
    def get_video_details(
        oauth_token: OAuthTokenData, video_id: str
    ) -> ListToolResponse:
        logger.info(f"Executing get_video_details for video: {video_id}")
        try:
            service = get_service(oauth_token)

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
        oauth_token: OAuthTokenData, channel_id: str, max_results: int = 25
    ) -> ListToolResponse:
        logger.info(f"Executing get_channel_videos for channel: {channel_id}")
        try:
            service = get_service(oauth_token)

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
        oauth_token: OAuthTokenData, playlist_id: str, max_results: int = 50
    ) -> ListToolResponse:
        logger.info(f"Executing get_playlist_items for playlist: {playlist_id}")
        try:
            service = get_service(oauth_token)

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
        oauth_token: OAuthTokenData,
        video_id: str,
        max_results: int = 20,
        order: str = "relevance",
    ) -> ListToolResponse:
        logger.info(f"Executing get_video_comments for video: {video_id}")
        try:
            service = get_service(oauth_token)

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
    def get_my_subscriptions(
        oauth_token: OAuthTokenData, max_results: int = 25
    ) -> ListToolResponse:
        logger.info("Executing get_my_subscriptions")
        try:
            service = get_service(oauth_token)

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
    def get_my_activities(
        oauth_token: OAuthTokenData, max_results: int = 25
    ) -> ListToolResponse:
        logger.info("Executing get_my_activities")
        try:
            service = get_service(oauth_token)

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
        oauth_token: OAuthTokenData,
        title: str,
        description: str = "",
        privacy_status: str = "private",
    ) -> ResourceToolResponse:
        logger.info(f"Executing create_playlist: {title}")
        try:
            service = get_service(oauth_token)

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
    def add_video_to_playlist(
        oauth_token: OAuthTokenData, playlist_id: str, video_id: str
    ) -> ResourceToolResponse:
        logger.info(f"Executing add_video_to_playlist: {video_id} to {playlist_id}")
        try:
            service = get_service(oauth_token)

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
    def subscribe_to_channel(
        oauth_token: OAuthTokenData, channel_id: str
    ) -> ResourceToolResponse:
        logger.info(f"Executing subscribe_to_channel: {channel_id}")
        try:
            service = get_service(oauth_token)

            request = service.subscriptions().insert(
                part="snippet",
                body={
                    "snippet": {
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": channel_id,
                        }
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
    def rate_video(
        oauth_token: OAuthTokenData,
        video_id: str,
        rating: Literal["like", "dislike", "none"],
    ) -> MessageToolResponse:
        logger.info(f"Executing rate_video: {video_id} with rating {rating}")
        try:
            service = get_service(oauth_token)

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
    def post_comment(
        oauth_token: OAuthTokenData, video_id: str, text: str
    ) -> ResourceToolResponse:
        logger.info(f"Executing post_comment on video: {video_id}")
        try:
            service = get_service(oauth_token)

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
