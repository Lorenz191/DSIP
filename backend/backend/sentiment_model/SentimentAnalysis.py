from transformers import pipeline

pipe = pipeline("text-classification", model="oliverguhr/german-sentiment-bert")


class SeAn:

    def __init__(self):
        self.model = pipe

    def get_sentiment(self, text):
        result = self.model(text)
        classes = [res["label"] for res in result]
        probabilities = [res["score"] for res in result]
        return classes, probabilities
