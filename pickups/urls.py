from django.urls import path

from pickups.views import PickupListView, PickupDetailView, PickupDetailViewProtected

urlpatterns = [
    path("", PickupListView.as_view()),
    path("request", PickupDetailView.as_view()),
    path("update/<uuid:pk>", PickupDetailViewProtected.as_view()),
    path("delete/<uuid:pk>", PickupDetailViewProtected.as_view())
]