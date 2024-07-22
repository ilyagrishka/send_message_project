from django.core.management.base import BaseCommand
import json
from django.conf import settings
import os

from service.models import ClientOfService, MailingMessage


class Command(BaseCommand):
    help = "загрузка данных в базу"

    @staticmethod
    def clear_all_data():
        ClientOfService.objects.all().delete()
        MailingMessage.objects.all().delete()

    def handle(self, *args, **options):
        client_for_create = []
        message_for_create = []

        for client in Command.json_read_client():
            client_for_create.append(
                ClientOfService(**client["fields"])
            )

        ClientOfService.objects.bulk_create(client_for_create)

        for message in Command.json_read_message():
            message_id = message["fields"]["client"]
            print(message_id)
            message["fields"]["client"] = ClientOfService.objects.get(pk=message_id)
            message_for_create.append(
                MailingMessage(**message["fields"])
            )

        MailingMessage.objects.bulk_create(message_for_create)

    @staticmethod
    def json_read_client():
        data = Command.read_json()
        return list(filter(lambda x: x.get("model") == "service.client", data))

    @staticmethod
    def json_read_message():
        data = Command.read_json()
        return list(filter(lambda x: x.get("model") == "service.message", data))

    @staticmethod
    def read_json():
        path = str(settings.BASE_DIR) + "/service/fixture/data.json"
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
