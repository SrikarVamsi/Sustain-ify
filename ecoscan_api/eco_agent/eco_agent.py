from fastapi import APIRouter, Depends, status, HTTPException, Body, UploadFile, File
from typing import List

# from .models import PreNatalQuery

from wrapper import getOutPutInFormat, tavilySearch, model_pro, model, typeDocInputNOutputFormat
from .output_structure import EdibleDataExtraction, EnviromentalProsAndCons, HealthProsAndCons

from .prompts import product_description_template, web_searching_template, enviromental_suggestions

from report_analysis_and_storage import firebase_helper


router = APIRouter(
    prefix="/eco-agent",
    tags=['Eco-Friendly Suggestions']
)

@router.get('/test')
def testRouter():
    return {"Prenatal - API Router Test": "Works like a Charm!!!"}

@router.post('/product-details')
async def describeProducts(userMedicalAilments: str, file: UploadFile = File(...)):
    # try:
    file_content = await file.read()

    with open('/Users/macromrit/Documents/Rcube-Sustainify/media/videos/sunnyD.mp4', 'wb') as jammer:
        jammer.write(file_content)

    product_details = eval(typeDocInputNOutputFormat(model, product_description_template, EdibleDataExtraction, '/Users/macromrit/Documents/Rcube-Sustainify/media/videos/sunnyD.mp4'))

    search_queries = eval(getOutPutInFormat(model,web_searching_template.render(
            product_name = product_details["product_name"],
            product_appereance = product_details["product_appearance"],
            product_description = product_details["product_description"],
            manufacturing_location = product_details["manufacturing_location"],
            ingridients_used = product_details["ingridients_used"],
    ), [], list[str]))

    # taking reference by visiting links related to web queries made ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    context = []
    for query in search_queries:
        print(query)
        context.extend(tavilySearch(query))

    context = '\n\n'.join(context)

    # generating review - env
    pros_and_cons_enviromental = eval(getOutPutInFormat(model, enviromental_suggestions.render(
        product_name = product_details["product_name"],
        product_appereance = product_details["product_appearance"],
        product_description = product_details["product_description"],
        manufacturing_location = product_details["manufacturing_location"],
        ingridients_used = product_details["ingridients_used"],
        web_scraped_info = context
    ), [], EnviromentalProsAndCons))

    # generating review - health
    pros_and_cons_health = eval(getOutPutInFormat(model, enviromental_suggestions.render(
        product_name = product_details["product_name"],
        product_description = product_details["product_description"],
        ingridients_used = product_details["ingridients_used"],
        allergen_information = product_details["allergen_information"],
        cautions_and_warnings = product_details["cautions_and_warnings"],
        user_medical_ailments = userMedicalAilments,
        user_medical_report_details = '\n\n'.join(firebase_helper.retrieve_data_by_keyword('Om123'))
    ), [], HealthProsAndCons))

    product_details['enviromental pros and cons'] = pros_and_cons_enviromental
    product_details['health pros and cons'] = pros_and_cons_health

    # product_details["nutritional_information"] = dict([[j.str ip() for j in i.split(':')] for i in product_details["nutritional_information"]])
#       "nutritional_information": [
#     "Calories 90",
#     "Total Fat 0g",
#     "Saturated Fat 0g",
#     "Trans Fat 0g",
#     "Cholesterol 0mg",
#     "Sodium 240mg",
#     "Total Carbohydrate 23g",
#     "Dietary Fiber 0g",
#     "Total Sugars 22g",
#     "Includes 19g Added Sugars",
#     "Protein 0g",
#     "Vitamin C 130%",
#     "Thiamin 20%"
#   ],

    return product_details

    # except:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

# @router.post('/prenatal_advice')
# def prenatalAdvice(userInput: PreNatalQuery = Body(...)):

#     user_input = dict(
#         # MOM Inputs
#         mom_age = userInput.mom_query.PhysiologicalQueries.age,
#         mom_menstrual_history = userInput.mom_query.PhysiologicalQueries.mestrual_history,
#         mom_health_conditions = userInput.mom_query.PhysiologicalQueries.health_conditions,
#         mom_prev_complications = userInput.mom_query.PhysiologicalQueries.complications_in_prev_pregnancy,
#         mom_medications = userInput.mom_query.PhysiologicalQueries.medications,
#         mom_reproductive_health = userInput.mom_query.BiologicalQueries.present_reproductive_health,
#         mom_diet_type = userInput.mom_query.BiologicalQueries.diet_type,
#         mom_life_style = userInput.mom_query.BiologicalQueries.life_style,
#         mom_family_history_pregnancy_issue = userInput.mom_query.BiologicalQueries.family_history_of_pregnancy_issues,
#         mom_genetic_conditions = userInput.mom_query.BiologicalQueries.any_genetic_conditions,
#         mom_yearly_renumeration = userInput.mom_query.EnviromentalAndEmotionalQueries.renumeration_made_a_year,
#         mom_nationality = userInput.mom_query.EnviromentalAndEmotionalQueries.nationality,
#         mom_current_place_of_living = userInput.mom_query.EnviromentalAndEmotionalQueries.current_place_of_living,
#         mom_married = userInput.mom_query.EnviromentalAndEmotionalQueries.is_2_be_dad_husband,
#         mom_emotional_readiness = userInput.mom_query.EnviromentalAndEmotionalQueries.are_you_emotionally_ready,
#         mom_partner_understanding = userInput.mom_query.EnviromentalAndEmotionalQueries.level_of_understanding_with_partner,
#         mom_access_to_prenatal_care = userInput.mom_query.EnviromentalAndEmotionalQueries.has_access_to_prenatal_care,
#         mom_access_to_care_givers = userInput.mom_query.EnviromentalAndEmotionalQueries.has_access_to_care_givers_for_baby,

#         # DAD Inputs
#         dad_age = userInput.dad_query.PhysiologicalQueries.age,
#         dad_health_conditions = userInput.dad_query.PhysiologicalQueries.health_conditions,
#         dad_sexual_health = userInput.dad_query.PhysiologicalQueries.sexual_health,
#         dad_fertility_history = userInput.dad_query.PhysiologicalQueries.fertility_history,
#         dad_medications = userInput.dad_query.PhysiologicalQueries.medications,
#         dad_reproductive_health = userInput.dad_query.BiologicalQueries.present_reproductive_health,
#         dad_diet_type = userInput.dad_query.BiologicalQueries.diet_type,
#         dad_life_style = userInput.dad_query.BiologicalQueries.life_style,
#         dad_genetic_conditions = userInput.dad_query.BiologicalQueries.any_genetic_conditions_or_family_history_of_reproductive_issue,
#         dad_yearly_renumeration = userInput.dad_query.EnviromentalAndEmotionalQueries.renumeration_made_a_year,
#         dad_nationality = userInput.dad_query.EnviromentalAndEmotionalQueries.nationality,
#         dad_current_place_of_living = userInput.dad_query.EnviromentalAndEmotionalQueries.current_place_of_living,
#         dad_married = userInput.dad_query.EnviromentalAndEmotionalQueries.is_2_be_mom_wife,
#         dad_emotional_readiness = userInput.dad_query.EnviromentalAndEmotionalQueries.are_you_emotionally_ready,
#         dad_partner_understanding = userInput.dad_query.EnviromentalAndEmotionalQueries.level_of_understanding_with_partner,
#     )

    
#     # generating web search queries ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     web_search_result = web_searching_template.render(
#         user_input        
#     )
#     search_queries = eval(getOutPutInFormat(model_pro, web_search_result, [], list[str]))
#     # print(search_queries)

#     # taking reference by visiting links related to web queries made ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     context = []
#     for query in search_queries:
#         print(query)
#         context.extend(tavilySearch(query))
#     # print(context)

#     # generating pros and cons and improvements to make ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     user_input.update({"relevant_contexts": context})
#     advice_query = prenatal_template.render(user_input)
#     # print(advice_query)
#     final_output = eval(getOutPutInFormat(model_pro, advice_query, [], FinalAdvice))


#     # generating plots ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     del user_input["relevant_contexts"]
#     plot_scores_query = evaluation_template.render(user_input)
#     plot_output = eval(getOutPutInFormat(model_pro, plot_scores_query, [], BarPlot))

#     final_output['scores_for_plot'] = plot_output

#     print(final_output)

#     return final_output
#     # return hello()







# if __name__ == "__main__":
#     from wrapper import *
#     from .output_structure import FinalAdvice, BarPlot

#     sample_inputs = dict(
#         # MOM Inputs
#         mom_age = 28,
#         mom_menstrual_history = 'Regular periods, no significant issues.',
#         mom_health_conditions = 'Mild allergies to pollen and dust.',
#         mom_prev_complications = None,
#         mom_medications = 'None currently, but was on antibiotics for a sinus infection last year.',
#         mom_reproductive_health = 'Regular menstrual cycles, no birth control currently.',
#         mom_diet_type = 'Vegetarian',
#         mom_life_style = 'Does not smoke, drink alcohol occasionally, no drug use.',
#         mom_family_history_pregnancy_issue = 'No history of pregnancy complications or genetic disorders.',
#         mom_genetic_conditions = None,
#         mom_yearly_renumeration = 50_000,
#         mom_nationality = 'Indian',
#         mom_current_place_of_living = 'Chennai, Tamil Nadu, India',
#         mom_married = "Yes",
#         mom_emotional_readiness = 'Excited and prepared to start a family',
#         mom_partner_understanding = 'Strong communication and mutual support',
#         mom_access_to_prenatal_care = True,
#         mom_access_to_care_givers = True,

#         # DAD Inputs
#         dad_age = 30,
#         dad_health_conditions = None,
#         dad_sexual_health = 'Healthy and active',
#         dad_fertility_history = 'No known issues',
#         dad_medications = None,
#         dad_reproductive_health = 'Healthy and active',
#         dad_diet_type = 'Omnivore',
#         dad_life_style = 'Does not smoke, drinks alcohol occasionally, no drug use',
#         dad_genetic_conditions = None,
#         dad_yearly_renumeration = 65_000,
#         dad_nationality = 'Indian',
#         dad_current_place_of_living = 'Chennai, Tamil Nadu, India',
#         dad_married = True,
#         dad_emotional_readiness = 'Excited and supportive of starting a family',
#         dad_partner_understanding = 'Strong communication and mutual support',
#     )

#     # generating web search queries ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     web_search_result = web_searching_template.render(
#         sample_inputs        
#     )
#     search_queries = eval(getOutPutInFormat(model_pro, web_search_result, [], list[str]))
#     # print(search_queries)

#     # taking reference by visiting links related to web queries made ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     context = []
#     for query in search_queries:
#         print(query)
#         context.extend(tavilySearch(query))
#     # print(context)

#     # generating pros and cons and improvements to make ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     sample_inputs.update({"relevant_contexts": context})
#     advice_query = prenatal_template.render(sample_inputs)
#     # print(advice_query)
#     final_output = eval(getOutPutInFormat(model_pro, advice_query, [], FinalAdvice))


#     # generating plots ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#     del sample_inputs["relevant_contexts"]
#     plot_scores_query = evaluation_template.render(sample_inputs)
#     plot_output = eval(getOutPutInFormat(model_pro, plot_scores_query, [], BarPlot))

#     final_output['scores_for_plot'] = plot_output

#     print(final_output)


