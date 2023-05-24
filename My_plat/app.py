# from transformers import T5Tokenizer, T5Model

# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5Model.from_pretrained("t5-small")

# input_ids = tokenizer(
#     "Studies have been shown that owning a dog is good for you", return_tensors="pt"
# ).input_ids  # Batch size 1
# decoder_input_ids = tokenizer("Studies show that", return_tensors="pt").input_ids  # Batch size 1

# # forward pass
# outputs = model(input_ids=input_ids, decoder_input_ids=decoder_input_ids)
# last_hidden_states = outputs.last_hidden_state





































# from django.apps import AppConfig
# import html
# import pathlib
# import os

# from fast_bert.prediction import BertClassificationPredictor

# class WebappConfig(AppConfig):
#     name = 'fastbert'
#     MODEL_PATH = Path("model")
#     BERT_PRETRAINED_PATH = Path("model/")
#     LABEL_PATH = Path("")
#     predictor = BertClassificationPredictor(model_path = MODEL_PATH/"multilabel-emotion-fastbert-basic.bin", 
#                                             pretrained_path = BERT_PRETRAINED_PATH, 
#                                             #  label_path = LABEL_PATH,
#                                              multi_label=False)  

