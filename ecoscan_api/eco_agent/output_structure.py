import enum
from typing_extensions import TypedDict


class EdibleDataExtraction(TypedDict):
    product_name: str
    product_description: str
    ingridients_used: list[str]
    nutritional_information: list[str]
    allergen_information: list[str]
    cautions_and_warnings: list[str]
    manufacturing_location: str
    product_appearance: str

class HealthProsAndCons(TypedDict):
    positive_things_about_the_product: list[str]
    harmful_things_about_the_product: list[str]

class EnviromentalProsAndCons(TypedDict):
    positive_things_about_the_product: list[str]
    harmful_things_about_the_product: list[str]
    alternatives_to_consider: list[str]

class HealthProsAndCons(TypedDict):
    positive_things_about_the_product: list[str]
    harmful_things_about_the_product: list[str]
    alternatives_to_consider: list[str]