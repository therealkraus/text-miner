# Standard imports

# Related third party imports

# Local application/library specific imports
from text_miner.services import PDFExtractor, TextMiner, create_words_frequency


def extract_text(
    files: list[tuple[str, bytes]]
) -> tuple[list[dict[str, str]], dict[str, str]]:
    """Extract text from PDF files and return the frequency of words and bigrams.

    Args:
        files (list[tuple[str, bytes]]): A list of tuples containing the filename and the file content.

    Returns:
        tuple[list[dict[str, str]], dict[str, str]]: A tuple containing the results and errors.

    Examples:
        >>> files = [("file1.pdf", b"file1 content"), ("file2.pdf", b"file2 content")]
        >>> extract_text(files)
        ([{"word": "example", "frequency": 1}, {"word": "text", "frequency
        ": 2}], {})
    """

    results: list[dict[str, str]] = []
    errors: dict[str, str] = {}

    for filename, file in files:
        try:
            text_extractor = PDFExtractor(file)
            extracted_words = text_extractor.extract_words()

            text_miner = TextMiner(extracted_words)
            data = text_miner.mine()

            result = create_words_frequency(data, filename)
            results.extend(result)

        except Exception as e:
            errors[filename] = str(e)

    return results, errors
