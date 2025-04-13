# Directory: PIIAgenticSystem/cognitive_layer
# File: pii_masker.py

from agno.agent import Agent
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.predefined_recognizers import SpacyRecognizer
from flair.models import SequenceTagger
from flair.data import Sentence
import re
import random
import uuid

class PIIMaskingAgent(Agent):
    def __init__(self, mongo_handler):
        super().__init__(
            name="PII Masking Agent",
            role="Detects and masks PII using Presidio, Flair, and Regex, and stores original values in MongoDB.",
            instructions=["Input: Raw text", "Output: Masked text with collection ID"]
        )
        self.mongo_handler = mongo_handler
        self.analyzer = AnalyzerEngine()
        self.analyzer.registry.add_recognizer(SpacyRecognizer())
        self.flair_model = SequenceTagger.load("flair/ner-english-large")
        self.generated_masked_values = set()

        self.ADDRESS_REGEX_US = r"""
            \b\d{1,5}\s+[A-Za-z0-9\s.,]+(?:(?:\s*(?:Apt|Apartment|Suite|Unit)\s*\d+[A-Za-z]*))?\s*,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b
        """
        address_recognizer_us = PatternRecognizer(
            supported_entity="HOME_ADDRESS",
            patterns=[Pattern(name="address_us", regex=self.ADDRESS_REGEX_US, score=0.95)]
        )
        self.analyzer.registry.add_recognizer(address_recognizer_us)

    def _generate_unique_collection_id(self):
        while True:
            new_id = str(uuid.uuid4())
            if not self.mongo_handler.does_collection_id_exist(new_id):
                return new_id

    def _generate_unique_masked_value(self, entity_type: str, prefix: str) -> str:
        for _ in range(100):
            masked_value = f"<{prefix}_{entity_type}_{random.randint(1000, 9999)}>"
            if masked_value not in self.generated_masked_values:
                self.generated_masked_values.add(masked_value)
                return masked_value
        raise Exception("Failed to generate unique masked value after 100 attempts.")

    def run(self, text: str) -> str:
        collection_id = self._generate_unique_collection_id()
        results = self.analyzer.analyze(text=text, entities=["PERSON", "HOME_ADDRESS"], language='en')
        flair_sentence = Sentence(text)
        self.flair_model.predict(flair_sentence)

        masked_text = text
        mappings = {}

        for res in results:
            if res.score > 0.6:
                original_value = text[res.start:res.end]
                masked_value = self._generate_unique_masked_value(res.entity_type, "PRESIDIO")
                mappings[original_value] = masked_value
                self.mongo_handler.store_mapping_with_id(collection_id, masked_value, original_value)

        for entity in flair_sentence.get_spans('ner'):
            if entity.tag in ["PER", "LOC"]:
                original_value = entity.text
                if original_value not in mappings:
                    masked_value = self._generate_unique_masked_value(entity.tag, "FLAIR")
                    mappings[original_value] = masked_value
                    self.mongo_handler.store_mapping_with_id(collection_id, masked_value, original_value)

        regex_patterns = {
            "CARD": r"\b(?:\d[ -]*?){13,16}\b",
            "EXPIRY": r"\b(0[1-9]|1[0-2])/(\d{2})\b",
            "CVV": r"(?<!\d)\d{3}(?!\d)",
            "PASSWORD": r"(?i)password[=: ]*[^\s]+",
            "NATIONAL_ID": r"\b\d{10,14}\b",
            "PHONE": r"\+\d{1,3}[\s-]?\d{3,4}[\s-]?\d{3,4}\b",
            "DOB": r"\b\d{2}/\d{2}/\d{4}\b",
            "PASSPORT": r"\b[A-Z]{1,2}\d{6,9}\b",
            "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        }

        for key, pattern in regex_patterns.items():
            for match in re.finditer(pattern, masked_text):
                original_value = match.group(0)
                if original_value not in mappings:
                    masked_value = self._generate_unique_masked_value(key, "REGEX")
                    mappings[original_value] = masked_value
                    self.mongo_handler.store_mapping_with_id(collection_id, masked_value, original_value)

        for original, masked in mappings.items():
            masked_text = re.sub(re.escape(original), masked, masked_text)

        return collection_id + "\n" + masked_text
