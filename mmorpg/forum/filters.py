from django_filters import FilterSet, ModelMultipleChoiceFilter, BooleanFilter
from django_filters.widgets import BooleanWidget
from .models import Response, Post


class ResponseFilter(FilterSet):

    def myPosts(request):
        if request is None:
            return Post.objects.none()

        user = request.user
        return Post.objects.filter(user=user)

    post = ModelMultipleChoiceFilter(
        queryset=myPosts,
        label="Посты",
        conjoined=False,
    )

    is_accepted = BooleanFilter(
        field_name="is_accepted",
        widget=BooleanWidget(),
        label="Принято",
    )

    class Meta:
        model = Response
        fields = [
            "post",
            "is_accepted"
        ]
