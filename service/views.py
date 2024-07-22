from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from service.models import MailingSettings, ClientOfService, MailingMessage
from django.utils.text import slugify


class MailingListView(ListView):
    model = MailingSettings
    template_name = "service/mailing_list.html"

    def get_queryset(self):
        return MailingSettings.objects.filter(owner=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "список рассылок"
        context["mailings_all"] = len(MailingSettings.objects.all())
        context["mailings_active"] = len(MailingSettings.objects.filter(status="started"))
        return context


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    success_url = reverse_lazy("service:mailing_list")

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    success_url = reverse_lazy("service:mailing_list")

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return object
        return PermissionDenied


class MailingSettingsDetailView(DetailView):
    model = MailingSettings

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.views_counter += 1
            self.object.save()
            return self.object
        raise PermissionDenied


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy("service:mailing_list")


class ClientOfServiceListView(ListView):
    model = ClientOfService
    template_name = "service/client_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_status=True)
        return queryset


class ClientOfServiceDetail(DetailView):
    model = ClientOfService
    template_name = "service/client_details.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ClientOfServiceCreate(CreateView):
    model = ClientOfService
    success_url = reverse_lazy("service:mailing_list")

    def form_valid(self, form):
        if form.is_valid():
            new_form = form.save()
            new_form.slug = slugify(new_form.name)
            new_form.save()

        return super().form_valid(form)


class ClientOfServiceUpdateView(UpdateView):
    model = ClientOfService

    success_url = reverse_lazy("service:mailing_list")


class ClientOfServiceDeleteView(DeleteView):
    model = ClientOfService
    success_url = reverse_lazy("service:mailing_list")


class MailingMessageListView(ListView):
    model = MailingMessage
    template_name = "service/message_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_status=True)
        return queryset


class MailingMessageDetail(DetailView):
    model = MailingMessage
    template_name = "service/message_details.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class MailingMessageCreate(CreateView):
    model = MailingMessage
    success_url = reverse_lazy("service:mailing_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage

    success_url = reverse_lazy("service:mailing_list")


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy("service:mailing_list")
