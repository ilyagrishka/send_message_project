from django.forms import ModelForm, BooleanField
from service.models import ClientOfService, MailingMessage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class ClientOfServiceForm(ModelForm):
    class Meta:
        model = ClientOfService
        fields = "__all__"
        exclude = ("comments", "owner")


class ProductModeratorForm(ModelForm):
    class Meta:
        model = ClientOfService
        fields = ("email", "full_name")


class MailingMessageForm(ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ("owner",)
        fields = "__all__"
