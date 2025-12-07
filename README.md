# GameVerse - Digital Game Store

A modern digital game store application built with Streamlit and powered by Botpress AI chatbot integration. GameVerse provides a complete e-commerce experience for browsing, purchasing, and managing digital game collections.

## Features

- Browse and search game catalog with advanced filtering
- Shopping cart and wishlist management
- User profile and purchase history tracking
- Real-time AI assistant powered by Botpress
- Analytics dashboard with platform statistics
- Modern, responsive UI with dark theme

## Prerequisites

- Python 3.11 or higher
- UV package manager
- Botpress account with Chat API credentials

## Installation

### Installing UV

UV is a fast Python package manager written in Rust. Install it using one of the following methods:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Via pip:**
```bash
pip install uv
```

Verify the installation:
```bash
uv --version
```

### Project Setup

1. Clone the repository:
```bash
git clone https://github.com/AN1N8/GameVerse.git
cd GameVerse
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

This will install all dependencies specified in `pyproject.toml`:
- streamlit
- pandas
- numpy
- requests
- sseclient-py
- python-dotenv

## Configuration

### Botpress Setup

1. Create a Botpress account at [botpress.cloud](https://botpress.cloud)

2. Create a new chatbot and obtain your Chat API credentials:
   - Chat API ID
   - User Key

3. Create the Streamlit secrets directory:
```bash
mkdir -p .streamlit
```

4. Create a secrets file at `.streamlit/secrets.toml`:
```toml
CHAT_API_ID = "your-chat-api-id-here"

[[users]]
key = "your-user-key-here"
```

### Creating Botpress Users

Use the included script to create and register new users:

```bash
python create_botpress_user.py \
  --name "User Name" \
  --id "unique-user-id" \
  --chat_api_id "your-chat-api-id"
```

This will create the user and automatically append their credentials to `.streamlit/secrets.toml`.

To create a user without saving to secrets:
```bash
python create_botpress_user.py \
  --name "User Name" \
  --id "unique-user-id" \
  --chat_api_id "your-chat-api-id" \
  --no-secrets
```

## Running the Application

Start the Streamlit development server:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

## Project Structure

```
gameverse/
├── app.py                          # Main application entry point
├── create_botpress_user.py         # User creation utility
├── pyproject.toml                  # Project dependencies
├── data/
│   ├── __init__.py
│   └── games_data.py               # Game catalog data and filters
├── utils/
│   ├── __init__.py
│   ├── botpress_client.py          # Botpress API client
│   ├── helpers.py                  # UI helper functions
│   └── styling.py                  # Custom CSS styling
├── views/
│   ├── __init__.py
│   ├── analytics.py                # Analytics dashboard
│   ├── browse.py                   # Game browsing interface
│   ├── cart.py                     # Shopping cart
│   ├── chatbot.py                  # AI assistant chat interface
│   ├── home.py                     # Home page with featured games
│   ├── profile.py                  # User profile management
│   └── wishlist.py                 # Wishlist management
├── images/                         # Game cover images
└── knowledge/                      # Knowledge base for chatbot
```

## Key Components

### Botpress Client

The `BotpressClient` class in `utils/botpress_client.py` provides:
- User authentication and management
- Conversation creation and listing
- Message sending and retrieval with polling
- Rich media support (images, cards, carousels)
- Connection pooling and retry logic
- Response caching for performance

### Session State

The application maintains session state for:
- Shopping cart items
- Wishlist items
- User profile data
- Chatbot conversation history
- Active conversation tracking

### Views

Each view module renders a specific page:
- **Home**: Featured games and special offers
- **Browse**: Searchable game catalog with filters
- **Cart**: Shopping cart with checkout
- **Wishlist**: Saved games for later
- **Profile**: User information and purchase history
- **Analytics**: Platform statistics and metrics
- **Chatbot**: AI-powered game recommendations and support

## Development

### Adding Dependencies

To add new Python packages:

```bash
uv pip install package-name
```

To update `pyproject.toml` with the new dependency, edit the `dependencies` array manually or use:

```bash
uv pip freeze > requirements.txt
# Then manually update pyproject.toml
```

### Modifying the UI

Custom styling is defined in `utils/styling.py`. The design follows a modern dark theme inspired by Steam and Xbox Store interfaces.

### Extending the Chatbot

To enhance the chatbot capabilities:
1. Update the Botpress bot configuration in the cloud dashboard
2. Modify `utils/botpress_client.py` for new API features
3. Adjust `views/chatbot.py` for UI changes

## Troubleshooting

### Botpress Connection Issues

If the chatbot fails to connect:
1. Verify credentials in `.streamlit/secrets.toml`
2. Check network connectivity
3. Review Botpress API status
4. Check browser console for JavaScript errors

### Import Errors

If you encounter import errors:
```bash
uv pip install -e .
```

### Session State Issues

Clear Streamlit cache and session state:
- Press 'C' in the terminal running Streamlit
- Or add `?clear_cache=true` to the URL

## Production Deployment

For production deployment:

1. Set environment variables instead of secrets file:
```bash
export CHAT_API_ID="your-chat-api-id"
export USER_KEY="your-user-key"
```

2. Configure Streamlit for production in `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

3. Use a production WSGI server or deploy to:
   - Streamlit Community Cloud
   - Heroku
   - AWS/GCP/Azure
   - Docker container

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Contact support through the application
- Refer to Botpress documentation at [docs.botpress.cloud](https://docs.botpress.cloud)

## Acknowledgments

- Built with Streamlit
- AI powered by Botpress
- UI design inspired by modern game store platforms

