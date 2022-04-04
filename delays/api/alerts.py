from gtfs import gtfs_realtime_pb2
from requests import Request, requests
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
        return entity.alert.header_text.translation[0].text

    @staticmethod
    def _stop_id(entity: gtfs_realtime_pb2.FeedMessage) -> str or None:
        return entity.alert.informed_entity[0].stop_id

    @staticmethod
    def _route_id(entity: gtfs_realtime_pb2.FeedMessage) -> str or None:
        return (entity.alert.informed_entity[0].route_id) or None

    def alerts(self):
        alerts = {}
        for alert in self.feed:
            train_id = self._route_id(alert)
            if train_id not in alerts:
                alerts[train_id] = []

            alerts[train_id].append({
                "text": self._alert_text(alert),
                "stop_id": self._stop_id(alert),
                "time": self._alert_timestamp(alert)
            })

    def service_alert(self):
        r = self.request()
        feed = self._parse_gtfs(r.content)
        self.feed = feed.entity
        self.alerts()
