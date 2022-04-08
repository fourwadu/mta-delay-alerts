
from gtfs.compiled import nyct_subway_pb2
from gtfs.compiled import gtfs_realtime_pb2
from gtfs.compiled.gtfs_realtime_pb2 import FeedMessage
from requests import Request
import requests

import os

from lib.trip import Trip


class GTFSServiceFeed:
    def __init__(self):
        self.api_key = os.environ["API_KEY"]
        self.feed = None

    def request(self, line: str = None) -> Request:
        res = requests.get(
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs{}".format("-" + line if line else ""), headers={"x-api-key": self.api_key})

        res.raise_for_status()
        return res

    @staticmethod
    def _decode_bytes(gtfs_bytes) -> FeedMessage:
        feed = FeedMessage()
        feed.ParseFromString(gtfs_bytes)
        return feed

    @staticmethod
    def _route_id(entity: FeedMessage) -> str:
        return (entity.trip_update.trip.route_id)

    @staticmethod
    def _trip_identifier(trip_data) -> tuple:
        return (trip_data.Extensions[nyct_subway_pb2.nyct_trip_descriptor].train_id[-7:], trip_data.route_id)

    def trip_feed(self) -> None:
        self.refresh()
        trip_updates = []
        for entity in self.feed:
            if entity.HasField("trip_update"):
                trip_updates.append(Trip(entity).parse_update())

        return trip_updates

    def vehicle_feed(self) -> dict:
        self.refresh()
        vehicle_updates = []
        for entity in self.feed:
            if entity.HasField("vehicle"):
                vehicle_updates.append(Trip(entity).parse_update())

        return vehicle_updates

    def refresh(self, line: str = None):
        r = self.request(line)
        feed = self._decode_bytes(r.content)
        self.feed = feed.entity

    def filter_feed(self, line: str = None):
        self
