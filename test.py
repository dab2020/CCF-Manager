def increment_and_return_value(filename='crmpwd.txt'):
    try:
        # Try to open the file in read mode
        with open(filename, 'r') as file:
            value = int(file.read().strip())
    except FileNotFoundError:
        # If the file does not exist, start with the value 1
        value = 0

    # Increment the value by 1
    value += 1

    # Write the updated value back to the file
    with open(filename, 'w') as file:
        file.write(str(value))

    # Return the updated value
    return value

# Example usage
current_value = increment_and_return_value()
print(current_value)
