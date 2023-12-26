import requests
from urllib import parse

title = '''Preliminary vigilance report against Delhi Chief Secretary Naresh Kumar in land compensation row seeks his removal'''
description = '''The report alleges "a conspiracy by senior officers of Delhi's Vigilance Department", including Chief Secretary Naresh Kumar to undervalue the "scale of the scam" at Rs 312 crore when the actual compensation award "would have resulted in an illicit gain of Rs 850 crore to the beneficiaries".'''

url = 'https://api.freegpt4.ddns.net/?text='
prompt = f'''Categories: Technology, Environment, Entertainment, Politics, Education, Crime, Sports, Business, Travel, Money and Nation.
Out of the above categories, determine the category below news' title and description belongs to.
Title: {title}
Description: {description}
Response should contain only one word ie, <category>.
Note: Anything that involves government bodies and similar news belongs to nation.'''
encoded_prompt = parse.quote(prompt)
print(encoded_prompt)
response = requests.get(url+encoded_prompt)
print(str(response.content))