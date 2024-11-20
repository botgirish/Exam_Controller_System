def has_uppercase(password):
    """Check if the password contains at least one uppercase letter."""
    for char in password:
        if char.isupper():
            return True
    return False

def has_lowercase(password):
    """Check if the password contains at least one lowercase letter."""
    for char in password:
        if char.islower():
            return True
    return False

def has_number(password):
    """Check if the password contains at least one digit."""
    for char in password:
        if char.isdigit():
            return True
    return False

def has_special_char(password):
    """Check if the password contains at least one special character from the allowed set."""
    special_chars = "!@#"
    for char in password:
        if char in special_chars:
            return True
    return False

def validate_password(password, criteria):
    if len(password) < 8:
        print(f"Password '{password}' is invalid. Length is less than 8 characters.")
        return False

    for criterion in criteria:
        if criterion == 1 and not has_uppercase(password):
            print(f"Password '{password}' is invalid. Missing uppercase letter.")
            return False
        elif criterion == 2 and not has_lowercase(password):
            print(f"Password '{password}' is invalid. Missing lowercase letter.")
            return False
        elif criterion == 3 and not has_number(password):
            print(f"Password '{password}' is invalid. Missing number.")
            return False
        elif criterion == 4 and not has_special_char(password):
            print(f"Password '{password}' is invalid. Missing special character.")
            return False

    print(f"Password '{password}' is valid.")
    return True

def main():
    password = input("Enter the password to validate: ")
    user_input = input("Enter criteria to check (1 - Uppercase, 2 - Lowercase, 3 - Numbers, 4 - Special characters): ")

    # Convert user input to a list of integers
    criteria = []
    for item in user_input.split(','):
        if item.strip().isdigit():
            criteria.append(int(item.strip()))

    validate_password(password, criteria)

if __name__ == "__main__":
    main()
