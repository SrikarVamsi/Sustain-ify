from pydantic import BaseModel
from typing import Union


# # Inputs for the enviromental thing
# class PhysiologicalMom(BaseModel):
#     age: int
#     mestrual_history: str # answers to like are your menstrual cycles regular and cycle duration. Whether PMS or PMDD is experienced
#     health_conditions: Union[str, None] # B.P, Diabetes and more like that
#     complications_in_prev_pregnancy: Union[str, None] # If had one before
#     medications: Union[str, None]