"""
Lab 2 Solution: Text Utility Server

This is the complete implementation of the text utility server from Lab 2.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Text Utility Server")


@mcp.tool()
def word_count(text: str) -> int:
    """Count the number of words in the given text.

    Args:
        text: The text to count words in

    Returns:
        The number of words in the text
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


@mcp.tool()
def char_count(text: str) -> int:
    """Count the number of characters in the given text.

    Args:
        text: The text to count characters in

    Returns:
        The number of characters in the text (including spaces)
    """
    return len(text)


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse the given text.

    Args:
        text: The text to reverse

    Returns:
        The reversed text
    """
    return text[::-1]


@mcp.tool()
def to_uppercase(text: str) -> str:
    """Convert the given text to uppercase.

    Args:
        text: The text to convert

    Returns:
        The text in uppercase
    """
    return text.upper()


# Bonus tools not required by the lab


@mcp.tool()
def to_lowercase(text: str) -> str:
    """Convert the given text to lowercase.

    Args:
        text: The text to convert

    Returns:
        The text in lowercase
    """
    return text.lower()


@mcp.tool()
def title_case(text: str) -> str:
    """Convert the given text to title case.

    Args:
        text: The text to convert

    Returns:
        The text in title case
    """
    return text.title()


@mcp.tool()
def line_count(text: str) -> int:
    """Count the number of lines in the given text.

    Args:
        text: The text to count lines in

    Returns:
        The number of lines
    """
    if not text:
        return 0
    return text.count('\n') + 1


if __name__ == "__main__":
    mcp.run()
