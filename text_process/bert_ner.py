from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def main():
    print("loading models.....")
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    print("loaded models.....")

    print("extracting entities.....")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    example = "My name is Wolfgang and I live in Berlin"

    ner_results = nlp(example)
    print(ner_results)

if __name__ == '__main__':
    main()