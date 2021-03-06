"""Train Wit.

Parses the values provided in the config to create intents, entities, traits &
 ultimately utterances based on them.
"""

import os
from time import sleep

from tqdm import tqdm
import yaml
from wit import Wit

from src.traits import create_traits
from src.intents import create_intents
from src.entities import create_entities
from src.utterances import permute_utterance
from src.utils import chunks


config = yaml.safe_load(open("wit_training_config.yaml"))


if __name__ == "__main__":
    client = Wit(os.getenv("WIT_TOKEN"))

    # First define the core attributes required
    if "intents" in config and config.get("intents") is not None:
        create_intents(client, list(config["intents"].keys()))
    
    if "traits" in config and config.get("traits") is not None:
        create_traits(client, config["traits"])

    if "entities" in config and config.get("entities") is not None:
        create_entities(client, list(config["entities"].keys()))

    # Build each utterance sequence & train wit on them
    new_utterances = []
    for intent in config["intents"]:
        print(f"Training utterances for intent: {intent}")
        for utterance in config["intents"][intent]:
            new_utterances.extend(permute_utterance(utterance, intent, config))

    # Wit has a rate limit of 200 utterances per minute, so we'll chunk and go slow if needed
    if len(new_utterances) >= 200:
        new_utterances_chunks = chunks(new_utterances, 200)
        for chunk in tqdm(new_utterances_chunks):
            client.train(chunk)
            sleep(61)  # an extra second just cos
    else:
        client.train(new_utterances)
        sleep(61)  # an extra second just cos
