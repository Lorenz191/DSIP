import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect, render
from urllib.parse import quote_plus, urlencode
from django.core.cache import cache
from django.middleware.csrf import get_token

from ..sentiment_model.SentimentAnalysis import SeAn
from django.http import JsonResponse
from bson import ObjectId
from datetime import datetime
from ..db_access.db_access import DB

import requests

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


@csrf_exempt
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


@csrf_exempt
def view_delete_post(request):
    """Löscht einen Vorschlag."""
    if request.method == "POST":
        body = json.loads(request.body)
        post_id = body.get("post_id")

        db_instance = DB()
        post_document = db_instance.select_post_by_id(post_id)

        print(cache.get("roles")[0] != "is_admin")
        print(post_document.get("fk_author") != cache.get("auth0_id"))

        if (
            post_document.get("fk_author") != cache.get("auth0_id")
            and cache.get("roles")[0] != "is_admin"
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
            votes = body.get("votes")

            if not post_id or not votes:
                return JsonResponse({"error": "Missing post_id or votes."}, status=400)

            db_instance = DB()
            success = db_instance.update_post_votes(post_id, votes)

            if success:
                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse(
                    {"error": "Votes not modified. Check data or post existence."},
                    status=200,
                )

        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


def view_create_post(request):
    """Erstellt einen neuen Vorschlag."""
    db_instance = DB()

    if request.method == "POST":
        try:
            post_data = json.loads(request.body)
            body = post_data.get("body")

            sentiment = SeAn().get_sentiment(body.get("title"), body.get("content"))

            ##if sentiment[0]:
            ##  return JsonResponse(
            ##    {"error": "Post contains negative sentiment."}, status=400
            ##)
            if cache.get("roles")[0] != "is_admin":
                post_document = {
                    "fk_author": cache.get("auth0_id"),
                    "body": body,
                    "is_anonym": post_data.get("is_anonym"),
                    "upvotes": [],
                    "downvotes": [],
                    "status": "published",
                    "created_at": datetime.now(),
                }
            elif cache.get("roles")[0] == "is_admin":
                post_document = {
                    "fk_author": cache.get("auth0_id"),
                    "body": body,
                    "is_anonym": post_data.get("is_anonym"),
                    "upvotes": [],
                    "downvotes": [],
                    "status": "published",
                    "sv_post": True,
                    "created_at": datetime.now(),
                }

            result = db_instance.insert_into_post(post_document)

            return JsonResponse({"success": result}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def view_update_post_body(request):
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
            access_token = data.get("accessToken")
            roles = data.get("roles")

            if not auth0_id or not access_token:
                return JsonResponse(
                    {"error": "Both auth0Id and accessToken are required."}, status=400
                )

            cache.set("auth0_id", auth0_id)
            cache.set("access_token", access_token)
            cache.set("roles", roles)

            print("Auth0 ID set in cache:", cache.get("auth0_id"))
            print("Access token set in cache:", cache.get("access_token"))
            print("Roles set in cache", cache.get("roles"))

            return JsonResponse({"success": True, "uuid": auth0_id}, status=200)

        except Exception as e:
            print(f"Error in set_session: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse(
            {"error": "Invalid HTTP method. Only POST is allowed."}, status=405
        )


@csrf_exempt
def get_user_roles(request):
    return JsonResponse({"roles": cache.get("roles")}, status=200)
