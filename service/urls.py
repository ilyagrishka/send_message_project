from django.urls import path

from service.apps import ServiceConfig
from service.views import MailingListView, MailingSettingsCreateView, MailingSettingsUpdateView, \
    MailingSettingsDeleteView, ClientOfServiceListView, ClientOfServiceUpdateView, ClientOfServiceDeleteView, \
    MailingMessageListView, MailingMessageUpdateView, MailingMessageDeleteView, MailingMessageCreate, \
    ClientOfServiceCreate

app_name = ServiceConfig.name

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("create/", MailingSettingsCreateView.as_view(), name="mailing_create"),
    path("update/<int:pk>/", MailingSettingsUpdateView.as_view(), name="mailing_update"),
    path("delete/<int:pk>/", MailingSettingsDeleteView.as_view(), name="mailing_delete"),
    path('email-attempts/', views.email_attempts_view, name='attempt_to_send'),

    path("clients/", ClientOfServiceListView.as_view(), name="clients_list"),
    path("clients/create/", ClientOfServiceCreate.as_view(), name="clients_create"),
    path("clients/update/<int:pk>/", ClientOfServiceUpdateView.as_view(), name="clients_update"),
    path("clients/delete/<int:pk>/", ClientOfServiceDeleteView.as_view(), name="clients_delete"),

    path("message/", MailingMessageListView.as_view(), name="mailing_message_list"),
    path("message/create/", MailingMessageCreate.as_view(), name="mailing_message_create"),
    path("message/update/<int:pk>/", MailingMessageUpdateView.as_view(), name="mailing_message_update"),
    path("message/delete/<int:pk>/", MailingMessageDeleteView.as_view(), name="mailing_message_delete"),
]
