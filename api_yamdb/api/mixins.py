from rest_framework import mixins, viewsets


class GetPostDelMixin(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    pass