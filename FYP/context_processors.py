from django.conf import settings

def add_project_name(obj):
    return {"PROJECT_NAME": settings.PROJECT_NAME}
