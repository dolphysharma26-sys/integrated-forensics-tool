"""
Database Setup Module
Initializes database connection and schema
"""

import sqlite3
import os
from typing import Optional, List, Dict, Any
from core.common.logger import setup_logger

logger = setup_logger(__name__)

class Database:
    """Database management class"""
    
    def __init__(self, db_path: str = "data/forensics.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor = None
        
        # Create data directory
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        logger.info(f"Database initialized at {db_path}")
    
    def connect(self):
        """Connect to database"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        logger.info("Database connected")
    
    def create_tables(self):
        """Create all required tables"""
        if not self.connection:
            self.connect()
        
        # Operations table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                operation_id TEXT PRIMARY KEY,
                operation_type TEXT NOT NULL,
                device_path TEXT,
                status TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                details TEXT
            )
        """)
        
        # Devices table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                name TEXT,
                path TEXT,
                size_gb REAL,
                filesystem TEXT,
                device_type TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP
            )
        """)
        
        # Files table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_id TEXT PRIMARY KEY,
                operation_id TEXT,
                filename TEXT,
                file_size INTEGER,
                file_hash TEXT,
                status TEXT,
                recovery_score REAL,
                FOREIGN KEY (operation_id) REFERENCES operations(operation_id)
            )
        """)
        
        # Audit table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_id TEXT,
                user TEXT,
                action TEXT,
                timestamp TIMESTAMP,
                details TEXT,
                FOREIGN KEY (operation_id) REFERENCES operations(operation_id)
            )
        """)
        
        self.connection.commit()
        logger.info("Database tables created")
    
    def insert_operation(self, operation: Dict) -> bool:
        """Insert operation record"""
        try:
            self.cursor.execute("""
                INSERT INTO operations 
                (operation_id, operation_type, device_path, status, start_time, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                operation.get("operation_id"),
                operation.get("operation_type"),
                operation.get("device_path"),
                operation.get("status"),
                operation.get("start_time"),
                operation.get("details")
            ))
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Insert operation failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    db = Database()
    db.connect()
    db.create_tables()
    print("Database ready")
    db.close()