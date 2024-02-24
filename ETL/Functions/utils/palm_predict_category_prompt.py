import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai_api_key = os.environ.get("genai_api_key")

genai.configure(api_key=genai_api_key)

for m in genai.list_models():
  if 'generateText' in m.supported_generation_methods:
    print(m.name)

def predict_category_prompt(title, description):
    models = [m for m in genai.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name

    prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
    Out of the above categories, determine the category below news' title and description belongs to.
    Title: {title}
    Description: {description}
    Response should contain only one word ie, <category>.
    Example Response: Technology
    None is not an option.
    Note: Anything that involves government bodies and similar news belongs to nation.'''

    safety_settings=[
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_DEROGATORY,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_TOXICITY,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },        
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_VIOLENCE,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },        
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_SEXUAL,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },        
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_MEDICAL,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },        
        {
            "category": genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS,
            "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
        },
    ]

    completion = genai.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.99,
        max_output_tokens=1,
        safety_settings=safety_settings
    )
    category = completion.result or None
    return category

title = "Man thrashed and sexually assaulted in Delhi; police arrest 2"
description = "The incident took place on Diwali night when the complainant and the family of the accused were celebrating the festival."
print(predict_category_prompt(title, description))