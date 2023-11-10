# example/example_code.py

def calculate_sum(a, b):
    """
    Calculate and return the sum of two numbers.
    """
    return a + b

def calculate_subtract(x, y):
    # New function to subtract two numbers
    result = x - y
    return result

# Example usage
if __name__ == "__main__":
    sum_result = calculate_sum(5, 7)
    # Test the subtract function
    subtract_result = calculate_subtract(5, 3)
    print(f"The sum is: {sum_result}")
    print("The subtraction result is", subtract_result)

