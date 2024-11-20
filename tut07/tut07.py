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
        return False

    for criterion in criteria:
        if criterion == 1 and not has_uppercase(password):
            return False
        elif criterion == 2 and not has_lowercase(password):
            return False
        elif criterion == 3 and not has_number(password):
            return False
        elif criterion == 4 and not has_special_char(password):
            return False

    return True

def main():
    user_input = input("Enter criteria to check (1 - Uppercase, 2 - Lowercase, 3 - Numbers, 4 - Special characters): ")
    criteria = []
    for item in user_input.split(','):
        if item.strip().isdigit():
            criteria.append(int(item.strip()))

    valid_count = 0
    invalid_count = 0

    try:
        with open('input.txt', 'r') as file:
            passwords = file.readlines()

        for password in passwords:
            password = password.strip()
            if validate_password(password, criteria):
                valid_count += 1
                print(f"Password '{password}' is valid.")
            else:
                invalid_count += 1
                print(f"Password '{password}' is invalid.")

    except FileNotFoundError:
        print("The file 'input.txt' was not found.")

    print(f"\nTotal valid passwords: {valid_count}")
    print(f"Total invalid passwords: {invalid_count}")

if __name__ == "__main__":
    main()
