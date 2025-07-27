"""Helper utility functions for the QA automation framework."""

import asyncio
import random
import string
from typing import Any, Callable, Dict, List, Optional
from faker import Faker

fake = Faker()


def generate_test_data() -> Dict[str, Any]:
    """Generate random test data for testing purposes.
    
    Returns:
        Dictionary containing various test data fields.
    """
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "password": generate_random_string(12),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "city": fake.city(),
        "country": fake.country(),
        "company": fake.company(),
        "text": fake.text(max_nb_chars=200),
    }


def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length.
    
    Args:
        length: Length of the random string.
        
    Returns:
        Random string.
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_cities() -> List[str]:
    """Generate a list of test cities for weather API testing.
    
    Returns:
        List of city names.
    """
    return [
        "London",
        "New York",
        "Tokyo",
        "Paris",
        "Berlin",
        "Sydney",
        "Moscow",
        "Mumbai",
        "Cairo",
        "Rio de Janeiro"
    ]


async def wait_for_condition(
    condition: Callable[[], bool],
    timeout: int = 30,
    interval: float = 0.5,
    error_message: str = "Condition was not met within timeout"
) -> None:
    """Wait for a condition to be true within a timeout period.
    
    Args:
        condition: Callable that returns True when condition is met.
        timeout: Maximum time to wait in seconds.
        interval: Time between condition checks in seconds.
        error_message: Error message to raise if timeout is exceeded.
        
    Raises:
        TimeoutError: If condition is not met within timeout.
    """
    start_time = asyncio.get_event_loop().time()
    
    while True:
        if condition():
            return
            
        current_time = asyncio.get_event_loop().time()
        if current_time - start_time >= timeout:
            raise TimeoutError(error_message)
            
        await asyncio.sleep(interval)


def validate_response_schema(response_data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate that response data contains required fields.
    
    Args:
        response_data: Response data to validate.
        required_fields: List of required field names.
        
    Returns:
        True if all required fields are present, False otherwise.
    """
    return all(field in response_data for field in required_fields) 