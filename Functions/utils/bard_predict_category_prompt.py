from bardapi import Bard
import os

def predict_category_prompt(title, description):
    token = 'dQgo_YN818D59gMdRIHG_Oar2j79s1Nk7a62HA4HzB1lu4wqNzZPYF3rV3fN4hctJ7ZFGA.'
    os.environ['_BARD_API_KEY']=token

    bard = Bard()
    # bard.token(token)
    # title = '''Preliminary vigilance report against Delhi Chief Secretary Naresh Kumar in land compensation row seeks his removal'''
    # description = '''The report alleges "a conspiracy by senior officers of Delhi's Vigilance Department", including Chief Secretary Naresh Kumar to undervalue the "scale of the scam" at Rs 312 crore when the actual compensation award "would have resulted in an illicit gain of Rs 850 crore to the beneficiaries".'''

    prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
    Out of the above categories, determine the category below news' title and description belongs to.
    Title: {title}
    Description: {description}
    Response should contain only one word ie, <category>.
    Note: Anything that involves national government bodies and similar news belongs to nation.'''
    category = bard.get_answer(prompt).content
    return category
