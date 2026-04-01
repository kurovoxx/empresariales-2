import libsql_client
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_client():
    url = os.getenv("TURSO_URL")
    token = os.getenv("TURSO_TOKEN")
    if not url.startswith("libsql://") and not url.startswith("https://"):
        url = f"https://{url}"
    return libsql_client.create_client_sync(url, auth_token=token)

def init_db():
    client = get_db_client()
    try:
        client.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        client.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                email TEXT NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups (id)
            )
        """)
    finally:
        client.close()

def get_groups():
    client = get_db_client()
    try:
        result = client.execute("SELECT id, name FROM groups")
        return [{"id": row[0], "name": row[1]} for row in result.rows]
    finally:
        client.close()

def create_group(name):
    client = get_db_client()
    try:
        client.execute("INSERT INTO groups (name) VALUES (?)", (name,))
    finally:
        client.close()

def update_group_name(group_id, new_name):
    client = get_db_client()
    try:
        client.execute("UPDATE groups SET name = ? WHERE id = ?", (new_name, group_id))
    finally:
        client.close()

def add_email_to_group(group_id, email):
    client = get_db_client()
    try:
        client.execute("INSERT INTO emails (group_id, email) VALUES (?, ?)", (group_id, email))
    finally:
        client.close()

def delete_email(email_id):
    client = get_db_client()
    try:
        client.execute("DELETE FROM emails WHERE id = ?", (email_id,))
    finally:
        client.close()

def get_emails_by_group(group_id):
    client = get_db_client()
    try:
        # Traemos también el ID para poder borrarlos
        result = client.execute("SELECT id, email FROM emails WHERE group_id = ?", (group_id,))
        return [{"id": row[0], "email": row[1]} for row in result.rows]
    finally:
        client.close()
