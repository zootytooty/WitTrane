"""Train Wit.

Parses the values provided in the config to create intents, entities, traits &
 ultimately utterances based on them.
"""

#%%
import os
from typing import List

import yaml
from wit import Wit

config = yaml.safe_load(open("config.yaml"))


#%%
def create_intents(wit_client: Wit, intents: List[str]) -> None:
    """Creates Wit Intents.

    Args:
        wit_client (Wit): Instantiated Wit Client
        intents (List[str]): All intents to be created.
    """
    existing_intents = [x["name"] for x in wit_client.intent_list()]
    # Definitely can be done more efficiently
    intents_to_create = [x for x in intents if x not in existing_intents]
    intents_to_skip = [x for x in intents if x in existing_intents]

    print(f"Skipping intents as they already exist: {intents_to_skip}")

    for intent in intents_to_create:
        try:
            print(f"Creating: {intent}")
            wit_client.create_intent(intent)
            print(f"Intent '{intent}' created")
        except Exception as ex:
            print(f"Unable to create: {intent}")
            print(ex)


#%%
def create_traits(wit_client: Wit, traits: dict) -> None:
    """Create Wit Traits.

    Args:
        wit_client (Wit): Instantiated Wit Client
        traits (List[dict]): Each dict should have a key for
    """

    existing_traits = [x["name"] for x in wit_client.trait_list()]
    for trait in traits:
        print(f"Creating Trait: {trait}")

        # Traits can be added by sending new values one by one but for
        # simplicities (and possibly speeds) sake, drop the existing verion
        #  & totally replace it
        if trait in existing_traits:
            print(f"Trait '{trait}' already exists. Removing existing values")
            wit_client.delete_trait(trait)

        wit_client.create_trait(trait_name=trait, values=traits[trait])


#%%
if __name__ == "__main__":
    client = Wit(os.getenv("WIT_TOKEN"))

    create_intents(client, config["intents"])
    create_traits(client, config["traits"])
