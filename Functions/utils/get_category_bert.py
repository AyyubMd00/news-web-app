import torch
from transformers import BertForSequenceClassification, BertTokenizer
import numpy as np

categories = [
    'Technology',
    'Environment',
    'Entertainment',
    'Politics',
    'Education',
    'Crime',
    'Sports',
    'Business',
    'Travel',
    'Money'
]

def get_category(title, description):
    text = [title+" "+description]
    
    model = BertForSequenceClassification.from_pretrained('google/bert_uncased_L-4_H-512_A-8', num_labels=10) # change the model name and the number of labels according to your data
    model.load_state_dict(torch.load('utils/category_predictor.pt', map_location=torch.device('cpu')))
    model.eval() # put the model in inference mode

    tokenizer = BertTokenizer.from_pretrained('google/bert_uncased_L-4_H-512_A-8', do_lower_case=True) # change the model name according to your data

    # preprocess the data
    tokens = tokenizer.encode_plus(text, max_length=128, pad_to_max_length=True, truncation=True, return_tensors='pt')
    seq = tokens['input_ids']
    mask = tokens['attention_mask']

    # pass the data through the model
    with torch.no_grad():
        logits = model(seq, mask)
        pred = np.argmax(logits[0].detach().cpu().numpy(), axis=1)
    category = categories[pred[0]]
    return category

# title = "'Amazing Host' Priyanka Chopra And Preity Zinta Had This Much Fun At Jonas Brothers Concert"
# description = "'Last night I officially became a fan', writes Preity Zinta"
# print(get_category(title, description))