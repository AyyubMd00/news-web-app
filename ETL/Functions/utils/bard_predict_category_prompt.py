from bardapi import Bard
import os

def predict_category_prompt(title, description):
    token = 'dQgo_R5M_D5zZRsunONckuNy483g3M0mCbGS5Ueqy5ZIjfhx-Z_gry6YmEPawk4J-9XcmA.'
    # os.environ['_BARD_API_KEY']=token

    bard = Bard(token=token)
    # bard.token(token)

    prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
    Out of the above categories, determine the category below news' title and description belongs to.
    Title: {title}
    Description: {description}
    Response should contain only one word ie, <category>.
    Note: Anything that involves national government bodies and similar news belongs to nation.'''
    response = bard.get_answer(prompt)
    # print(response)
    if response['status_code'] == 200:
        category = response['content']
        return category
    return ""

title = '''Preliminary vigilance report against Delhi Chief Secretary Naresh Kumar in land compensation row seeks his removal'''
description = '''The report alleges "a conspiracy by senior officers of Delhi's Vigilance Department", including Chief Secretary Naresh Kumar to undervalue the "scale of the scam" at Rs 312 crore when the actual compensation award "would have resulted in an illicit gain of Rs 850 crore to the beneficiaries".'''
print(predict_category_prompt(title, description))