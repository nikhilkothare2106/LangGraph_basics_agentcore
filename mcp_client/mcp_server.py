from mcp.server.fastmcp import FastMCP

mcp = FastMCP("arith")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a: Number to subtract from
        b: Number to subtract
    """
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b.

    Args:
        a: Numerator
        b: Denominator (must not be zero)
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the given exponent.

    Args:
        base: The base number
        exponent: The exponent to raise the base to
    """
    return base ** exponent


@mcp.tool()
def square_root(x: float) -> float:
    """Compute the square root of a number.

    Args:
        x: The number to take the square root of (must be >= 0)
    """
    if x < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return x ** 0.5


if __name__ == "__main__":
    # Runs over stdio by default, matching the "stdio" transport
    # configured in your MultiServerMCPClient
    mcp.run(transport="stdio")