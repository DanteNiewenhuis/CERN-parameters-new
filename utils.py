from variables import compression_types


def is_valid_compression(compression_type: str) -> bool:
    if compression_type in compression_types:
        return True
    return False


def convertToByte(value: int, form: str = "b") -> int:
    """Convert value to byte, kilobyte, or megabyte

    Args:
        value (int)
        form (str, optional): The desired output. Defaults to "b".

    Returns:
        int
    """
    if form == "b" or form == "B":
        return value

    if form == "kb" or form == "KB":
        return value * 1024

    if form == "mb" or form == "MB":
        return value * 1_048_576
