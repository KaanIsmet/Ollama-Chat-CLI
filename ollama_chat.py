#!/usr/bin/env python3
"""
Enhanced CLI for Ollama with chat persistence, starring, and customization
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import argparse
import subprocess
import sys
from typing import Dict, List, Optional
class OllamaChatCLI:
    def __init__(self):
        self.db_path = Path.home() / ".ollama_chat" / "chats.db"
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for chat storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                model TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                starred BOOLEAN DEFAULT FALSE,
                tags TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_chat(self, title: str, model: str, tags: str = None) -> int:
        """Create a new chat session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO chats (title, model, tags) VALUES (?, ?, ?)",
            (title, model, tags or "")
        )
        
        chat_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return chat_id
    
    def add_message(self, chat_id: int, role: str, content: str):
        """Add a message to a chat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )
        
        conn.commit()
        conn.close()
    
    def get_chat_history(self, chat_id: int) -> List[Dict]:
        """Get all messages from a chat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, timestamp FROM messages WHERE chat_id = ? ORDER BY timestamp",
            (chat_id,)
        )
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "role": row[0],
                "content": row[1],
                "timestamp": row[2]
            })
        
        conn.close()
        return messages
    
    def list_chats(self, starred_only: bool = False) -> List[Dict]:
        """List all chats"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT id, title, model, created_at, starred, tags FROM chats"
        if starred_only:
            query += " WHERE starred = TRUE"
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query)
        
        chats = []
        for row in cursor.fetchall():
            chats.append({
                "id": row[0],
                "title": row[1],
                "model": row[2],
                "created_at": row[3],
                "starred": bool(row[4]),
                "tags": row[5]
            })
        
        conn.close()
        return chats
    
    def star_chat(self, chat_id: int, starred: bool = True):
        """Star or unstar a chat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE chats SET starred = ? WHERE id = ?",
            (starred, chat_id)
        )
        
        conn.commit()
        conn.close()
    
    def delete_chat(self, chat_id: int):
        """Delete a chat and all its messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
        
        conn.commit()
        conn.close()
    
    def chat_with_ollama(self, model: str, chat_id: Optional[int] = None, system_prompt: str = None):
        """Interactive chat with Ollama"""
        if chat_id:
            # Load existing chat
            history = self.get_chat_history(chat_id)
            print(f"\n🔄 Resuming chat #{chat_id}")
            
            # Display recent messages
            for msg in history[-5:]:  # Show last 5 messages
                role_emoji = "👤" if msg["role"] == "user" else "🤖"
                print(f"{role_emoji} {msg['role']}: {msg['content'][:100]}...")
        else:
            # Create new chat
            title = input("📝 Chat title (or press Enter for auto-title): ").strip()
            if not title:
                title = f"Chat with {model} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            tags = input("🏷️  Tags (comma-separated, optional): ").strip()
            chat_id = self.create_chat(title, model, tags)
            print(f"💬 Started new chat #{chat_id}: {title}")
        
        print(f"\n🚀 Chatting with {model}. Type 'exit' to quit, '/star' to star this chat.")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    break
                elif user_input == '/star':
                    self.star_chat(chat_id)
                    print("⭐ Chat starred!")
                    continue
                elif user_input == '/unstar':
                    self.star_chat(chat_id, False)
                    print("⭐ Chat unstarred!")
                    continue
                
                if not user_input:
                    continue
                
                # Save user message
                self.add_message(chat_id, "user", user_input)
                
                # Call Ollama
                print("🤖 Assistant: ", end="", flush=True)
                result = subprocess.run([
                    "ollama", "run", model, user_input
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    print(response)
                    # Save assistant message
                    self.add_message(chat_id, "assistant", response)
                else:
                    print(f"❌ Error: {result.stderr}")
                
            except KeyboardInterrupt:
                print("\n👋 Chat session ended.")
                break
    
    def export_chat(self, chat_id: int, format: str = "json"):
        """Export chat to file"""
        history = self.get_chat_history(chat_id)
        
        if format == "json":
            filename = f"chat_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(history, f, indent=2)
        elif format == "txt":
            filename = f"chat_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                for msg in history:
                    f.write(f"{msg['role'].upper()}: {msg['content']}\n")
                    f.write("-" * 50 + "\n")
        
        print(f"💾 Chat exported to {filename}")

def main():
    cli = OllamaChatCLI()
    
    parser = argparse.ArgumentParser(description="Enhanced Ollama CLI with chat persistence")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Start or resume a chat')
    chat_parser.add_argument('model', help='Ollama model to use')
    chat_parser.add_argument('--resume', type=int, help='Resume chat by ID')
    chat_parser.add_argument('--system', help='System prompt')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List chats')
    list_parser.add_argument('--starred', action='store_true', help='Show only starred chats')
    
    # Star command
    star_parser = subparsers.add_parser('star', help='Star a chat')
    star_parser.add_argument('chat_id', type=int, help='Chat ID to star')
    
    # Unstar command
    unstar_parser = subparsers.add_parser('unstar', help='Unstar a chat')
    unstar_parser.add_argument('chat_id', type=int, help='Chat ID to unstar')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a chat')
    delete_parser.add_argument('chat_id', type=int, help='Chat ID to delete')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export a chat')
    export_parser.add_argument('chat_id', type=int, help='Chat ID to export')
    export_parser.add_argument('--format', choices=['json', 'txt'], default='json', help='Export format')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'chat':
        cli.chat_with_ollama(args.model, args.resume, args.system)
    
    elif args.command == 'list':
        chats = cli.list_chats(args.starred)
        if not chats:
            print("📭 No chats found.")
            return
        
        print(f"\n📚 {'Starred chats' if args.starred else 'All chats'}:")
        print("-" * 80)
        for chat in chats:
            star = "⭐" if chat['starred'] else "  "
            print(f"{star} #{chat['id']:3d} | {chat['title'][:40]:40s} | {chat['model']:15s} | {chat['created_at'][:19]}")
    
    elif args.command == 'star':
        cli.star_chat(args.chat_id)
        print(f"⭐ Chat #{args.chat_id} starred!")
    
    elif args.command == 'unstar':
        cli.star_chat(args.chat_id, False)
        print(f"⭐ Chat #{args.chat_id} unstarred!")
    
    elif args.command == 'delete':
        confirm = input(f"❌ Are you sure you want to delete chat #{args.chat_id}? (y/N): ")
        if confirm.lower() == 'y':
            cli.delete_chat(args.chat_id)
            print(f"🗑️  Chat #{args.chat_id} deleted!")
    
    elif args.command == 'export':
        cli.export_chat(args.chat_id, args.format)

if __name__ == "__main__":
    main()
