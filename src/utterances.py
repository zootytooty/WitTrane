"""Suite of utilities to build & train utterances."""

from itertools import product
from re import compile, findall
from typing import List

from utils import extract_component, component_substitute_values, create_value
from entities import assign_entity_start_end


def permute_utterance(utterance: str, intent: str, config: dict) -> List[dict]:

    # 1. Identify traits & entities required to build the utterances
    entities_and_traits = extract_entities_and_traits(utterance)
    traits = extract_component(entities_and_traits, "traits")
    entities = extract_component(entities_and_traits, "entities")

    # 2. For each trait & entity required, build the values' representation
    trait_values = component_substitute_values("traits", traits, config)
    entity_values = component_substitute_values("entities", entities, config)

    # 3. Collect all possible groupings that can be used to build the utterance
    iterable_items = trait_values + entity_values
    template_values = [create_value(x) for x in product(*iterable_items)]

    # 4. Build the POST payload for each permutation of the utterance
    new_utterances = []
    for template_value in template_values:

        new_utterances.append(
            {
                "text": format_utterance(utterance, template_value),
                "intent": intent,
                "entities": template_value.get("list_of_entities", []),
                "traits": template_value.get("list_of_traits", [])
            }
        )

    # 5. For each new utterance, calculate the position for each subbed entity
    _ = [assign_entity_start_end(x) for x in new_utterances]

    return new_utterances


def extract_entities_and_traits(utterance: str) -> List[str]:

    # Extract all text between the curly braces
    # This could be a risk if someone provides dodgy samples but it'll do for now
    pattern = compile(r"\{(.*?)\}")
    return findall(pattern, utterance)


def format_utterance(utterance: str, format_values: dict) -> str:

    matches_to_replace = extract_entities_and_traits(utterance)

    for match in matches_to_replace:
        match_string = "{" + match + "}"
        utterance = utterance.replace(match_string, format_values.get(match))

    return utterance
