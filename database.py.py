"""
database.py
-----------
This module handles all database operations for the Student Result Management System.
It creates and manages the SQLite database connection and student table.
"""

import sqlite3
import os
from pathlib import Path


def get_database_path():
    """
    Get the absolute path to the database file.
    
    Returns:
        Path: Absolute path to students.db in the data folder
    """
    # Get the project root directory (parent of src folder)
    project_root = Path(__file__).parent.parent
    data_folder = project_root / "data"
    
    # Create data folder if it doesn't exist
    data_folder.mkdir(exist_ok=True)
    
    return data_folder / "students.db"


def create_connection():
    """
    Create a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    db_path = get_database_path()
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"✓ Database connection established successfully!")
        print(f"  Database location: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        return None


def create_table(conn):
    """
    Create the students table if it doesn't exist.
    
    Args:
        conn (sqlite3.Connection): Database connection object
    """
    try:
        cursor = conn.cursor()
        
        # SQL query to create students table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject1 INTEGER NOT NULL,
            subject2 INTEGER NOT NULL,
            subject3 INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✓ Students table created/verified successfully!")
        
    except sqlite3.Error as e:
        print(f"✗ Error creating table: {e}")


def insert_student(conn, name, subject1, subject2, subject3, total, percentage):
    """
    Insert a new student record into the database.
    
    Args:
        conn (sqlite3.Connection): Database connection object
        name (str): Student's name
        subject1 (int): Marks for subject 1
        subject2 (int): Marks for subject 2
        subject3 (int): Marks for subject 3
        total (int): Total marks
        percentage (float): Percentage calculated
    
    Returns:
        int: The ID of the newly inserted student, or None if failed
    """
    try:
        cursor = conn.cursor()
        
        # SQL query to insert student data
        insert_sql = """
        INSERT INTO students (name, subject1, subject2, subject3, total, percentage)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        
        cursor.execute(insert_sql, (name, subject1, subject2, subject3, total, percentage))
        conn.commit()
        
        student_id = cursor.lastrowid
        return student_id
        
    except sqlite3.Error as e:
        print(f"✗ Error inserting student: {e}")
        return None


def close_connection(conn):
    """
    Close the database connection.
    
    Args:
        conn (sqlite3.Connection): Database connection object
    """
    if conn:
        conn.close()
        print("✓ Database connection closed.")


# This block runs when database.py is executed directly
if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MODULE TEST")
    print("=" * 60)
    
    # Test database connection
    conn = create_connection()
    
    if conn:
        # Create table
        create_table(conn)
        
        # Close connection
        close_connection(conn)
        
        print("\n✓ Database module test completed successfully!")