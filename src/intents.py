"""Suite of utilities to build & train Intents."""

from typing import List

from wit import Wit


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
