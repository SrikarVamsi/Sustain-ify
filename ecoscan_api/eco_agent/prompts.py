# refer to -> https://console.cloud.google.com/vertex-ai/studio/prompt-gallery?project=intricate-dryad-435706-f4
from jinja2 import Template


# EDIBLE
product_description_template = """
You are a professional Product Describer. 
Your task is to provide a detailed description of the product shown in the attached video. 
Extract all the nutritional information as key-value pairs('Name: value'), list the ingredients and return as a python list, allergen information as a python list, cautions as a python list, warnings, and the manufacturing location as a string. 
Generate a description of the product's appearance, such as the container it is in, whether its made of plastic, the bottle, or other details.
Additionally, provide a clear and concise overall description of the product.
"""

# PROS and CONS IN TERMS OF ENVIRONMENT
enviromental_suggestions = Template("""
You are an Enviromental Product Analyst, Refer to the product description and list out atleast 3 points each
about the positives and negatives of the product to the enviroment and sustainability as seperate python lists of strings being points.
You can also suggest few other alternatives to create a good impact.

PRODUCT DETAILS:
product's name: {{product_name}}.
product's appearance: {{product_appereance}}.
product's description: {{product_description}}.
product's manufacturing location: {{manufacturing_location}}.
ingridients used in manufacturing the product: {{ingridients_used}}.

MORE DETAILS ABOUT THE MANUFACTURING PROCESS AND THE CARBON FOOTPRINT ASSOCIATED WITH THE PRODUCT:
{{web_scraped_info}}

RESPONSE:
""")

# PROS and CONS IN TERMS OF HEALTH

health_suggestions = Template("""
You are an Health Product Analyst, Refer to the product description and list out atleast 3 points each
about the positives and negatives of the product related to health factors as seperate python lists of strings being points.
You can also suggest few other alternatives to have a good health life. 
Data from a few user medical report's have been attached too

PRODUCT DETAILS:
product's name: {{product_name}}.
product's description: {{product_description}}.
ingridients used in manufacturing the product: {{ingridients_used}}.
product's allergen information: {{allergen_information}}.
product's cautions and warnings: {{cautions_and_warnings}}.

USER MEDICAL AILMENTS: {{user_medical_ailments}}                    

USER MEDICAL REPORT DETAILS:
{{user_medical_report_details}}

RESPONSE:
""")



web_searching_template = Template(
    """
You are a professional web-search query writer, you are tasked to write web queries to get more details, such as the manufacturing process, Carbon Footprint and other enviromental factors associated with it.
You can craft queries based on the product's description given. The webqueries will be posed to a browser and results will be taken as refernce.

generate 4 web-queries. The output should be a python list of strings.

PRODUCT DESCRIPTION:
    product's name: {{product_name}}.
    product's appearance: {{product_appereance}}.
    product's description: {{product_description}}.
    product's manufacturing location: {{manufacturing_location}}.
    ingridients used in manufacturing the product: {{ingridients_used}}.

WEB QUERIES:
"""
)


prenatal_template = Template(
    """
You are a pregnancy Advisor, you are tasked to recommend couples to whether have a baby or not based on responses to a few questions
given to to-be mom and dad. Based on the given responses and other relevant contexts from the web, your task is to list out the reasons for
why to have a baby and why not to. Also provide advice on how to overcome/resolve issues, if any exists.

The output is expected to be python list of strings with reasons in them supporting why to have a baby, why not to have a baby and improvements or steps to take to increase the chances of having a baby

relevant_context:
    {% for context in relevant_contexts %}
    {{context}}
    {% endfor %}

Questions asked to to-be-Mom and the Responses she gave:
Physiological Questions
q1) Current Age: {{mom_age}}
q2) A few lines about your Menstrual History/Issues, if any: {{mom_menstrual_history}}
q3) Medical Ailments or Conditions you have or have experienced, if any: {{mom_health_conditions}}
q4) A few lines on complications in your previous pregnancy, if any: {{mom_prev_complications}}
q5) Are you under any medication, or have you been under any medication. If so When?: {{mom_medications}}
Biological Questions
q1) A few lines on your current reproductive health: {{mom_reproductive_health}}
q2) Your Diet Type(i.e Vegetarian, Vegan, Non-Vegetarian... etc): {{mom_diet_type}}
q3) Your present life-style(Do you Smoke, Drink or Consume Drugs): {{mom_life_style}}
q4) Do you have a family history of any pregnancy issue?: {{mom_family_history_pregnancy_issue}}
q5) Any genetic conditions to mention?: {{mom_genetic_conditions}}
Enviromental And Emotional Questions
q1) Total Renumeration you make in a year in USD: {{mom_yearly_renumeration}}
q2) Your Nationality: {{mom_nationality}}
q3) Your current place of Living (Country, State and City): {{mom_current_place_of_living}}
q4) Are you married to your partner, who is going to be the dad: {% if mom_married %} Yes {% else %} No {% endif %}
q5) Are you emotinally ready to have a baby? Give a few lines about it.: {{mom_emotional_readiness}}
q6) A Few Lines on your level of understanding and happenings b/w you and your partner: {{mom_partner_understanding}}
q7) Do you have access to prenatal care(like massages, regular check-ups and more.): {% if mom_access_to_prenatal_care %} Yes {% else %} No {% endif %}
q8) Do you have access to care givers to take care of you and the baby after pregnancy: {% if mom_access_to_care_givers %} Yes {% else %} No {% endif %}

Questions asked to to-be-Dad and the Responses he gave:
Physiological Questions
q1) Current Age: {{dad_age}}
q2) Medical Ailments or Conditions you have or have experienced, if any: {{dad_health_conditions}}
q3) A few lines about your Sexual Health and Drive, if any: {{dad_sexual_health}}
q3) A few lines on your fertility history, if any: {{dad_fertility_history}}
q4) Are you under any medication, or have you been under any medication. If so When?: {{dad_medications}}
Biological Questions
q1) A few lines on your current reproductive health: {{dad_reproductive_health}}
q2) Your Diet Type(i.e Vegetarian, Vegan, Non-Vegetarian... etc): {{dad_diet_type}}
q3) Your present life-style(Do you Smoke, Drink or Consume Drugs): {{dad_life_style}}
q4) Any genetic conditions or family history of reproductive issues to mention?: {{dad_genetic_conditions}}
Enviromental And Emotional Questions
q1) Total Renumeration you make in a year in USD: {{dad_yearly_renumeration}}
q2) Your Nationality: {{dad_nationality}}
q3) Your current place of Living (Country, State and City): {{dad_current_place_of_living}}
q4) Are you married to your partner, who is going to be the dad: {% if dad_married %} Yes {% else %} No {% endif %}
q5) Are you emotinally ready to have a baby? Give a few lines about it.: {{dad_emotional_readiness}}
q6) A Few Lines on your level of understanding and happenings b/w you and your partner: {{dad_partner_understanding}}


"""
    )


evaluation_template = Template(
    """
You are a Pregnancy Factor Evaluator, you are tasked to evaluate the answers posed by both to-be mom and
to-be dad, for the questions asked. You score should be out of 10, and scores should be assigned based on 
enviromental, biological and physiological, and emotional factors.

Questions asked to to-be-Mom and the Responses she gave:
Physiological Questions
q1) Current Age: {{mom_age}}
q2) A few lines about your Menstrual History/Issues, if any: {{mom_menstrual_history}}
q3) Medical Ailments or Conditions you have or have experienced, if any: {{mom_health_conditions}}
q4) A few lines on complications in your previous pregnancy, if any: {{mom_prev_complications}}
q5) Are you under any medication, or have you been under any medication. If so When?: {{mom_medications}}
Biological Questions
q1) A few lines on your current reproductive health: {{mom_reproductive_health}}
q2) Your Diet Type(i.e Vegetarian, Vegan, Non-Vegetarian... etc): {{mom_diet_type}}
q3) Your present life-style(Do you Smoke, Drink or Consume Drugs): {{mom_life_style}}
q4) Do you have a family history of any pregnancy issue?: {{mom_family_history_pregnancy_issue}}
q5) Any genetic conditions to mention?: {{mom_genetic_conditions}}
Enviromental And Emotional Questions
q1) Total Renumeration you make in a year in USD: {{mom_yearly_renumeration}}
q2) Your Nationality: {{mom_nationality}}
q3) Your current place of Living (Country, State and City): {{mom_current_place_of_living}}
q4) Are you married to your partner, who is going to be the dad: {% if mom_married %} Yes {% else %} No {% endif %}
q5) Are you emotinally ready to have a baby? Give a few lines about it.: {{mom_emotional_readiness}}
q6) A Few Lines on your level of understanding and happenings b/w you and your partner: {{mom_partner_understanding}}
q7) Do you have access to prenatal care(like massages, regular check-ups and more.): {% if mom_access_to_prenatal_care %} Yes {% else %} No {% endif %}
q8) Do you have access to care givers to take care of you and the baby after pregnancy: {% if mom_access_to_care_givers %} Yes {% else %} No {% endif %}

Questions asked to to-be-Dad and the Responses he gave:
Physiological Questions
q1) Current Age: {{dad_age}}
q2) Medical Ailments or Conditions you have or have experienced, if any: {{dad_health_conditions}}
q3) A few lines about your Sexual Health and Drive, if any: {{dad_sexual_health}}
q3) A few lines on your fertility history, if any: {{dad_fertility_history}}
q4) Are you under any medication, or have you been under any medication. If so When?: {{dad_medications}}
Biological Questions
q1) A few lines on your current reproductive health: {{dad_reproductive_health}}
q2) Your Diet Type(i.e Vegetarian, Vegan, Non-Vegetarian... etc): {{dad_diet_type}}
q3) Your present life-style(Do you Smoke, Drink or Consume Drugs): {{dad_life_style}}
q4) Any genetic conditions or family history of reproductive issues to mention?: {{dad_genetic_conditions}}
Enviromental And Emotional Questions
q1) Total Renumeration you make in a year in USD: {{dad_yearly_renumeration}}
q2) Your Nationality: {{dad_nationality}}
q3) Your current place of Living (Country, State and City): {{dad_current_place_of_living}}
q4) Are you married to your partner, who is going to be the dad: {% if dad_married %} Yes {% else %} No {% endif %}
q5) Are you emotinally ready to have a baby? Give a few lines about it.: {{dad_emotional_readiness}}
q6) A Few Lines on your level of understanding and happenings b/w you and your partner: {{dad_partner_understanding}}
"""
)


# result = prenatal_template.render(name="World")


if __name__ == "__main__":
    from wrapper import *
    from .output_structure import EdibleDataExtraction

    # sample_inputs = dict(
    #     # MOM Inputs
    #     mom_age = 28,
    #     mom_menstrual_history = 'Regular periods, no significant issues.',
    #     mom_health_conditions = 'Mild allergies to pollen and dust.',
    #     mom_prev_complications = None,
    #     mom_medications = 'None currently, but was on antibiotics for a sinus infection last year.',
    #     mom_reproductive_health = 'Regular menstrual cycles, no birth control currently.',
    #     mom_diet_type = 'Vegetarian',
    #     mom_life_style = 'Does not smoke, drink alcohol occasionally, no drug use.',
    #     mom_family_history_pregnancy_issue = 'No history of pregnancy complications or genetic disorders.',
    #     mom_genetic_conditions = None,
    #     mom_yearly_renumeration = 50_000,
    #     mom_nationality = 'Indian',
    #     mom_current_place_of_living = 'Chennai, Tamil Nadu, India',
    #     mom_married = "Yes",
    #     mom_emotional_readiness = 'Excited and prepared to start a family',
    #     mom_partner_understanding = 'Strong communication and mutual support',
    #     mom_access_to_prenatal_care = True,
    #     mom_access_to_care_givers = True,

    #     # DAD Inputs
    #     dad_age = 30,
    #     dad_health_conditions = None,
    #     dad_sexual_health = 'Healthy and active',
    #     dad_fertility_history = 'No known issues',
    #     dad_medications = None,
    #     dad_reproductive_health = 'Healthy and active',
    #     dad_diet_type = 'Omnivore',
    #     dad_life_style = 'Does not smoke, drinks alcohol occasionally, no drug use',
    #     dad_genetic_conditions = None,
    #     dad_yearly_renumeration = 65_000,
    #     dad_nationality = 'Indian',
    #     dad_current_place_of_living = 'Chennai, Tamil Nadu, India',
    #     dad_married = True,
    #     dad_emotional_readiness = 'Excited and supportive of starting a family',
    #     dad_partner_understanding = 'Strong communication and mutual support',
    # )

    # # generating web search queries ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # web_search_result = web_searching_template.render(
    #     sample_inputs        
    # )
    # search_queries = eval(getOutPutInFormat(model_pro, web_search_result, [], list[str]))
    # # print(search_queries)

    # # taking reference by visiting links related to web queries made ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # context = []
    # for query in search_queries:
    #     print(query)
    #     context.extend(tavilySearch(query))
    # # print(context)

    # # generating pros and cons and improvements to make ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # sample_inputs.update({"relevant_contexts": context})
    # advice_query = prenatal_template.render(sample_inputs)
    # # print(advice_query)
    # final_output = eval(getOutPutInFormat(model_pro, advice_query, [], FinalAdvice))


    # # generating plots ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # del sample_inputs["relevant_contexts"]
    # plot_scores_query = evaluation_template.render(sample_inputs)
    # plot_output = eval(getOutPutInFormat(model_pro, plot_scores_query, [], BarPlot))

    # final_output['scores_for_plot'] = plot_output

    # print(final_output)


    