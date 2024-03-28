import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import json
from pprint import pprint

genai_api_key = os.environ.get("genai_api_key")
genai_api_key = "AIzaSyCkH1kMBD13rpwWwS2VUfcXAIa_uPsfqVo"
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
    
    Response should be in JSON format. No Explanation needed. And no text should be present outside the json object.''' + '''
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
    try:
        tags = response.text
    except ValueError:
        return {}
    if tags[0] == '`':
        tags = tags[tags.find('\n'):tags.rfind('\n')]
    print(tags)
    if tags == None or tags[0] != '{':
        return {}
    return json.loads(tags)

# title = "Bengaluru’s car wash sector struggles amid water crisis, waterless options start gaining popularity in city"
# description = "The Bangalore Water Supply and Sewerage Board (BWSSB) has cracked down on using drinking water for non-essential purposes like car washing and has announced hefty penalty of Rs 5,000 for violations"
# content = [
#     "Written by Muskaan Kousar",
#     "Bengaluru’s car wash sector is feeling the heat and not because of the hot sun but due to the severe water crisis in the city. The water crisis has forced some businesses to scramble for solutions, while others have been forced to shut down.",
#     "The Bangalore Water Supply and Sewerage Board (BWSSB) has cracked down on using drinking water for non-essential purposes like car washing and has announced hefty penalty of Rs 5,000 for violations. This, coupled with drying borewells, has disrupted the traditional car wash services in the city who mainly use high-pressure water hose pipes to clean vehicles.",
#     "Ashraf Hussain, a worker at the K S Water Service, said, “We are struggling because of the water crisis. Initially, we were using water tanker services to cater to the car washing needs of our customers but we were warned by the BWSSB.”",
#     "“We not just stopped using tanker services but completely suspended the car wash service. Our business has gone down and now, there are very few customers,” Hussain said.",
#     "Amidst the crisis, a few establishments have started advertising for dry car wash services. “We offer waterless car washing service,” said Harish of Flip Care Washing.",
#     "“We use just one litre of water and 30 ml of a solution. With that, we wash an entire car or maybe two, depending on the size of the vehicles.”",
#     "This method not only saves water but also prioritises safety. “We don’t need any extra water or chemicals,” Harish added. “The chemicals that we use are also both human and environment friendly. We focus mostly on luxury cars. We have our regular customers and we focus on saving water and providing a hygienic car wash,” he said.",
#     "However, some establishments have not been affected by the water crisis in Bengaluru. For instance, Amruth Car Wash claims the shortfall has not affected them much. Amruth, the owner of the business, said, “It has not affected our service because we are not using a lot of water. We are getting a tanker that can sustain us for 15-20 days.”",
#     "Asked if the BWSSB has warned his establishment against using tanker services for washing vehicles, Amruth said, “We haven’t received any warning or notice.”"
# ]
# pprint(get_tags(title, description, content))