from rest_framework.response import Response
from rest_framework import status

def delete_user_post(request, post_id):
    """Löscht einen Benutzer-Beitrag als Admin."""
    pass

def comment_as_admin(request, post_id): # muss nicht
    """Kommentiert einen Beitrag als Admin."""
    pass

def get_reports(request):
    """Gibt Berichte und Statistiken zu Vorschlägen zurück."""
    pass
