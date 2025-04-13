# Directory: PIIAgenticSystem/cognitive_layer
# File: pii_unmasker.py

from agno.agent import Agent
import re

class PIIUnmaskingAgent(Agent):
    def __init__(self, mongo_handler):
        super().__init__(
            name="PII Unmasking Agent",
            role="Restores original PII values using stored mappings from MongoDB.",
            instructions=["Input: Masked text and collection ID", "Output: Fully unmasked original text"]
        )
        self.mongo_handler = mongo_handler

    def run(self, collection_id: str, masked_text: str) -> str:
        unmasked_text = masked_text
        masked_values = set(re.findall(r'<[^>\s]+>', masked_text))
        sorted_tokens = sorted(masked_values, key=len, reverse=True)

        for full_token in sorted_tokens:
            token = full_token.strip("<>").strip()
            original_value = self.mongo_handler.retrieve_mapping_with_id(collection_id, token)
            if original_value:
                pattern = re.escape(full_token)
                unmasked_text = re.sub(pattern, original_value, unmasked_text)

        return unmasked_text
