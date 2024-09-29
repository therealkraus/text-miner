# Standard imports

# Related third party imports

# Local application/library specific imports
from text_miner.services import PDFExtractor, TextMiner, create_words_frequency


def extract_text(
    files: list[tuple[str, bytes]]
) -> tuple[list[dict[str, str]], dict[str, str]]:
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
