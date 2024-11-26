from django.shortcuts import render
from django.http import HttpResponse

from ..sentiment_model.SentimentAnalysis import SeAn
from django.http import JsonResponse
from bson import ObjectId
from datetime import datetime
from ..db_access.db_access import DB


def custom_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def sean_view(request, text):
    sentiment = SeAn().get_sentiment(text)
    return HttpResponse(sentiment[0])


# ADMIN


def view_delete_user_post(request, post_id):
    pass


def view_comment_as_admin(request, post_id):
    pass


# EXTERNAL


def view_authenticate_with_external_service(request):
    """Authentifiziert sich bei einem externen Dienst."""
    pass


# POST


def view_get_posts(request):
    db_instance = DB()
    posts = db_instance.select_posts()
    serialized_posts = [
        {
            key: (
                custom_serializer(value)
                if isinstance(value, (ObjectId, datetime))
                else value
            )
            for key, value in post.items()
        }
        for post in posts
    ]
    return JsonResponse(serialized_posts, safe=False)


def view_get_post(request, post_id):
    """Gibt einen bestimmten Vorschlag zurück."""
    db_instance = DB()
    post = db_instance.select_post_by_id(post_id)
    return JsonResponse(post, safe=False)


def view_delete_post(request, post_id):
    """Löscht einen Vorschlag."""

    pass


def view_upvote_post(request, post_id):
    """Erhöht die Bewertung eines Vorschlags."""

    pass


def view_downvote_post(request, post_id):
    """Verringert die Bewertung eines Vorschlags."""

    pass


# USERS


def view_register_user(request):
    """Registriert einen neuen Benutzer."""
    pass


def view_login_user(request):
    """Loggt einen Benutzer ein."""
    pass


def view_get_user_profile(request, user_id):
    """Gibt das Benutzerprofil zurück."""
    pass


def view_delete_user_profile(request, user_id):
    """Löscht das Benutzerprofil."""
    pass


def view_create_post(request):
    pass


def view_update_post(request, post_id, post_body):
    pass
