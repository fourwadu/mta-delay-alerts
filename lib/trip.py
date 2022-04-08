from gtfs.compiled import nyct_subway_pb2


class Trip:
    def __init__(self, update):
        self.update = update

    def parse_trip(self) -> dict:
        trip = self.update.trip_update

        return {
            "id": self.update.id,
            "trip_update": {
                "trip": {
                    "trip_id": trip.trip.trip_id,
                    "start_date": trip.trip.start_date,
                    "route_id": trip.trip.route_id
                },
            },
            "stop_time_update": [
                {
                    "stop_id": update.stop_id,
                    "arrival": update.arrival and update.arrival.time or None,
                    "departure": update.departure and update.departure.time or None
                } for update in trip.stop_time_update
            ],
            "type": "trip_update"
        }

    def parse_vehicle(self) -> dict:
        vehicle = self.update.vehicle
        trip = vehicle.trip
        trip_descriptor = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]

        return {
            "id": self.update.id,
            "vehicle": {
                "trip": {
                    "trip_id": trip.trip_id,
                    "start_time": trip.start_time,
                    "start_date": trip.start_date,
                    "route_id": trip.route_id,
                    "trip_descriptor": {
                        "train_id": trip_descriptor.train_id,
                        "is_assigned": trip_descriptor.is_assigned
                    }
                },
                "current_stop_sequence": vehicle.current_stop_sequence,
                "current_status": str(vehicle.current_status),
                "timestamp": vehicle.timestamp,
                "stop_id": vehicle.stop_id
            }
        }

    def parse_update(self) -> dict:
        if str(self.update.trip_update):
            return self.parse_trip()
        elif str(self.update.vehicle):
            return self.parse_vehicle()
