from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from joblib import load

def get_category(title, description):
    model = load_model("utils/category_predictor_cnn.h5")
    input_data = [title+" "+description]

    max_words = 10000
    max_sequence_length = 100
    tokenizer = Tokenizer(num_words=max_words)
    new_sequences = tokenizer.texts_to_sequences(input_data)
    pred_X = pad_sequences(new_sequences, maxlen=max_sequence_length)
    
    predictions = model.predict(pred_X)

    label_encoder = load("utils/label_encoder.pkl")
    category = label_encoder.inverse_transform(predictions.argmax(axis=1))
    return category[0]

# title = "'Amazing Host' Priyanka Chopra And Preity Zinta Had This Much Fun At Jonas Brothers Concert"
# description = "'Last night I officially became a fan', writes Preity Zinta"
# print(get_category(title, description))