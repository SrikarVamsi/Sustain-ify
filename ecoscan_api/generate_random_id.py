import uuid

def generate_unique_code() -> str:
    """Generates a unique code using UUID."""
    return str(uuid.uuid4())  # Generates a random UUID


if __name__ == "__main__":
    # Example usage
    # for i in range(10):
    #     print(generate_unique_code())
    ...
