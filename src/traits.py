"""Suite of utilities to build & train traits."""

from wit import Wit


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


def build_trait(component_type, item, trait_value):

    sub_value = trait_value
    if item == "venue":
        sub_value = convert_venue_trait(trait_value)

    trait = {
        f"{component_type}_{item}": sub_value,
        "list_of_traits": [{"trait": item, "value": trait_value}],
    }
    return trait


def convert_venue_trait(trait_value: str) -> str:

    trait_value = trait_value.replace("_", " ").title()
    return trait_value
