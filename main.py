from delays.api.alerts import GTFSAlertsFeed
import os


def main():
    alerts = GTFSAlertsFeed()
    alerts.service_alert()


if __name__ == "__main__":
    try:
        os.environ["API_KEY"]
        main()
    except Exception as error:
        print(error)
