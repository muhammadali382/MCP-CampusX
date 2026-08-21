import math
import random

from fastmcp import FastMCP

mcp = FastMCP(name="Math Server")


@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool
def power(base: float, exponent: float) -> float:
    """Raise a number to a given power."""
    return base ** exponent


@mcp.tool
def square_root(number: float) -> float:
    """Calculate the square root of a number."""
    if number < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(number)


@mcp.tool
def modulo(a: int, b: int) -> int:
    """Return the remainder after dividing a by b."""
    if b == 0:
        raise ValueError("Cannot calculate modulo by zero.")
    return a % b


@mcp.tool
def percentage(value: float, percent: float) -> float:
    """Calculate a percentage of a value."""
    return (value * percent) / 100


@mcp.tool
def absolute_value(number: float) -> float:
    """Return the absolute value of a number."""
    return abs(number)


@mcp.tool
def factorial(number: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if number < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    return math.factorial(number)


@mcp.tool
def average(numbers: list[float]) -> float:
    """Calculate the arithmetic average of a list of numbers."""
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    return sum(numbers) / len(numbers)


@mcp.tool
def maximum(numbers: list[float]) -> float:
    """Return the largest number in a list."""
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    return max(numbers)


@mcp.tool
def minimum(numbers: list[float]) -> float:
    """Return the smallest number in a list."""
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    return min(numbers)


@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll n six-sided dice and return the results."""
    if n_dice < 1:
        raise ValueError("n_dice must be at least 1.")

    return [random.randint(1, 6) for _ in range(n_dice)]


if __name__ == "__main__":
    mcp.run()