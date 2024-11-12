from django.shortcuts import render
from django.http import HttpResponse
from ..sentiment_model.SentimentAnalysis import SeAn
from ..api.admin.admin import delete_user_post, comment_as_admin, get_reports
from ..api.external.external import authenticate_with_external_service
from ..api.forum.forum import (
    create_forum_post,
    get_forum_posts,
    create_forum_comment,
    get_forum_comments,
)
from ..api.moderation.moderation import analyze_sentiment, moderate_post
from ..api.posts.posts import (
    create_post,
    get_post,
    update_post,
    delete_post,
    upvote_post,
    downvote_post,
)
from ..api.sort.sorting import (
    sort_posts_by_newest,
    sort_posts_by_oldest,
    sort_posts_by_popularity,
)
from ..api.users.users import register_user, get_user_profile, update_user_profile


def sean_view(request, text):
    sentiment = SeAn().get_sentiment(text)
    return HttpResponse(sentiment[0])


# ADMIN


def view_delete_user_post(request, post_id):
    status = delete_user_post(post_id=post_id)
    return HttpResponse(status=status)


def view_comment_as_admin(request, post_id):
    status = comment_as_admin(post_id=post_id)
    return HttpResponse(status=status)


# EXTERNAL


def view_authenticate_with_external_service(request):
    """Authentifiziert sich bei einem externen Dienst."""
    pass


# POST


def view_create_post(request, post_body):
    """Erstellt einen neuen Vorschlag."""
    pass


def view_get_post(request, post_id):
    """Gibt einen bestimmten Vorschlag zurück."""
    pass


def view_update_post(request, post_id):
    """Aktualisiert einen bestehenden Vorschlag."""
    pass


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
