from django.urls import path
from .views import login_view, register_view, dashboard_view, profile_view, update_profile_view, change_password_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile_view, name='profile_update'),
    path('profile/change-password/', change_password_view, name='change_password'),

]


from .views import notes_list_create_view, note_detail_view

urlpatterns += [
    path("notes/", notes_list_create_view, name="notes_list_create"),
    path("notes/<int:pk>/", note_detail_view, name="note_detail"),
]
