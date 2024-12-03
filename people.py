"""A template for a python script deliverable for INST326.

Driver: Precious Onyenwe
Assignment: Exercise 7
Date: 10/26/2024

Challenges Encountered: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import argparse
import re
import sys
#run using python script_name.py employees.txt

def parse_name(text):
    """Extracts the first and last name from the provided text.
    
    Args:
        text (str): The input text containing a full name.
        
    Returns:
        tuple: A tuple containing the first and last name (first_name, last_name).
        If no match is found, returns (None, None).
    """
    match = re.search(r'(\w+)\s+(\w+)', text)
    if match: 
        first_name = match.group(1)
        last_name = match.group(2)
        return first_name, last_name
    return None, None

def parse_address(text):
    """Extracts the street address, city, and state from the provided text.
    
    Args:
        text (str): The input text containing an address.
        
    Returns:
        Address: An Address object with street, city, and state attributes if a match is found.
        If no match is found, returns None.
    """
    match = re.search(r'(\d+\s+[A-Za-z\s]+)\s+([A-Za-z_]+)\s+([A-Z]{2})', text)
    if match:
        street = match.group(1)
        city = match.group(2)
        state = match.group(3)
        return Address(street, city, state)
    return None

def parse_email(text):
    """Extracts an email address from the provided text.
    
    Args:
        text (str): The input text containing an email address.
        
    Returns:
        str: The extracted email address if a match is found.
        If no match is found, returns None.
    """
    match = re.search(r'[\w\.]+@[\w\.]+\w+', text)

    if match:
        return match.group(0)
    return None

class Address:
    """Represents a mailing address with a street, city, and state.
    
    Attributes:
        street (str): The street address.
        city (str): The city.
        state (str): The state (two-letter abbreviation).
    """
    def __init__(self, street, city, state):
        self.street = street
        self.city = city
        self.state = state

class Employee:
    """Represents an employee with a name, address, and email.
    
    Attributes:
        first_name (str): The employee's first name.
        last_name (str): The employee's last name.
        address (Address): The employee's address.
        email (str): The employee's email address.
    
    Methods:
        __init__(text): Initializes the employee object by parsing text.
    """
    def __init__(self, text):
        self.first_name, self.last_name = parse_name(text)
        self.address = parse_address(text)
        self.email = parse_email(text)

def main(path):
    """Reads employee data from a file and creates a list of Employee objects.
    
    Args:
        path (str): The path to the file containing employee data.
        
    Returns:
        list: A list of Employee objects.
    """
    employee_list = []
    with open(path, "r") as files:
        for file in files:
            employee = Employee(file.strip())
            employee_list.append(employee)
    return employee_list

def parse_args(args_list):
    """Parses command line arguments.
    
    Args:
        args_list (list): The list of command line arguments.
        
    Returns:
        argparse.Namespace: The parsed arguments as an object.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('required', type=float, help='This is an example of a required argument.')
    parser.add_argument('--optional', '-o', type=int, default=12, help='This is an example of an optional argument')
    args = parser.parse_args(args_list)
    return args

if __name__ == "__main__":
    """Main script execution. Reads employee data and prints details.
    """
    employees = main("people.txt")
    for employ in employees:
        print(f"Name: {employ.first_name} {employ.last_name}")
        print(f"Address: {employ.address.street}, {employ.address.city}, {employ.address.state}")
        print(f"Email: {employ.email}")

    # Handle command line arguments for additional functionality
    arguments = parse_args(sys.argv[1:])