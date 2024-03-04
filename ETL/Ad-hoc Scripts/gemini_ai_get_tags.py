import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import json
from dotenv import load_dotenv
# from pprint import pprint

load_dotenv()
genai_api_key = os.environ.get("genai_api_key")
genai.configure(api_key=genai_api_key)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

def get_tags(title, description, content):

    model = genai.GenerativeModel('gemini-pro')

    prompt = f'''title: {title}
    description: {description}
    content: {''.join(c for c in content)}
    
    List the relevant tags by classifying them into people based tags, location or landmark based tags and other generic tags.
    
    Classify the location tags into landmarks, localities, cities, states, countries.
    
    Response should be in JSON format. No Explanation needed. And no text should be present outside the json object. Reponse should not start with anything else other than the JSON object itself.''' + '''
    Sample question:
    title: Student from Hyderabad ambushed and robbed at gunpoint in Chicago
    description: Syed Mazahir Ali, a resident of Hashim Nagar of Langer Houz, was a few minutes away from his flat in Campbell Ave, Chicago, when three armed robbers ambushed and attacked him
    content: A student from Hyderabad pursuing his Masters in Indiana Wesleyan University in Chicago was ambushed and robbed at gunpoint by three armed robbers on February 4. Syed Mazahir Ali, a resident of Hashim Nagar of Langer Houz, was a few minutes away from his flat in Campbell Ave, Chicago, when three armed robbers ambushed and attacked him. They fled with his wallet and mobile. There have been a string of violent incidents involving students from India over the past few weeks. In a viral video shot minutes after the attack, which is being circulated on social media, Mr. Ali can be heard mentioning how they jumped on him and that he is scared Speaking to The Hindu, his wife, Syeda Ruquiya Fatima Razvi, said that Mr. Ali went to the U.S. .about six months ago for a two years Masters course in Information & Technology from Indiana Wesleyan University. “My husband sustained injuries on the back of his head, back and knees. He is admitted at a private hospital and is in a state of shock. His video doing rounds on social media is traumatising for us to watch,” she said. Ms. Rizwi has written to the Minister for External Affairs S. Jaishankar requesting help in getting the best medical treatment.
    Sample Response in JSON format:
    {
        "people": [
            "Syed Mazahir Ali",
            "Syeda Ruquiya Fatima Razvi",
            "S. Jaishankar",
            "Minister of External Affairs"
            "Students from India"
        ],
        "location": {
            "landmarks": [],
            "localities": [
                "Hashim Nagar, Langer Houz",
                "Campbell Ave, Chicago"
            ],
            "cities": [
                "Hyderabad",
                "Chicago"
            ],
            "states": [
                "Telangana",
                "IL"
            ],
            "countries": [
                "India",
                "USA"
            ]
        },
        "other": [
            "robbery",
            "gunpoint",
            "attack",
            "violence",
            "injuries",
            "hospital",
            "video",
            "social media",
            "medical treatment"
        ]
    }
    '''

    safety_settings={
        # HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        # HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        # HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
        # HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        # HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
        # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
        # HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE
    }
    response = model.generate_content(prompt,safety_settings=safety_settings, generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        temperature=0.2))
    tags = response.text
    print(tags)
    if not tags:
        return None
    return json.loads(tags)

# title = "Man thrashed and sexually assaulted in Delhi; police arrest 2"
# description = "The incident took place on Diwali night when the complainant and the family of the accused were celebrating the festival."
# content  = ["A student from Hyderabad pursuing his Masters in Indiana Wesleyan University in Chicago was ambushed and robbed at gunpoint by three armed robbers on February 4.","Syed Mazahir Ali, a resident of Hashim Nagar of Langer Houz, was a few minutes away from his flat in Campbell Ave, Chicago, when three armed robbers ambushed and attacked him. They fled with his wallet and mobile.","There have been a string of violent incidents involving students from India over the past few weeks. In a viral video shot minutes after the attack, which is being circulated on social media, Mr. Ali can be heard mentioning how they jumped on him and that he is scared","Speaking to The Hindu, his wife, Syeda Ruquiya Fatima Razvi, said that Mr. Ali went to the U.S. .about six months ago for a two years Masters course in Information & Technology from Indiana Wesleyan University. “My husband sustained injuries on the back of his head, back and knees. He is admitted at a private hospital and is in a state of shock. His video doing rounds on social media is traumatising for us to watch,” she said.","Ms. Rizwi has written to the Minister for External Affairs S. Jaishankar requesting help in getting the best medical treatment."]
# pprint(get_tags(title, description, content))