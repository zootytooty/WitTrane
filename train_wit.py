"""Train Wit.

Parses the values provided in the config to create intents, entities, traits &
 ultimately utterances based on them.
"""

import os
from time import sleep

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
    create_intents(client, list(config["intents"].keys()))
    create_traits(client, config["traits"])
    create_entities(client, list(config["entities"].keys()))

    # Build each utterance sequence & train wit on them
    for intent in config["intents"]:
        print(f"Training utterances for intent: {intent}")
        for utterance in config["intents"][intent]:
            new_utterances = permute_utterance(utterance, intent, config)

            if len(new_utterances) >= 200:
                # Wit has a rate limit of 200 utterances per minute, so we'll chunk and go slow
                new_utterances_chunks = chunks(new_utterances, 200)
                for chunk in new_utterances_chunks:
                    client.train(chunk)
                    sleep(61)  # an extra second just cos
            else:
                client.train(new_utterances)
                sleep(61)  # an extra second just cos
