from django.urls import path


from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.user_register, name="register"),
    path("code-validation/", views.code_validation, name="code_validation"),
    path("logout/", views.logout_user, name="logout"),
    path("password-create/", views.new_user_create, name="password_for_new_user"),
    path("login-with-password/", views.login_with_password,
         name="login_with_password"),
    path("add-to-favourite/", views.add_to_facourite, name="add_to_favourite"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-address/", views.add_address, name="add_address"),
    path("city-ajax-set/", views.city_ajax_set, name="city_ajax_set"),
    path("favourite-products/", views.favourite_products_list,
         name="favourite_products_list"),
    path("dashboard-adress/", views.dashboard_adress, name="dashboard_address"),
    path("update-address/<int:address_id>/",
         views.address_edit, name="address_edit"),
    path("dashboard-notifications/", views.dashboard_notifications,
         name="dashboard_notifications"),
    path("dashboard-account/", views.dashbourd_acount, name="dashboard_account"),
    path("phone-edit-validation/", views.phone_change_validation,
         name="phone_change_validation"),
    path("set-city/", view=views.set_city, name="set_city"),
    path("edit-phone-phone-entry/", view=views.edit_phone_phone_entry,
         name="edit_phone_phone_entry"),
    path("edit-phone-validation-previous/", view=views.edit_phone_validation_previous,
         name="edit_phone_validation_previous"),
    path("edit-phone-new-phone-validation/", view=views.edit_phone_new_phone_validation,
         name="edit_phone_new_phone_validation"),
    path("generate-new-valiadation-code/", view=views.generate_new_valiadation_code,
         name="generate_new_valiadation_code"),
    path("password-edit-ajax/", view=views.password_edit_ajax,
         name="password_edit_ajax"),
    path("remove-address/", view=views.delete_address, name="remove_address"),
]
