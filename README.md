**Manage YouTube channels, videos, playlists, and analytics via API.**

A Model Context Protocol (MCP) server that exposes YouTube's API for managing channels, uploading content, interacting with videos, and accessing comprehensive analytics.

---

## Overview

The YouTube MCP Server provides stateless, multi-user access to YouTube's core operations:

- **Channel Management** — Access and manage authenticated user's YouTube channel, subscriptions, and activities
- **Video Operations** — Search, retrieve, rate, and comment on videos with detailed metadata
- **Playlist Management** — Create playlists, manage playlist items, and organize video collections
- **Content Interaction** — Subscribe to channels, like/dislike videos, and post comments

Perfect for:

- Automated YouTube content management and distribution
- Building AI-powered video discovery and recommendation systems
- Integrating YouTube capabilities into multi-agent applications and workflows

---

## Tools

<details>
<summary><code>get_my_channel</code> — Get information about the authenticated user's YouTube channel</summary>

Retrieve detailed information about the authenticated user's YouTube channel including channel ID, name, subscriber count, and other metadata.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object with YouTube scopes

**Output:**

```json
{
  "result": {
    "kind": "youtube#channelListResponse",
    "pageInfo": {
      "totalResults": 1,
      "resultsPerPage": 1
    },
    "items": [
      {
        "id": "UCxxxxxxxxxxxxxx",
        "snippet": {
          "title": "Channel Name",
          "description": "Channel description"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_my_channel

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  }
}
```

</details>

---

<details>
<summary><code>get_my_playlists</code> — Get playlists from the authenticated user's channel</summary>

Retrieve all playlists created by the authenticated user with pagination support.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `max_results` (integer, optional) — Maximum playlists to return (default: 25)

**Output:**

```json
{
  "result": {
    "kind": "youtube#playlistListResponse",
    "pageInfo": {
      "totalResults": 5,
      "resultsPerPage": 25
    },
    "items": [
      {
        "id": "PLxxxxxxxxxxxxxx",
        "snippet": {
          "title": "My Playlist",
          "description": "Playlist description"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_my_playlists

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "max_results": 25
}
```

</details>

---

<details>
<summary><code>search_videos</code> — Search for videos on YouTube</summary>

Search for videos on YouTube using keywords with advanced filtering options.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `query` (string, required) — Search query string
- `max_results` (integer, optional) — Maximum results to return (default: 10)
- `order` (string, optional) — Sort order: "relevance", "date", "viewCount", "rating" (default: "relevance")

**Output:**

```json
{
  "result": {
    "kind": "youtube#searchListResponse",
    "pageInfo": {
      "totalResults": 1000000,
      "resultsPerPage": 10
    },
    "items": [
      {
        "kind": "youtube#searchResult",
        "id": {
          "videoId": "dQw4w9WgXcQ"
        },
        "snippet": {
          "title": "Video Title",
          "description": "Video description"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/search_videos

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "query": "machine learning tutorial",
  "max_results": 10,
  "order": "relevance"
}
```

</details>

---

<details>
<summary><code>get_video_details</code> — Get detailed information about a specific video by ID</summary>

Retrieve comprehensive details about a specific video including statistics, ratings, comments count, and metadata.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `video_id` (string, required) — The YouTube video ID

**Output:**

```json
{
  "result": {
    "kind": "youtube#videoListResponse",
    "pageInfo": {
      "totalResults": 1,
      "resultsPerPage": 1
    },
    "items": [
      {
        "id": "dQw4w9WgXcQ",
        "snippet": {
          "title": "Video Title",
          "description": "Video description",
          "publishedAt": "2024-01-01T12:00:00Z"
        },
        "statistics": {
          "viewCount": "1000000",
          "likeCount": "50000",
          "commentCount": "5000"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_video_details

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "video_id": "dQw4w9WgXcQ"
}
```

</details>

---

<details>
<summary><code>get_channel_videos</code> — Get videos from a specific channel</summary>

Retrieve all videos uploaded by a specific channel with pagination support.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `channel_id` (string, required) — The YouTube channel ID
- `max_results` (integer, optional) — Maximum videos to return (default: 25)

**Output:**

```json
{
  "result": {
    "kind": "youtube#searchListResponse",
    "pageInfo": {
      "totalResults": 100,
      "resultsPerPage": 25
    },
    "items": [
      {
        "id": {
          "videoId": "video-id-123"
        },
        "snippet": {
          "title": "Video Title",
          "channelId": "UCxxxxxxxxxxxxxx"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_channel_videos

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "channel_id": "UCxxxxxxxxxxxxxx",
  "max_results": 25
}
```

</details>

---

<details>
<summary><code>get_playlist_items</code> — Get videos from a specific playlist</summary>

Retrieve all videos in a specific playlist with full details and ordering.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `playlist_id` (string, required) — The YouTube playlist ID
- `max_results` (integer, optional) — Maximum items to return (default: 50)

**Output:**

```json
{
  "result": {
    "kind": "youtube#playlistItemListResponse",
    "pageInfo": {
      "totalResults": 50,
      "resultsPerPage": 50
    },
    "items": [
      {
        "id": "PLitem123",
        "snippet": {
          "title": "Video Title",
          "videoId": "dQw4w9WgXcQ",
          "position": 0
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_playlist_items

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "playlist_id": "PLxxxxxxxxxxxxxx",
  "max_results": 50
}
```

</details>

---

<details>
<summary><code>get_video_comments</code> — Get comments for a specific video</summary>

Retrieve comments on a video with filtering and sorting options.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `video_id` (string, required) — The YouTube video ID
- `max_results` (integer, optional) — Maximum comments to return (default: 20)
- `order` (string, optional) — Sort order: "relevance" or "time" (default: "relevance")

**Output:**

```json
{
  "result": {
    "kind": "youtube#commentThreadListResponse",
    "pageInfo": {
      "totalResults": 5000,
      "resultsPerPage": 20
    },
    "items": [
      {
        "snippet": {
          "videoId": "dQw4w9WgXcQ",
          "textDisplay": "Great video!",
          "authorDisplayName": "User Name"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_video_comments

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "video_id": "dQw4w9WgXcQ",
  "max_results": 20,
  "order": "relevance"
}
```

</details>

---

<details>
<summary><code>get_my_subscriptions</code> — Get the authenticated user's channel subscriptions</summary>

Retrieve all channels that the authenticated user is subscribed to.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `max_results` (integer, optional) — Maximum subscriptions to return (default: 25)

**Output:**

```json
{
  "result": {
    "kind": "youtube#subscriptionListResponse",
    "pageInfo": {
      "totalResults": 150,
      "resultsPerPage": 25
    },
    "items": [
      {
        "snippet": {
          "title": "Subscribed Channel",
          "channelId": "UCxxxxxxxxxxxxxx"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_my_subscriptions

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "max_results": 25
}
```

</details>

---

<details>
<summary><code>get_my_activities</code> — Get recent activities on the authenticated user's channel</summary>

Retrieve recent activities on the authenticated user's channel including uploads, likes, and other interactions.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `max_results` (integer, optional) — Maximum activities to return (default: 25)

**Output:**

```json
{
  "result": {
    "kind": "youtube#activityListResponse",
    "pageInfo": {
      "totalResults": 100,
      "resultsPerPage": 25
    },
    "items": [
      {
        "id": "activity-123",
        "snippet": {
          "type": "upload",
          "title": "Activity Title"
        }
      }
    ]
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/get_my_activities

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "max_results": 25
}
```

</details>

---

<details>
<summary><code>create_playlist</code> — Create a new playlist on the authenticated user's channel</summary>

Create a new playlist with customizable title, description, and privacy settings.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `title` (string, required) — Playlist title
- `description` (string, optional) — Playlist description (default: "")
- `privacy_status` (string, optional) — Privacy level: "private", "public", or "unlisted" (default: "private")

**Output:**

```json
{
  "result": {
    "kind": "youtube#playlist",
    "id": "PLxxxxxxxxxxxxxx",
    "snippet": {
      "title": "My New Playlist",
      "description": "Playlist description"
    },
    "status": {
      "privacyStatus": "private"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/create_playlist

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "title": "My New Playlist",
  "description": "A collection of my favorite videos",
  "privacy_status": "private"
}
```

</details>

---

<details>
<summary><code>add_video_to_playlist</code> — Add a video to a playlist</summary>

Add a specific video to an existing playlist.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `playlist_id` (string, required) — The target playlist ID
- `video_id` (string, required) — The video ID to add

**Output:**

```json
{
  "result": {
    "kind": "youtube#playlistItem",
    "id": "PLitem456",
    "snippet": {
      "playlistId": "PLxxxxxxxxxxxxxx",
      "videoId": "dQw4w9WgXcQ"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/add_video_to_playlist

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "playlist_id": "PLxxxxxxxxxxxxxx",
  "video_id": "dQw4w9WgXcQ"
}
```

</details>

---

<details>
<summary><code>subscribe_to_channel</code> — Subscribe to a YouTube channel</summary>

Subscribe the authenticated user to a specific YouTube channel.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `channel_id` (string, required) — The channel ID to subscribe to

**Output:**

```json
{
  "result": {
    "kind": "youtube#subscription",
    "id": "subscription-123",
    "snippet": {
      "title": "Channel Name",
      "channelId": "UCxxxxxxxxxxxxxx"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/subscribe_to_channel

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "channel_id": "UCxxxxxxxxxxxxxx"
}
```

</details>

---

<details>
<summary><code>rate_video</code> — Rate a video (like or dislike)</summary>

Like, dislike, or clear rating for a video.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `video_id` (string, required) — The video ID to rate
- `rating` (string, required) — Rating action: "like", "dislike", or "none"

**Output:**

```json
{
  "result": {
    "message": "Video rated successfully"
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/rate_video

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "video_id": "dQw4w9WgXcQ",
  "rating": "like"
}
```

</details>

---

<details>
<summary><code>post_comment</code> — Post a comment on a video</summary>

Post a comment on a specific video as the authenticated user.

**Inputs:**

- `oauth_token` (object, required) — Valid Google OAuth token object
- `video_id` (string, required) — The video ID to comment on
- `text` (string, required) — Comment text content

**Output:**

```json
{
  "result": {
    "kind": "youtube#comment",
    "id": "comment-123",
    "snippet": {
      "videoId": "dQw4w9WgXcQ",
      "textDisplay": "Great video!"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/cyoutube/post_comment

{
  "oauth_token": {
    "token": "ya29.a0AfH6SMxxxxxxxxxxxxxx",
    "refresh_token": "1//0xxxxx",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "xxxxx",
    "scopes": ["https://www.googleapis.com/auth/youtube"]
  },
  "video_id": "dQw4w9WgXcQ",
  "text": "Great video! Thanks for the tutorial."
}
```

</details>

---

## Reference & Support

<details>
<summary><strong>API Parameters Reference</strong></summary>

### Pagination

- `max_results` — Maximum results per page (varies by endpoint: 10-50)
- `nextPageToken` — Token for retrieving next page of results
- `prevPageToken` — Token for retrieving previous page of results

### Search & Filtering

- `query` — Search keywords for video search
- `order` — Sort results by: "relevance", "date", "viewCount", "rating"

### Content Types

- `kind` — Response type identifier (e.g., "youtube#video", "youtube#playlist")
- `type` — Activity type: "upload", "like", "subscribe", "favorite", "comment", "playlistItem"

### Resource Formats

**Video Resource:**

```
videos/{VIDEO_ID}
Example: dQw4w9WgXcQ
```

**Channel Resource:**

```
channels/{CHANNEL_ID}
Example: UCxxxxxxxxxxxxxx
```

**Playlist Resource:**

```
playlists/{PLAYLIST_ID}
Example: PLxxxxxxxxxxxxxx
```

</details>

---

<details>
<summary><strong>OAuth Guide</strong></summary>

All tools require a valid Google OAuth token. Here's how to obtain one:

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3** from the API Library

### Step 2: Create OAuth 2.0 Credentials

1. Navigate to **Credentials** in Google Cloud Console
2. Click **+ Create Credentials** → **OAuth client ID**
3. Select your application type (Desktop, Web, or other)
4. Download the credentials JSON file

### Step 3: Authenticate

Use your Google account to authenticate and obtain the OAuth token. Refer to [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2) for detailed authentication steps.

### Step 4: Required Scopes

Ensure your OAuth token has these scopes:

- `https://www.googleapis.com/auth/youtube` — Full YouTube account access
- `https://www.googleapis.com/auth/youtube.readonly` — Read-only access to YouTube
- `https://www.googleapis.com/auth/youtube.force-ssl` — HTTPS-only access

</details>

---

<details>
<summary><strong>Troubleshooting</strong></summary>

### **Missing or Invalid OAuth Token**

- **Cause:** OAuth token not provided in request or incorrect format
- **Solution:**
  1. Verify `oauth_token` parameter is present in request
  2. Check token is valid and not expired
  3. Obtain a fresh OAuth token from Google

### **Insufficient Permissions**

- **Cause:** OAuth token lacks required scopes for operation
- **Solution:**
  1. Verify token has all required YouTube scopes
  2. Regenerate token with additional scopes if needed
  3. Check Google Cloud project has YouTube Data API v3 enabled

### **Insufficient Credits**

- **Cause:** API calls have exceeded your requests limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

### **Malformed Request Payload**

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required parameters are included
  3. Check parameter types match expected values (string, integer, object)

### **Server Not Found**

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `/mcp/{server-name}/{tool-name}`
  2. Use lowercase server name: `/mcp/cyoutube/...`
  3. Check available servers in documentation

### **Video Not Found or Access Denied**

- **Cause:** Video ID is invalid or video is private/deleted
- **Solution:**
  1. Verify video ID is correct
  2. Check if video is public or accessible by authenticated user
  3. Ensure video hasn't been deleted or made private

### **Authentication Token Invalid or Expired**

- **Cause:** Token rejected by YouTube API or has expired
- **Solution:**
  1. Obtain a fresh OAuth token from Google
  2. Verify token has all required YouTube scopes
  3. Check token expiration and refresh if needed

### **Quota Exceeded**

- **Cause:** API quota for the day/month has been exceeded
- **Solution:**
  1. Check quota usage in Google Cloud Console
  2. Wait until quota resets (usually daily)
  3. Upgrade Google Cloud project plan for higher quota

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[YouTube API Documentation](https://developers.google.com/youtube/v3)** — Official YouTube API reference
- **[Google Cloud OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)** — Authentication setup guide
- **[YouTube Data API Reference](https://developers.google.com/youtube/v3/reference)** — Complete API endpoint reference
- **[YouTube API Quotas](https://developers.google.com/youtube/v3/getting-started#quota)** — Quota and rate limits
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification

</details>

---