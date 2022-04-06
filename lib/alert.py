class Alert:
    def __init__(self, alert):
        self.alert = alert.alert

        self.data = {
            "timestamp": self._alert_timestamp(),
            "text": self._alert_text(),
            "stop_id": self._stop_id(),
            "route_id": self._route_id(),
        }

    def _alert_timestamp(self):
        periods = self.alert.active_period
        return [{"start": period.start, "end": period.end} for period in periods]

    def _alert_text(self) -> str:
        return self.alert.header_text.translation[0].text

    def _stop_id(self) -> str or None:
        for entity in self.alerts.informed_entity:
            return entity

    def _route_id(self) -> str or None:
        for e in self.alert.informed_entity:
            if e.route_id:
                return e.route_id
