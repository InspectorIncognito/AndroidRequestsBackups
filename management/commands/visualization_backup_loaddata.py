from django.core.management.base import BaseCommand
from django.core import serializers


class Command(BaseCommand):

    def handle(self, *args, **options):

        to_transform = [
            'dump_Report.json',
            'dump_EventForBusStop.json',
            'dump_EventForBusv2.json',
            'dump_Busv2.json'
        ]

        # we must load the files in order!
        list_json = [
            'dump_Report.json',
            'dump_EventForBusStop.json',
            'dump_StadisticDataFromRegistrationBusStop.json',
            'dump_EventForBusv2.json',
            'dump_StadisticDataFromRegistrationBus.json',
            'dump_Busassignment.json',
            'dump_Busv2.json'
        ]

        for filename in list_json:
            mark_for_transform = True if filename in to_transform else False
            self.from_JSON(self.save_to_database_cb, filename, mark_for_transform)
            # self.from_JSON(self.print_cb, filename)


    def from_JSON(self, callback, filename, mark_for_transform):
        print("loading data from: " + filename)
        cnt = 0
        with open(filename, 'r') as file:
            for deserialized_object in serializers.deserialize("json", file, ignorenonexistent=True):
                if mark_for_transform:
                    deserialized_object.object.transformed = False

                callback(deserialized_object)
                cnt += 1
        print(" . . . loaded " + str(cnt) + " rows.")


    def save_to_database_cb(self, deserialized_object):
        deserialized_object.save()

    def print_cb(self, deserialized_object):
        print(deserialized_object.object)
