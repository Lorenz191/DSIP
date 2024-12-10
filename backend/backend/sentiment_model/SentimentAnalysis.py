from transformers import pipeline

pipe = pipeline(
    "text-classification", model="oliverguhr/german-sentiment-bert", device=-1
)


class SeAn:

    def __init__(self):
        self.model = pipe

    def get_sentiment(self, title, content):
        title_sentiment = self.model(title)[0]
        content_sentiment = self.model(content)[0]

        if (
            title_sentiment["label"] == "negative"
            or content_sentiment["label"] == "negative"
        ):
            return True, title_sentiment, content_sentiment
        return False, title_sentiment, content_sentiment
