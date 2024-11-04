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
