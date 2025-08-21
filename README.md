# Ollama Chat CLI

A robust command-line interface for Ollama built with Java, featuring persistent chat sessions, starring, tagging, and export functionality for your AI conversations.

## Features

- 💬 **Persistent Chat Sessions** - Save and resume conversations across sessions
- ⭐ **Star Important Chats** - Mark your favorite conversations for easy access
- 🏷️ **Chat Tagging** - Organize chats with custom tags
- 📚 **Chat History** - View and manage all your previous conversations
- 📤 **Export Functionality** - Export chats to JSON or text formats
- 🔄 **Resume Conversations** - Pick up where you left off in any chat
- 💾 **File-based Storage** - Local JSON storage with no external dependencies

## Installation

### Prerequisites

- Java 11 or higher
- [Ollama](https://ollama.ai/) installed and running
- Maven (for building from source)

### Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ollama-chat-cli.git
   cd ollama-chat-cli
   ```

2. Build with Maven:
   ```bash
   mvn clean package
   ```

3. The executable JAR will be created at `target/ollama-cli-1.0-SNAPSHOT.jar`

### Installation

1. Copy the JAR to a directory in your PATH:
   ```bash
   sudo cp target/ollama-cli-1.0-SNAPSHOT.jar /usr/local/bin/ollama-cli.jar
   ```

2. Create a shell script wrapper:
   ```bash
   echo '#!/bin/bash
   java -jar /usr/local/bin/ollama-cli.jar "$@"' | sudo tee /usr/local/bin/ollama-cli
   sudo chmod +x /usr/local/bin/ollama-cli
   ```

## Usage

### Start a New Chat

```bash
ollama-cli chat <model_name>
```

Example:
```bash
ollama-cli chat llama2
```

When starting a new chat, you'll be prompted for:
- **Chat title** (optional - auto-generated if empty)
- **Tags** (optional - comma-separated)

### Resume an Existing Chat

```bash
ollama-cli chat <model_name> --resume <chat_id>
```

Example:
```bash
ollama-cli chat llama2 --resume 5
```

### List All Chats

```bash
ollama-cli list
```

Show only starred chats:
```bash
ollama-cli list --starred
```

### Star/Unstar Chats

Star a chat:
```bash
ollama-cli star <chat_id>
```

Unstar a chat:
```bash
ollama-cli unstar <chat_id>
```

You can also star/unstar during a chat session using `/star` and `/unstar` commands.

### Delete a Chat

```bash
ollama-cli delete <chat_id>
```

### Export Chat

Export to JSON (default):
```bash
ollama-cli export <chat_id>
```

Export to text file:
```bash
ollama-cli export <chat_id> --format txt
```

## Interactive Commands

While in a chat session, you can use these commands:

- `exit` - End the chat session
- `/star` - Star the current chat
- `/unstar` - Unstar the current chat

## Data Storage

The CLI stores all data locally using JSON files in:
```
~/.ollama-cli/
├── chats/
│   ├── chat-001.json
│   ├── chat-002.json
│   └── ...
└── index.json
```

### Storage Structure

#### `index.json`:
Contains chat metadata:
```json
{
  "chats": [
    {
      "id": "001",
      "title": "My Python Questions",
      "model": "llama2",
      "created_at": "2024-01-15T10:30:45Z",
      "starred": true,
      "tags": ["python", "programming"]
    }
  ]
}
```

#### Individual chat files (`chat-XXX.json`):
Contains conversation history:
```json
{
  "chat_id": "001",
  "messages": [
    {
      "role": "user",
      "content": "What are Python decorators?",
      "timestamp": "2024-01-15T10:31:00Z"
    },
    {
      "role": "assistant", 
      "content": "Python decorators are...",
      "timestamp": "2024-01-15T10:31:05Z"
    }
  ]
}
```

## Technical Implementation

### Dependencies

The project uses the following libraries:
- **OkHttp** - For HTTP requests to Ollama API
- **Gson** - For JSON parsing and serialization
- **JUnit** - For testing

### Key Components

- `OllamaClient` - Handles HTTP communication with Ollama
- `ChatManager` - Manages chat storage and retrieval
- `CommandParser` - Parses command line arguments
- `ChatSession` - Handles interactive chat sessions

## Examples

### Basic Usage

```bash
# Start a new chat with llama2
ollama-cli chat llama2

# List all chats
ollama-cli list

# Resume chat #3
ollama-cli chat llama2 --resume 3

# Star chat #3
ollama-cli star 3

# Export chat #3 to JSON
ollama-cli export 3
```

### Sample Chat Session

```
$ ollama-cli chat llama2
📝 Chat title (or press Enter for auto-title): My Java Questions
🏷  Tags (comma-separated, optional): java, programming

💬 Started new chat #001: My Java Questions

🚀 Chatting with llama2. Type 'exit' to quit, '/star' to star this chat.
============================================================

👤 You: What are Java streams?

🤖 Assistant: Java streams are a powerful feature introduced in Java 8 that provide a functional approach...

👤 You: /star
⭐ Chat starred!

👤 You: exit
👋 Chat session ended.
```

### Listing Chats

```
$ ollama-cli list

📚 All chats:
--------------------------------------------------------------------------------
⭐  #001 | My Java Questions                      | llama2         | 2024-01-15 10:30:45
    #002 | Code Review Session                    | codellama      | 2024-01-15 09:15:22
    #003 | General Questions                      | llama2         | 2024-01-14 16:45:10
```

## Development

### Project Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/yourname/ollamacli/
│   │       ├── Main.java
│   │       ├── OllamaClient.java
│   │       ├── ChatManager.java
│   │       ├── CommandParser.java
│   │       ├── ChatSession.java
│   │       └── models/
│   │           ├── Chat.java
│   │           └── Message.java
│   └── resources/
└── test/
    └── java/
        └── com/yourname/ollamacli/
            └── ...
```

### Running Tests

```bash
mvn test
```

### Development Mode

```bash
mvn exec:java -Dexec.mainClass="com.yourname.ollamacli.Main" -Dexec.args="chat llama2"
```

## Troubleshooting

### Common Issues

1. **"ollama: command not found"**
   - Ensure Ollama is installed and in your PATH
   - Check if Ollama service is running

2. **Java version errors**
   - Ensure you have Java 11 or higher installed
   - Check with `java --version`

3. **Permission errors**
   - Make sure the JAR is executable
   - Check permissions for the `~/.ollama-cli/` directory

4. **HTTP connection errors**
   - Verify Ollama is running on default port (11434)
   - Check firewall settings

### Getting Help

For command-specific help:
```bash
ollama-cli --help
ollama-cli chat --help
ollama-cli list --help
```

## Requirements

- Java 11 or higher
- Ollama installed and accessible via HTTP API
- Maven (for building from source)

## Performance

- **Fast startup**: Plain Java application starts in milliseconds
- **Low memory**: Minimal memory footprint compared to Spring Boot applications
- **Portable**: Single JAR file with no external dependencies

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Some ideas for improvements:

- Add search functionality for chat history
- Implement chat import functionality  
- Add support for system prompts
- Create configuration file support
- Add chat statistics and analytics
- Implement chat backup/restore features
- Add colored output for better readability
