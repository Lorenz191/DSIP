import json
import logging

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

from ..sentiment_model.SentimentAnalysis import SeAn
from bson import ObjectId
from datetime import datetime
from ..db_access.db_access import DB


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


def check_origin_and_auth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if (
            request.META.get("HTTP_ORIGIN") != "http://localhost:8080"
            or request.META.get("HTTP_ORIGIN") != "http://localhost:8000"
        ):
            return JsonResponse({"error": "Unauthorized origin"}, status=403)

        if not request.session.get("auth0_id"):
            return JsonResponse(
                {"error": "Unauthorized: auth0_id not set in session"}, status=403
            )

        return func(request, *args, **kwargs)

    return wrapper


# @check_origin_and_auth
@csrf_exempt
def view_get_posts(request):
    db_instance = DB()
    posts = db_instance.select_posts()
    serialized_posts = [custom_serializer(post) for post in posts]
    return JsonResponse(serialized_posts, safe=False)


@csrf_exempt
# @check_origin_and_auth
def view_get_sv_posts(request):
    db_instance = DB()
    posts = db_instance.select_posts_sv()
    serialized_posts = [custom_serializer(post) for post in posts]
    return JsonResponse(serialized_posts, safe=False)


@csrf_exempt
# @check_origin_and_auth
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
# @check_origin_and_auth
def view_delete_post(request):
    """Löscht einen Vorschlag."""
    if request.method == "POST":
        body = json.loads(request.body)
        post_id = body.get("post_id")

        db_instance = DB()
        post_document = db_instance.select_post_by_id(post_id)

        if (
            post_document.get("fk_author") != cache.get("auth0_id")
            and cache.get("admin") != True
            and cache.get("sv") != True
            and cache.get("auth0_id") != post_document.get("fk_author")
        ):
            return JsonResponse(
                {"error": "You are not authorized to delete this post."}, status=403
            )

        db_instance.delete_post(post_id)
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
# @check_origin_and_auth
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


@csrf_exempt
# @check_origin_and_auth
def view_create_post(request):
    """Erstellt einen neuen Vorschlag."""
    db_instance = DB()

    if request.method == "POST":
        try:
            post_data = json.loads(request.body)
            logging.info(post_data)

            sentiment = SeAn().contains_swearwords(
                post_data.get("title"), post_data.get("content")
            )

            logging.info(sentiment)

            if sentiment[0]:
                return JsonResponse(
                    {"error": "Post contains negative sentiment."}, status=400
                )
            if not cache.get("sv"):
                if cache.get("auth0_id") is not None:
                    post_document = {
                        "fk_author": cache.get("auth0_id"),
                        "body": {
                            "title": post_data.get("title"),
                            "content": post_data.get("content"),
                        },
                        "is_anonym": True,
                        "upvotes": [],
                        "downvotes": [],
                        "status": "published",
                        "created_at": datetime.now(),
                    }
                else:
                    return JsonResponse(status=403)
            elif cache.get("sv"):
                post_document = {
                    "fk_author": cache.get("auth0_id"),
                    "body": {
                        "title": post_data.get("title"),
                        "content": post_data.get("content"),
                    },
                    "is_anonym": True,
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


@csrf_exempt
# @check_origin_and_auth
def view_update_post_body(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            post_id = body.get("post_id")
            post_title = body.get("title")
            post_content = body.get("content")

            db_instance = DB()
            post_document = db_instance.select_post_by_id(post_id)

            if post_document.get("fk_author") != cache.get("auth0_id"):
                return JsonResponse(
                    {"error": "You are not authorized to update this post."}, status=403
                )

            result = db_instance.update_post_body(post_id, post_title, post_content)

            return JsonResponse({"success": result}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
# @check_origin_and_auth
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


@csrf_exempt
# @check_origin_and_auth
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


logging.basicConfig(level=logging.DEBUG)


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

            # Logging cache operations
            cache.set("auth0_id", auth0_id, timeout=86400)
            cache.set("access_token", access_token, timeout=86400)
            cache.set("sv", ("sv" in roles), timeout=86400)
            cache.set("admin", ("is_admin" in roles), timeout=86400)

            logging.info("Auth0 ID set in cache: %s", cache.get("auth0_id"))
            logging.info("Access token set in cache: %s", cache.get("access_token"))
            logging.info(
                "Roles set in cache: %s",
                str(cache.get("admin")) + "/" + str(cache.get("sv")),
            )

            response = JsonResponse({"success": True, "uuid": auth0_id}, status=200)

            return response

        except Exception as e:
            logging.error("Error in set_session: %s", str(e), exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse(
            {"error": "Invalid HTTP method. Only POST is allowed."}, status=405
        )


@csrf_exempt
def view_get_user_posts(request):
    if request.method == "GET":
        db_instance = DB()
        posts = db_instance.select_posts_for_user(cache.get("auth0_id"))
        serialized_posts = [custom_serializer(post) for post in posts]
        return JsonResponse(serialized_posts, status=200, safe=False)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
def view_get_user_liked_posts(request):
    if request.method == "GET":
        db_instance = DB()
        posts = db_instance.select_upvotes(cache.get("auth0_id"))
        serialized_posts = [custom_serializer(post) for post in posts]
        return JsonResponse(serialized_posts, status=200, safe=False)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
def view_get_user_disliked_posts(request):
    if request.method == "GET":
        db_instance = DB()
        posts = db_instance.select_downvotes(cache.get("auth0_id"))
        serialized_posts = [custom_serializer(post) for post in posts]
        return JsonResponse(serialized_posts, status=200, safe=False)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
def clear_session_cache(request):
    if request.method == "POST":
        try:

            data = json.loads(request.body)

            access_token_sent = data.get("access_token")

            auth0_id = cache.get("auth0_id")

            logging.info(access_token_sent)
            logging.info(cache.get("access_token"))

            if access_token_sent == cache.get("access_token") and auth0_id:
                cache.delete("auth0_id")
                cache.delete("access_token")
                cache.delete("sv")
                cache.delete("admin")

                request.session.flush()

                return JsonResponse(
                    {"success": True, "message": "Cache cleared and user logged out"},
                    status=200,
                )
            else:
                return JsonResponse({"error": "No active session found"}, status=403)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)


@csrf_exempt
def view_add_comment(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            post_id = body.get("post_id")
            comment = body.get("comment")
            comment = {
                "author": "SV/Admin",
                "comment": comment,
                "author_id": cache.get("auth0_id"),
                "created_at": datetime.now(),
            }

            if cache.get("sv") is None or cache.get("admin") is None:
                return JsonResponse(
                    {"error": "Unauthorized: auth0_id not set in session"}, status=403
                )
            else:
                db_instance = DB()
                result = db_instance.post_comment(post_id, comment)
                return JsonResponse({"success": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
