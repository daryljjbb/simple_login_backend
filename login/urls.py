from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    # Auth
    MyTokenObtainPairView,
    RegisterView,
    ProfileView,
    ChangePasswordView,

    # Admin User Management
    AdminUserListView,
    AdminUserDetailView,
    AdminUpdateRoleView,
    AdminDeleteUserView,

    # Admin
    AdminDashboardView,

    # Notes
    notes_list_create_view,
    note_detail_view,

    # Tasks
    tasks_list_create_view,
    task_detail_view,
)

urlpatterns = [
    # -----------------------------------------------------
    # AUTHENTICATION
    # -----------------------------------------------------
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),

    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

        # ADMIN USER MANAGEMENT
    path("admin/users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin_user_detail"),
    path("admin/users/<int:pk>/role/", AdminUpdateRoleView.as_view(), name="admin_update_role"),
    path("admin/users/<int:pk>/delete/", AdminDeleteUserView.as_view(), name="admin_delete_user"),


    # -----------------------------------------------------
    # ADMIN (ROLE‑PROTECTED)
    # -----------------------------------------------------
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),

    # -----------------------------------------------------
    # NOTES
    # -----------------------------------------------------
    path("notes/", notes_list_create_view, name="notes_list_create"),
    path("notes/<int:pk>/", note_detail_view, name="note_detail"),

    # -----------------------------------------------------
    # TASKS
    # -----------------------------------------------------
    path("tasks/", tasks_list_create_view, name="tasks_list_create"),
    path("tasks/<int:pk>/", task_detail_view, name="task_detail"),
]
