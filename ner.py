from transformers import pipeline
ner_pipeline = pipeline("ner" , model = "dslim/bert-base-NER" , grouped_entities = True)#implementing a named entity recognition based pipeline using BERT
def extract_entities(text):
    if not text.strip():
        return []
    entities = ner_pipeline(text)
    result = []
    for ent in entities:
        result.append({"entity" : ent["entity_group"] , #store the name of entities
                       "word" : ent["word"]})
    return result
