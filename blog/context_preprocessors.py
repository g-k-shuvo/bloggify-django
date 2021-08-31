from blog.models import Topic


def topic_preprocessor(request):
    topics = Topic.objects.all()
    return {'topics': topics}