from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import pandas as pd
model_name = "cointegrated/rubert-tiny-toxicity"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None)







labels = ['dangerous', 'insult', 'obscenity', 'threat']



def is_toxic(text:str):
    res = pipeline(text)
    df = pd.DataFrame(res[0])
    for _, row in df.iterrows():
        if row['label'] in labels and row['score'] >= 0.5:
            return True
    return False
    

    


