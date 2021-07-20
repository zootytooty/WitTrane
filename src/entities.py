"""Suite of utilities to build & train entities."""

from typing import List

import re

from wit import Wit


def create_entities(wit_client: Wit, entities: List[str]) -> None:

    existing_entities = [x["name"] for x in wit_client.entity_list()]

    # Wit has some dumb instances where the entity it returns & what you must send aren't quite the same
    # This maps between the two
    weird_wit_entities = {
        "wit$datetime:datetime": "wit$datetime",
    }

    # Definitely can be done more efficiently
    entities_to_create = [x for x in entities if x not in existing_entities]
    entities_to_skip = [x for x in entities if x in existing_entities]

    for entity in entities:
        if entity in weird_wit_entities:
            if weird_wit_entities[entity] in existing_entities:
                entities_to_create.remove(entity)
                entities_to_skip.append(weird_wit_entities[entity])

    print(f"Skipping intents as they already exist: {entities_to_skip}")

    for entity in entities_to_create:
        try:
            print(f"Creating: {entity}")
            wit_client.create_entity(entity, [entity])
            print(f"Intent '{entity}' created")
        except Exception as ex:
            print(f"Unable to create: {entity}")
            print(ex)


def build_entity(component_type, item, entity_value):

    entity = {
        f"{component_type}_{item}": entity_value,
        "list_of_entities": [{"entity": item, "body": entity_value, "entities": []}],
    }
    return entity


def assign_entity_start_end(utterrance_object: dict) -> None:
    for x in utterrance_object["entities"]:
        matches = re.search(rf"\b({x['body']})\b", utterrance_object["text"])
        if matches:
            x.update(start=matches.start(), end=matches.end())
