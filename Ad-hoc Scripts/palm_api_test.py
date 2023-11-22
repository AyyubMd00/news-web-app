import google.generativeai as palm
import os

palm_api_key = os.environ.get("palm_api_key")
palm.configure(api_key=palm_api_key)

# print(list(palm.list_models()))

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

title = '''BJP hopes to override caste conflict in Maharashtra by consolidating Hindutva via Ram temple plank'''
description = '''In the state which has been mired in caste cauldron with Marathas seeking reservation within OBC, the right wing party believes that Ayodhya can prove to be an instrumental factor to break the impregnable barriers of caste and communities that threaten to shake the very structure on which Maharashtra is founded.'''

prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
Out of the above categories, determine the category below news' title and description belongs to.
Title: {title}
Description: {description}
Response should contain only one word ie, <category>.
None is not an option.
Note: Anything that involves government bodies and similar news belongs to nation.'''

safety_settings=[
    {
        "category": palm.types.HarmCategory.HARM_CATEGORY_DEROGATORY,
        "threshold": palm.types.HarmBlockThreshold.BLOCK_NONE,
    },
    {
        "category": palm.types.HarmCategory.HARM_CATEGORY_TOXICITY,
        "threshold": palm.types.HarmBlockThreshold.BLOCK_NONE,
    },        
    {
        "category": palm.types.HarmCategory.HARM_CATEGORY_VIOLENCE,
        "threshold": palm.types.HarmBlockThreshold.BLOCK_NONE,
    },        
    {
        "category": palm.types.HarmCategory.HARM_CATEGORY_SEXUAL,
        "threshold": palm.types.HarmBlockThreshold.BLOCK_NONE,
    },        
    {
        "category": palm.types.HarmCategory.HARM_CATEGORY_MEDICAL,
        "threshold": palm.types.HarmBlockThreshold.BLOCK_NONE,
    },        
    {
        "category": palm.types.HarmCategory.HARM_CATEGORY_DANGEROUS,
        "threshold": palm.types.HarmBlockThreshold.BLOCK_NONE,
    },
]

completion = palm.generate_text(
    model=model,
    prompt=prompt,
    temperature=0.99,
    max_output_tokens=1,
    safety_settings=safety_settings
)

print(completion.result)