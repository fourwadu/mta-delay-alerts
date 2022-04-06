from gtfs.compiled import gtfs_realtime_pb2, nyct_subway_pb2
from gtfs.compiled.gtfs_realtime_pb2 import FeedMessage
from requests import Request
import requests
from ..alert import Alert
import os


class GTFSAlertsFeed:
    def __init__(self):
        self.api_key = os.environ["API_KEY"]
        self.feed = None

    def request(self) -> Request:
        res = requests.get(
            f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts", headers={"x-api-key": self.api_key})

        res.raise_for_status()
        return res

    @staticmethod
    def _decode_bytes(gtfs_bytes) -> FeedMessage:
        feed = FeedMessage()
        feed.ParseFromString(gtfs_bytes)
        return feed

    @staticmethod
    def _route_id(entity) -> str or None:
        for e in entity.alert.informed_entity:
            if e.route_id:
                return e.route_id

    def alerts(self):
        alerts = {}
        for alert in self.feed:
            train_id = self._route_id(alert)

            if train_id not in alerts:
                alerts[train_id] = []

            alerts[train_id].append(Alert(alert).data)
        return alerts

    def refresh(self):
        r = self.request()
        feed = self._decode_bytes(r.content)
        self.feed = feed.entity
        alerts = self.alerts()
        print(alerts)
