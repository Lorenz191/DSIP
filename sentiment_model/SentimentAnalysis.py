from germansentiment import SentimentModel


class SeAn:

    def __init__(self):
        self.model = SentimentModel()

    def get_sentiment(self, text):
        classes, probabilities = self.model.predict_sentiment(
            text, output_probabilities=True
        )

        for i in probabilities[0]:
            if i[0] == classes[0]:
                probabilities = i[1]
                break

        return classes[0], probabilities


if __name__ == "__main__":
    model = SeAn()
    print(model.get_sentiment(["Du bist das Kind einer HUre"]))
