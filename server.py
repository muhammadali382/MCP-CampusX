import random
from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP(name="Demo Server")


@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll n six-sided dice and return the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]


@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b


# Run the server
if __name__ == "__main__":
    mcp.run(transport= "streamable-http", host="0.0.0.0", port=8000)