from rest_framework.response import Response
from rest_framework import status
from ....backend.sentiment_model.SentimentAnalysis import SeAn


def create_post(request, post):
    """Erstellt einen neuen Vorschlag."""
    model = SeAn()

    if model.get_sentiment(post):
        return Response(
            "Post contains negative sentiment", status=status.HTTP_400_BAD_REQUEST
        )
    else:
        pass

    pass


def get_post(request, post_id):
    """Gibt einen bestimmten Vorschlag zurück."""
    pass


def update_post(request, post_id):
    """Aktualisiert einen bestehenden Vorschlag."""
    pass


def delete_post(request, post_id):
    """Löscht einen Vorschlag."""
    pass


def upvote_post(request, post_id):
    """Erhöht die Bewertung eines Vorschlags."""
    pass


def downvote_post(request, post_id):
    """Verringert die Bewertung eines Vorschlags."""
    pass
