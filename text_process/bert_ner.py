from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

def main():
    print("loading models.....")
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    print("loaded models.....")

    print("extracting entities.....")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    example = "People don't have their priorities right, our priority should be to get rid of BJP from power. But what our people are focusing on is 'if not Modi then who', Modi is a fucking clown, anyone is better than MODI. But don't vote for anyone vote for the party that's has the best chance to defeat BJP.\n\nIt's common sense."

    ner_results = nlp(example)
    print(ner_results)

if __name__ == '__main__':
    main()