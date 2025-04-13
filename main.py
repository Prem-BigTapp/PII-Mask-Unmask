# Directory: AGNO-PII-FINAL
# File: main.py (Entry Point)

from cli_input_handler import get_input
from file_handler import FileHandler
from pii_masker import PIIMaskingAgent
from pii_unmasker import PIIUnmaskingAgent
from mongo_storage import MongoHandler
from config import Config
from agno.agent import Agent  # Import Agno agent base

def main():
    config = Config()
    mongo_handler = MongoHandler(config)
    file_handler = FileHandler()

    mode, path = get_input()

    if mode == 'm':
        text = file_handler.get_text_from_file(path)
        if not text:
            print("\u274c Failed to read input file.")
            return
        masker_agent = PIIMaskingAgent(mongo_handler)
        result = masker_agent.run(text)
        print("\n\u2705 Masked Result:\n" + result)

    elif mode == 'u':
        cid = input("Enter the collection ID: ").strip()
        masked_text = file_handler.get_text_from_file(path)
        if not masked_text:
            print("\u274c Failed to read masked input file.")
            return
        unmasker_agent = PIIUnmaskingAgent(mongo_handler)
        result = unmasker_agent.run(cid, masked_text)
        print("\n\u2705 Unmasked Result:\n" + result)

    else:
        print("Invalid mode selected. Choose [M] or [U].")

if __name__ == "__main__":
    main()
