from transformers import pipeline

pipe = pipeline("text-classification", model="oliverguhr/german-sentiment-bert")


class SeAn:

    def __init__(self):
        self.model = pipe

    def get_sentiment(self, post_body):
        result_header = self.model("header")
        result_text = self.model(post_body["text"])
        classes = {}
        propabilities = {}

        classes["header"] = [res["label"] for res in result_header]
        classes["text"] = [res["label"] for res in result_text]
        propabilities["header"] = [res["score"] for res in result_header]
        propabilities["text"] = [res["score"] for res in result_text]

        if classes["header"] == "negative" or classes["text"] == "negative":
            return 1, classes, propabilities
        return 0, classes, propabilities
