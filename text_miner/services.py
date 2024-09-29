# Standard imports
import collections
import io
import re
from abc import ABC, abstractmethod

# Related third party imports
import nltk
from nltk.corpus import stopwords
import pdfplumber


# Local application/library specific imports


nltk.download("stopwords")


class TextExtactor(ABC):
    def __init__(self, file: bytes):
        self.file = file

    @abstractmethod
    def extract_words(self):
        """Subclasses must implement this method."""
        pass


class PDFExtractor(TextExtactor):
    def extract_words(self) -> list[str]:
        extracted_words: list[str] = []

        with pdfplumber.open(io.BytesIO(self.file)) as pdf:
            for page in pdf.pages:
                words = page.extract_words(
                    **{
                        "x_tolerance": 5,
                        "y_tolerance": 3,
                    }
                )
                for word in words:
                    text = word["text"]
                    assert isinstance(text, str)
                    extracted_words.append(text)

        return extracted_words


class TextMiner:
    def __init__(self, words: list[str]):
        self.words = words

    def mine(self) -> list[str]:
        words = self._sanitize_words(self.words)
        words = self._remove_stopwords(words)

        bigrams = self._get_bigrams(words)

        if not words and not bigrams:
            return []

        return words + bigrams

    def _sanitize_words(self, words: list[str]) -> list[str]:
        sanitized_words: list[str] = []

        for word in words:
            sanitized_word = re.sub("[^A-Za-z]+", " ", word).lower().strip().split()
            sanitized_words.extend(sanitized_word)

        return sanitized_words

    def _get_bigrams(self, words: list[str]) -> list[str]:
        bigrams = list(nltk.bigrams(words))
        return [" ".join(bigram) for bigram in bigrams if bigram[0] != bigram[1]]

    def _remove_stopwords(self, words: list[str]) -> list[str]:
        stop_words = set(stopwords.words("english"))
        return [word for word in words if word not in stop_words]


def create_words_frequency(words: list[str], filename: str) -> list[dict[str, str]]:
    results = []

    counter = collections.Counter(words)

    for word, frequency in counter.items():
        result = {}

        result["filename"] = filename
        result["word"] = word
        result["frequency"] = frequency

        results.append(result)

    return results
