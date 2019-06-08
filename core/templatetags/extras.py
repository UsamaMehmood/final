from django.template import library


register = library.Library()

@register.filter('liked_by_user')
def liked_by_user(post, user):
    return post.likes.filter(by=user).exists()
