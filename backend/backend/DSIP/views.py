import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render
from urllib.parse import quote_plus, urlencode

from ..sentiment_model.SentimentAnalysis import SeAn
from django.http import JsonResponse
from bson import ObjectId
from datetime import datetime
from ..db_access.db_access import DB

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def custom_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [custom_serializer(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: custom_serializer(value) for key, value in obj.items()}
    return obj


def sean_view(request, text):
    sentiment = SeAn().get_sentiment(text)
    return HttpResponse(sentiment[0])


# POST


def view_get_posts(request):
    db_instance = DB()
    posts = db_instance.select_posts()
    serialized_posts = [custom_serializer(post) for post in posts]
    return JsonResponse(serialized_posts, safe=False)


def view_get_sv_posts(request):
    db_instance = DB()
    posts = db_instance.select_posts_sv()
    serialized_posts = [custom_serializer(post) for post in posts]
    return JsonResponse(serialized_posts, safe=False)


@csrf_exempt
def view_get_post(request):
    """Returns a specific post."""
    if request.method == "POST":
        body = json.loads(request.body)
        post_id = body.get("post_id")

        db_instance = DB()
        post = db_instance.select_post_by_id(post_id)

        if post is None:
            return JsonResponse({"error": "Post not found"}, status=404)

        serialized_post = custom_serializer(post)
        return JsonResponse(serialized_post, safe=False)

    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


def view_delete_post(request):
    """Löscht einen Vorschlag."""
    if request.method == "POST":
        body = json.loads(request.body)
        post_id = body.get("post_id")

        db_instance = DB()
        post_document = db_instance.select_post_by_id(post_id)

        if (
            post_document.get("fk_author") != request.session.get("auth0_id")
            or request.session.get("is_admin") == False
        ):
            return JsonResponse(
                {"error": "You are not authorized to delete this post."}, status=403
            )

        db_instance.delete_post(post_id)
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
def view_vote_post(request):
    """Handles voting on a post."""
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            post_id = body.get("post_id")
            user_id = body.get("user_id")

            vote_type = body.get("vote_type", "upvote")

            if not post_id or not user_id:
                return JsonResponse(
                    {"error": "post_id and user_id are required."}, status=400
                )

            db_instance = DB()

            if body.get("action") == "add":
                success = db_instance.add_post_votes(post_id, user_id, vote_type)
            elif body.get("action") == "remove":
                success = db_instance.remove_post_vote(post_id, user_id, vote_type)
            else:
                return JsonResponse(
                    {"error": "Invalid action. Must be 'add' or 'remove'."}, status=400
                )

            if success:
                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse({"error": "Failed to update vote."}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
def view_create_post(request):
    """Erstellt einen neuen Vorschlag."""
    db_instance = DB()

    if request.method == "POST":
        try:
            post_data = json.loads(request.body)
            body = post_data.get("body")

            sentiment = SeAn().get_sentiment(body.get("title"), body.get("content"))

            if sentiment[0]:
                return JsonResponse(
                    {"error": "Post contains negative sentiment."}, status=400
                )

            post_document = {
                "fk_author": request.session.get("auth0_id"),
                "body": body,
                "is_anonym": post_data.get("is_anonym"),
                "upvotes": [{"user": ObjectId(post_data.get("fk_author"))}],
                "downvotes": [],
                "status": "published",
                "created_at": datetime.now(),
            }

            result = db_instance.insert_into_post(post_document)

            return JsonResponse({"success": result}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def view_update_post(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            post_id = body.get("post_id")
            post_data = body.get("post_data")

            db_instance = DB()
            post_document = db_instance.select_post_by_id(post_id)

            if post_document.get("fk_author") != request.session.get("auth0_id"):
                return JsonResponse(
                    {"error": "You are not authorized to update this post."}, status=403
                )

            result = db_instance.update_post_body(post_id, post_data)

            return JsonResponse({"success": result}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


def view_update_status_post(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            post_id = body.get("post_id")
            status = body.get("status")

            db_instance = DB()
            post_document = db_instance.select_post_by_id(post_id)

            if post_document.get("fk_author") != request.session.get("auth0_id"):
                return JsonResponse(
                    {"error": "You are not authorized to update this post."}, status=403
                )

            result = db_instance.update_post_status(post_id, status)

            return JsonResponse({"success": result}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


def view_login_user(request):
    """Loggt einen Benutzer ein."""
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def view_delete_user_profile(request, user_id):
    """Löscht das Benutzerprofil."""
    if request.session.get("auth0_id") == user_id:
        db_instance = DB()
        db_instance.delete_user(user_id)
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse(
            {"error": "You are not authorized to delete this user."}, status=403
        )


@csrf_exempt
def set_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            auth0_id = data.get("auth0Id")

            db_session = DB()
            db_session.insert_into_user(user_id=auth0_id, is_admin=False)

            if auth0_id:
                request.session["auth0_id"] = auth0_id
                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse({"error": "auth0Id is required."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
