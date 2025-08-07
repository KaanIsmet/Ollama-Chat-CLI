# Ollama Chat CLI

An enhanced command-line interface for Ollama that adds persistent chat sessions, starring, tagging, and export functionality to your AI conversations.

## Features

- 💬 **Persistent Chat Sessions** - Save and resume conversations across sessions
- ⭐ **Star Important Chats** - Mark your favorite conversations for easy access
- 🏷️ **Chat Tagging** - Organize chats with custom tags
- 📚 **Chat History** - View and manage all your previous conversations
- 📤 **Export Functionality** - Export chats to JSON or text formats
- 🔄 **Resume Conversations** - Pick up where you left off in any chat
- 🗃️ **SQLite Database** - Local storage with no external dependencies

## Installation

### Prerequisites

- Python 3.6 or higher
- [Ollama](https://ollama.ai/) installed and running

### Setup

1. Save the script as `ollama-chat.py`
2. Make it executable:
   ```bash
   chmod +x ollama-chat.py
   ```
3. Optionally, create a symlink for easy access:
   ```bash
   ln -s /path/to/ollama-chat.py /usr/local/bin/ollama-chat
   ```

## Usage

### Start a New Chat

```bash
python ollama-chat.py chat <model_name>
```

Example:
```bash
python ollama-chat.py chat llama2
```

When starting a new chat, you'll be prompted for:
- **Chat title** (optional - auto-generated if empty)
- **Tags** (optional - comma-separated)

### Resume an Existing Chat

```bash
python ollama-chat.py chat <model_name> --resume <chat_id>
```

Example:
```bash
python ollama-chat.py chat llama2 --resume 5
```

### List All Chats

```bash
python ollama-chat.py list
```

Show only starred chats:
```bash
python ollama-chat.py list --starred
```

### Star/Unstar Chats

Star a chat:
```bash
python ollama-chat.py star <chat_id>
```

Unstar a chat:
```bash
python ollama-chat.py unstar <chat_id>
```

You can also star/unstar during a chat session using `/star` and `/unstar` commands.

### Delete a Chat

```bash
python ollama-chat.py delete <chat_id>
```

### Export Chat

Export to JSON (default):
```bash
python ollama-chat.py export <chat_id>
```

Export to text file:
```bash
python ollama-chat.py export <chat_id> --format txt
```

## Interactive Commands

While in a chat session, you can use these commands:

- `exit` - End the chat session
- `/star` - Star the current chat
- `/unstar` - Unstar the current chat

## Database Storage

The CLI stores all data locally in an SQLite database located at:
```
~/.ollama_chat/chats.db
```

### Database Schema

The database contains two main tables:

#### `chats` table:
- `id` - Unique chat identifier
- `title` - Chat title
- `model` - Ollama model used
- `created_at` - Creation timestamp
- `starred` - Boolean flag for starred chats
- `tags` - Comma-separated tags

#### `messages` table:
- `id` - Unique message identifier
- `chat_id` - Reference to parent chat
- `role` - Either "user" or "assistant"
- `content` - Message content
- `timestamp` - Message timestamp

## Examples

### Basic Usage

```bash
# Start a new chat with llama2
python ollama-chat.py chat llama2

# List all chats
python ollama-chat.py list

# Resume chat #3
python ollama-chat.py chat llama2 --resume 3

# Star chat #3
python ollama-chat.py star 3

# Export chat #3 to JSON
python ollama-chat.py export 3
```

### Sample Chat Session

```
$ python ollama-chat.py chat llama2
📝 Chat title (or press Enter for auto-title): My Python Questions
🏷  Tags (comma-separated, optional): python, programming

💬 Started new chat #1: My Python Questions

🚀 Chatting with llama2. Type 'exit' to quit, '/star' to star this chat.
============================================================

👤 You: What are Python decorators?

🤖 Assistant: Python decorators are a powerful feature that allow you to modify or extend the behavior of functions...

👤 You: /star
⭐ Chat starred!

👤 You: exit
👋 Chat session ended.
```

### Listing Chats

```
$ python ollama-chat.py list

📚 All chats:
--------------------------------------------------------------------------------
⭐  #1 | My Python Questions                      | llama2         | 2024-01-15 10:30:45
    #2 | Code Review Session                      | codellama      | 2024-01-15 09:15:22
    #3 | General Questions                        | llama2         | 2024-01-14 16:45:10
```

## Configuration

The CLI automatically creates the necessary directories and database on first run. No additional configuration is required.

## Troubleshooting

### Common Issues

1. **"ollama: command not found"**
   - Ensure Ollama is installed and in your PATH
   - Check if Ollama service is running

2. **Permission errors**
   - Make sure the script is executable: `chmod +x ollama-chat.py`
   - Check permissions for the `~/.ollama_chat/` directory

3. **Database errors**
   - The database is automatically created on first run
   - If corrupted, you can safely delete `~/.ollama_chat/chats.db` (you'll lose chat history)

### Getting Help

For command-specific help:
```bash
python ollama-chat.py --help
python ollama-chat.py chat --help
python ollama-chat.py list --help
```

## Requirements

- Python 3.6+
- SQLite3 (included with Python)
- Ollama installed and accessible via command line

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Some ideas for improvements:

- Add search functionality for chat history
- Implement chat import functionality
- Add support for system prompts
- Create a web interface
- Add chat statistics and analytics
- Implement chat backup/restore features
