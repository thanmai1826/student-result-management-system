"""
main.py
-------
This is the main module of the Student Result Management System.
It handles user input, validation, and coordinates with the database module.
"""

import sys
import os

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import create_connection, create_table, insert_student, close_connection


def get_valid_integer(prompt, min_value=0, max_value=100):
    """
    Get a valid integer input from the user.
    
    Args:
        prompt (str): The prompt message to display
        min_value (int): Minimum allowed value (default: 0)
        max_value (int): Maximum allowed value (default: 100)
    
    Returns:
        int: Validated integer input
    """
    while True:
        try:
            value = int(input(prompt))
            
            if value < min_value or value > max_value:
                print(f"✗ Error: Please enter a value between {min_value} and {max_value}")
                continue
            
            return value
            
        except ValueError:
            print("✗ Error: Please enter a valid integer!")


def get_valid_name():
    """
    Get a valid name input from the user.
    
    Returns:
        str: Validated name input
    """
    while True:
        name = input("Enter student name: ").strip()
        
        if not name:
            print("✗ Error: Name cannot be empty!")
            continue
        
        if not name.replace(" ", "").isalpha():
            print("✗ Error: Name should contain only letters and spaces!")
            continue
        
        return name


def calculate_results(subject1, subject2, subject3):
    """
    Calculate total and percentage from subject marks.
    
    Args:
        subject1 (int): Marks for subject 1
        subject2 (int): Marks for subject 2
        subject3 (int): Marks for subject 3
    
    Returns:
        tuple: (total_marks, percentage)
    """
    total = subject1 + subject2 + subject3
    percentage = (total / 300) * 100
    return total, percentage


def add_student():
    """
    Main function to add a new student to the system.
    """
    print("\n" + "=" * 60)
    print("ADD NEW STUDENT")
    print("=" * 60)
    
    # Get student name
    name = get_valid_name()
    
    # Get subject marks
    print("\nEnter marks for 3 subjects (0-100):")
    subject1 = get_valid_integer("Subject 1 marks: ", 0, 100)
    subject2 = get_valid_integer("Subject 2 marks: ", 0, 100)
    subject3 = get_valid_integer("Subject 3 marks: ", 0, 100)
    
    # Calculate results
    total, percentage = calculate_results(subject1, subject2, subject3)
    
    # Display calculated results
    print("\n" + "-" * 40)
    print("CALCULATED RESULTS:")
    print("-" * 40)
    print(f"Total Marks: {total}/300")
    print(f"Percentage: {percentage:.2f}%")
    print("-" * 40)
    
    # Connect to database
    conn = create_connection()
    
    if conn:
        # Create table if not exists
        create_table(conn)
        
        # Insert student data
        student_id = insert_student(conn, name, subject1, subject2, subject3, total, percentage)
        
        if student_id:
            print(f"\n✓ Student added successfully!")
            print(f"  Student ID: {student_id}")
            print(f"  Name: {name}")
            print(f"  Total Marks: {total}")
            print(f"  Percentage: {percentage:.2f}%")
        else:
            print("\n✗ Failed to add student to database!")
        
        # Close connection
        close_connection(conn)
    
    return student_id is not None


def main_menu():
    """
    Display the main menu and handle user choices.
    """
    while True:
        print("\n" + "=" * 60)
        print("STUDENT RESULT MANAGEMENT SYSTEM")
        print("=" * 60)
        print("1. Add New Student")
        print("2. Exit")
        print("-" * 60)
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == "1":
            success = add_student()
            if success:
                print("\n✓ Operation completed successfully!")
            else:
                print("\n✗ Operation failed!")
        elif choice == "2":
            print("\n" + "=" * 60)
            print("Thank you for using Student Result Management System!")
            print("=" * 60)
            break
        else:
            print("\n✗ Invalid choice! Please enter 1 or 2.")


# This block runs when main.py is executed directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("STUDENT RESULT MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Welcome to the Student Result Management System!")
    print("This system helps you manage student records and results.")
    print("=" * 60)
    
    # Start the main menu
    main_menu()