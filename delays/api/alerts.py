from urllib.request import Request
from gtfs import gtfs_realtime_pb2
import requests
from datetime import datetime
import os


class GTFSAlertsFeed:

    def __init__(self):
        self.api_key = os.environ["API_KEY"]
        self.feed = None

    def request(self) -> Request:
        res = requests.get(
            f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts", headers={"x-api-key": self.api_key})

        if res.status_code == 403:
            raise RuntimeError("Invalid API_KEY")
        elif res.status_code > 200:
            raise RuntimeError("Invalid Response", res.content)
        return res

    @staticmethod
    def _parse_gtfs(gtfs_bytes) -> gtfs_realtime_pb2.FeedMessage:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(gtfs_bytes)
        return feed

    @staticmethod
    def _alert_timestamp(entity: gtfs_realtime_pb2.FeedMessage):
        periods = entity.alert.active_period
        return [{"start": period.start, "end": period.end} for period in periods]

    @staticmethod
    def _alert_text(entity: gtfs_realtime_pb2.FeedMessage) -> str:
        if entity.HasField("header_text"):
            print("No entity")
        return entity.alert.header_text.translation[0].text

    @staticmethod
    def _route_id(entity: gtfs_realtime_pb2.FeedMessage) -> str:
        return (entity.alert.informed_entity[0].route_id)

    def alerts(self):
        alerts = {}
        for alert in self.feed:
            # have to check alert informed entity
            # may be stop_id, or line_id

            alerts[self._route_id(alert)] = {
                "text": self._alert_text(alert),
                # TODO: functions for checking stop_id, line_id
                "stop_id": None,
                "line_id": None,
                "time": self._alert_timestamp(alert)
            }

        print(alerts)

    def service_alert(self):
        r = self.request()
        feed = self._parse_gtfs(r.content)
        self.feed = feed.entity
        print(self.feed)

        self.alerts()
