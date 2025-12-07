"""
Botpress Chat API Client - FIXED CACHING
High-performance client with reliable cache invalidation and polling support.
"""

import os
import json
import requests
import sseclient
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Constants
BASE_URI = "https://chat.botpress.cloud"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

# Connection pool settings
DEFAULT_TIMEOUT = 30  # seconds
STREAM_TIMEOUT = 120  # longer timeout for SSE streams


class BotpressClient:
    def __init__(self, api_id=None, user_key=None):
        self.api_id = api_id or os.getenv("CHAT_API_ID")
        self.user_key = user_key or os.getenv("USER_KEY")
        self.base_url = f"{BASE_URI}/{self.api_id}"
        self.headers = {
            **HEADERS,
            "x-user-key": self.user_key,
        }
        
        # Initialize session with connection pooling and retry strategy
        self.session = self._create_session()
        
        # Cache for reducing redundant API calls
        self._conversation_cache = {}
        self._user_cache = None

    def _create_session(self):
        """Create requests session with connection pooling and retry logic"""
        session = requests.Session()
        
        # Retry strategy for failed requests
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
        )
        
        # Mount adapter with connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def _request(self, method, path, json_data=None, timeout=DEFAULT_TIMEOUT):
        """Make HTTP request with proper error handling and timeouts"""
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(
                method, 
                url, 
                headers=self.headers, 
                json=json_data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            return {"error": "Request timed out"}
        except requests.HTTPError as e:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def _parse_payload_to_markdown(self, payload):
        """Helper to convert rich media payloads (Image, Card, Carousel) into HTML/Markdown."""
        msg_type = payload.get("type")
        
        # CSS Styles
        img_style = 'width: 100%; height: auto; border-radius: 8px 8px 0 0;'
        card_container_style = (
            'border: 1px solid rgba(128, 128, 128, 0.2); '
            'border-radius: 8px; '
            'padding: 0px; '
            'max-width: 240px; '
            'margin: 5px 0; '
            'overflow: hidden;'
        )
        text_padding = 'padding: 8px 10px;'

        if msg_type == "image" and "image" in payload:
            image_url = payload["image"]
            title = payload.get("title", "Image")
            return f'<img src="{image_url}" alt="{title}" style="max-width: 250px; width: auto; border-radius: 8px;">'

        elif msg_type == "card":
            title = payload.get("title", "")
            image = payload.get("image", "")
            subtitle = payload.get("subtitle", "")
            
            html_output = f'<div style="{card_container_style}">'
            if image:
                html_output += f'<img src="{image}" style="{img_style}">'
            html_output += f'<div style="{text_padding}">'
            if title:
                html_output += f'<div style="font-weight: 600; margin-bottom: 2px;">{title}</div>'
            if subtitle:
                html_output += f'<div style="font-size: 0.85em; opacity: 0.8;">{subtitle}</div>'
            html_output += '</div></div>'
            return html_output

        elif msg_type == "carousel":
            items = payload.get("items", [])
            html_output = '<div style="display: flex; gap: 10px; overflow-x: auto; padding-bottom: 5px;">'
            for item in items:
                title = item.get("title", "")
                image = item.get("image", "")
                html_output += f'<div style="{card_container_style} min-width: 200px;">'
                if image:
                    html_output += f'<img src="{image}" style="{img_style}">'
                html_output += f'<div style="{text_padding}">'
                if title:
                    html_output += f'<div style="font-weight: 600;">{title}</div>'
                html_output += '</div></div>'
            html_output += '</div>'
            return html_output

        elif msg_type in ["single-choice", "choice"]:
            text = payload.get("text", "")
            choices = payload.get("choices", [])
            md_output = f"{text}\n\n"
            for choice in choices:
                label = choice.get("title", choice.get("value", ""))
                md_output += f"* {label}\n"
            return md_output

        return payload.get("text", "")

    # --- Core API Methods ---

    def get_user(self):
        """Get current user information with caching"""
        if self._user_cache is None:
            self._user_cache = self._request("GET", "/users/me")
        return self._user_cache

    def create_user(self, name, id):
        """Create a new user"""
        user_data = {"name": name, "id": id}
        result = self._request("POST", "/users", json_data=user_data)
        self._user_cache = None
        return result

    def set_user_key(self, key):
        """Set user key for authentication"""
        self.user_key = key
        self.headers["x-user-key"] = key
        self._user_cache = None

    def create_and_set_user(self, name, id):
        """Create user and set their key"""
        new_user = self.create_user(name, id)
        if "key" in new_user:
            self.set_user_key(new_user["key"])
        return new_user

    def create_conversation(self):
        """Create a new conversation"""
        result = self._request("POST", "/conversations", json_data={"body": {}})
        if "conversation" in result and "id" in result["conversation"]:
            # Initialize cache for this new conversation
            conv_id = result["conversation"]["id"]
            self._conversation_cache[f"{conv_id}_messages"] = {"messages": []}
        return result

    def list_conversations(self):
        """List all conversations for current user"""
        return self._request("GET", "/conversations")

    def get_conversation(self, conversation_id):
        """Get specific conversation details with caching"""
        if conversation_id not in self._conversation_cache:
            self._conversation_cache[conversation_id] = self._request(
                "GET", f"/conversations/{conversation_id}"
            )
        return self._conversation_cache[conversation_id]

    def create_message(self, message, conversation_id):
        """Send a message in a conversation"""
        payload = {
            "payload": {"type": "text", "text": message},
            "conversationId": conversation_id,
        }
        result = self._request("POST", "/messages", json_data=payload)
        
        # FIXED: Correctly invalidate the specific message cache key
        cache_key = f"{conversation_id}_messages"
        self._conversation_cache.pop(cache_key, None)
        
        return result

    def list_messages(self, conversation_id, limit=50, ignore_cache=False):
        """
        List messages with rich media parsing.
        """
        cache_key = f"{conversation_id}_messages"
        
        # Return cached if valid and not ignored
        if not ignore_cache and cache_key in self._conversation_cache:
            return self._conversation_cache[cache_key]
        
        # Fetch messages
        result = self._request(
            "GET", 
            f"/conversations/{conversation_id}/messages?limit={limit}"
        )
        
        # Pre-process messages (handle missing text in payloads)
        if "messages" in result:
            for msg in result["messages"]:
                if "payload" in msg:
                    current_text = msg["payload"].get("text")
                    if not current_text:
                        msg["payload"]["text"] = self._parse_payload_to_markdown(msg["payload"])

        # Update Cache
        self._conversation_cache[cache_key] = result
        return result

    def listen_conversation(self, conversation_id):
        """Listen to conversation events (SSE)."""
        url = f"{self.base_url}/conversations/{conversation_id}/listen"
        try:
            response = self.session.get(
                url, 
                headers=self.headers, 
                stream=True,
                timeout=STREAM_TIMEOUT
            )
            response.raise_for_status()
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data == "ping": continue
                try:
                    event_data = json.loads(event.data)
                    if "data" in event_data:
                        data = event_data["data"]
                        if "payload" in data:
                            markdown_content = self._parse_payload_to_markdown(data["payload"])
                            if markdown_content:
                                yield markdown_content
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def close(self):
        """Close the session and cleanup resources"""
        if hasattr(self, 'session'):
            self.session.close()
        self._conversation_cache.clear()
        self._user_cache = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False