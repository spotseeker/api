from django_filters import rest_framework as filters

from spotseeker.post.models import Post


class PostFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="user__username", method="filter_user")
    is_archived = filters.BooleanFilter(
        field_name="is_archived", method="filter_is_archived"
    )
    is_bookmarked = filters.BooleanFilter(
        field_name="postbookmark__user", method="filter_is_bookmarked"
    )
    is_discover = filters.BooleanFilter(method="filter_is_discover")

    class Meta:
        model = Post
        fields = ["user", "is_archived"]

    def filter_user(self, queryset, name, value):
        return queryset.filter(user__username=value, is_archived=False)

    def filter_is_archived(self, queryset, name, value):
        if value:
            return queryset.filter(is_archived=True, user=self.request.user)
        return queryset.filter(is_archived=False)

    def filter_is_bookmarked(self, queryset, name, value):
        if value:
            return queryset.filter(postbookmark__user=self.request.user)
        return queryset.filter(is_archived=False)

    def filter_is_discover(self, queryset, name, value):
        following = self.request.user.following.values_list(
            "followed_user_id", flat=True
        )
        return queryset.exclude(user_id__in=following).filter(is_archived=False)
