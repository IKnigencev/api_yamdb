from rest_framework import viewsets

from reviews.models import *

from .permissions import *
from .serializers import *

class TitleViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass
