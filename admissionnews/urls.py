from django.urls import path

from .views import(
    UniversityCreateView, UniversityDetailView,
    UniversityListView, UniversityUpdateView,
    UniversityDeleteView,

    AdmissionNewsCreateView, AdmissionNewsDeleteView,
    AdmissionNewsDetailView, AdmissionNewsUpdateView,
    AdmissionNewsListView,

    CommentCreateView, CommentUpdateView, CommentDeleteView,

    DepartmentCreateView, DepartmentDeleteView, DepartmentDetailView,
    DepartmentUpdateView


)

urlpatterns = [
    path('', UniversityListView.as_view(), name='university-list'),
    path('university/new/', UniversityCreateView.as_view(),
         name='university-create'),
    path('university/<int:pk>/', UniversityDetailView.as_view(),
         name="university-detail"),
    path('university/<int:pk>/update/', UniversityUpdateView.as_view(),
         name="university-update"),
    path('university/<int:pk>/delete/', UniversityDeleteView.as_view(),
         name="university-delete"),
    #
    path('university/<int:pk>/new/', DepartmentCreateView.as_view(),name="department-create"),
    path('department/<int:pk>/', DepartmentDetailView.as_view(),name="department-detail"),
    path('department/<int:pk>/update/', DepartmentUpdateView.as_view(),name="department-update"),
    path('department/<int:pk>/delete/', DepartmentDeleteView.as_view(),name="department-delete"),
    #
    path('university/<int:unipk>/new/', AdmissionNewsCreateView.as_view(),
         name="admissionnews-create"),
    path('news/', AdmissionNewsListView.as_view(), name='admissionnews-list'),
    path('news/<int:pk>/', AdmissionNewsDetailView.as_view(),
         name="admissionnews-detail"),
    path('news/<int:pk>/update/', AdmissionNewsUpdateView.as_view(),
         name="admissionnews-update"),
    path('news/<int:pk>/delete/', AdmissionNewsDeleteView.as_view(),
         name="admissionnews-delete"),

    path('news/<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('news/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('news/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete')

]