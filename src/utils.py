"""Suite of general utilities."""

from itertools import chain
from operator import methodcaller
from typing import List

from traits import build_trait
from entities import build_entity


def extract_component(
    component_list: list, component_type: str, separator: str = "_"
) -> List[str]:

    all_components = [
        x.replace(f"{component_type}{separator}", "")
        for x in component_list
        if x.startswith(component_type)
    ]

    # If duplicates present, return only unique items
    return list(set(all_components))


def component_substitute_values(
    component_type: str, components: list, config: dict
) -> List[dict]:

    # Validate Request is valid
    if not set(components).issubset(set(config.get(component_type).keys())):
        unknown_values = set(components) - set(config.get(component_type).keys())
        raise ValueError(
            f"Unknown {component_type} values present. {unknown_values} are not present in the config. Acceptable values are {set(config.get(component_type).keys())}"
        )

    component_substitues = list()

    if component_type == "traits":
        for item in components:
            component_substitues.append(
                [
                    build_trait(component_type, item, x)
                    for x in config.get(component_type).get(item)
                ]
            )
    elif component_type == "entities":
        for item in components:
            component_substitues.append(
                [
                    build_entity(component_type, item, x)
                    for x in config.get(component_type).get(item)
                ]
            )

    return component_substitues


def create_value(utterance_items: tuple) -> dict:
    vals = {}
    dict_items = map(methodcaller("items"), utterance_items)
    for k, v in chain.from_iterable(dict_items):
        if k in vals:
            vals[k] = vals[k] + v
        else:
            vals[k] = v
    return vals


def chunks(lst: list, n: int) -> list:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
