# YouTube MCP Server

A Model Context Protocol (MCP) server that provides access to YouTube API endpoints.

## Features

This MCP server provides the following YouTube operations:

### Channel Management
- **get_my_channel**: Get information about your YouTube channel
- **get_my_activities**: Get recent activities on your channel
- **get_my_playlists**: Get your channel's playlists
- **get_my_subscriptions**: Get your channel subscriptions

### Video Operations
- **search_videos**: Search for videos on YouTube
- **get_video_details**: Get detailed information about a specific video
- **get_channel_videos**: Get videos from a specific channel
- **get_popular_videos**: Get most popular videos by region
- **get_video_comments**: Get comments for a specific video

### Playlist Operations
- **get_playlist_items**: Get videos from a specific playlist
- **create_playlist**: Create a new playlist
- **add_video_to_playlist**: Add a video to a playlist

### Interaction Operations
- **subscribe_to_channel**: Subscribe to a YouTube channel
- **rate_video**: Like or dislike a video
- **post_comment**: Post a comment on a video

## Setup

### 1. Install Dependencies

```bash
cd youtube
pip install -r requirements.txt
```

### 2. Configure Google OAuth

You need to create OAuth credentials with the following scopes:
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/youtube`
- `https://www.googleapis.com/auth/youtube.upload`

Save your OAuth credentials as `secret.json` in this directory.

### 3. Authenticate

Run the authentication script:

```bash
python authenticate.py
```

This will:
1. Open a browser window for authentication
2. Create a `token.json` file to store your credentials
3. Reuse the token on subsequent runs

### 4. Configure Your MCP Client

#### For Claude Desktop (stdio mode - default)

Add this to your Claude Desktop MCP settings file:

**Location**: `~/.config/Claude/claude_desktop_config.json` (Linux)

```json
{
  "mcpServers": {
    "youtube": {
      "command": "python3",
      "args": ["/home/shadyskies/Desktop/mcp-tools/youtube/youtube_mcp_server.py"],
      "cwd": "/home/shadyskies/Desktop/mcp-tools/youtube"
    }
  }
}
```

#### For HTTP/SSE Transport

You can run the server with different transport modes:

**SSE (Server-Sent Events)**:
```bash
python youtube_mcp_server.py --transport sse --host 0.0.0.0 --port 8000
```

**Streamable HTTP**:
```bash
python youtube_mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8000
```

**stdio (default)**:
```bash
python youtube_mcp_server.py --transport stdio
```

## Usage Examples

### Get My Channel Info
```json
{
  "tool": "get_my_channel"
}
```

### Search Videos
```json
{
  "tool": "search_videos",
  "arguments": {
    "query": "python tutorial",
    "max_results": 10,
    "order": "relevance"
  }
}
```

### Get Video Details
```json
{
  "tool": "get_video_details",
  "arguments": {
    "video_id": "dQw4w9WgXcQ"
  }
}
```

### Create Playlist
```json
{
  "tool": "create_playlist",
  "arguments": {
    "title": "My Favorite Videos",
    "description": "A collection of my favorite videos",
    "privacy_status": "private"
  }
}
```

### Subscribe to Channel
```json
{
  "tool": "subscribe_to_channel",
  "arguments": {
    "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw"
  }
}
```

### Rate Video
```json
{
  "tool": "rate_video",
  "arguments": {
    "video_id": "dQw4w9WgXcQ",
    "rating": "like"
  }
}
```

## API Parameters

### Search Order Options
- `relevance` - Resources sorted by relevance (default)
- `date` - Resources sorted by creation date (newest first)
- `rating` - Resources sorted by rating
- `title` - Resources sorted alphabetically by title
- `viewCount` - Resources sorted by view count

### Privacy Status Options
- `private` - Only visible to you
- `unlisted` - Anyone with the link can view
- `public` - Visible to everyone

### Rating Options
- `like` - Like the video
- `dislike` - Dislike the video
- `none` - Remove previous rating

## Region Codes

Common region codes for `get_popular_videos`:
- `US` - United States
- `GB` - United Kingdom
- `CA` - Canada
- `AU` - Australia
- `IN` - India
- `JP` - Japan
- `DE` - Germany
- `FR` - France

## Troubleshooting

### "token.json not found" Error
Run the authentication script:
```bash
python authenticate.py
```

### Authentication Issues
If you get authentication errors:
1. Delete `token.json`
2. Run `python authenticate.py` again
3. Complete the OAuth flow in your browser

### Permission Denied
Make sure your OAuth credentials have the correct scopes enabled in the Google Cloud Console:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services → Credentials
3. Edit your OAuth 2.0 Client ID
4. Ensure all required scopes are enabled
5. Add `http://localhost:8080` to authorized redirect URIs

### Quota Limits
YouTube API has quota limits. If you exceed them, you'll get quota errors. Check your quota usage in the Google Cloud Console.

## Security Notes

- Keep `secret.json` and `token.json` secure and never commit them to version control
- The server uses OAuth 2.0 for secure authentication
- Access tokens are refreshed automatically when they expire
- All operations are performed with the authenticated user's permissions

## Logging

The server logs all operations to:
- Console/stderr (for real-time monitoring)
- `youtube_mcp_server.log` (for persistent records)

Log levels:
- `INFO`: Normal operations and key events
- `DEBUG`: Detailed information
- `WARNING`: Warnings
- `ERROR`: Authentication failures, API errors
