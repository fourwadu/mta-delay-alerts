from lib.service.feed import GTFSServiceFeed
from lib.service.alerts import GTFSAlertsFeed
import os


def main():
    feed = GTFSServiceFeed()
    feed.refresh("ace")
    # feed = GTFSAlertsFeed()
    # feed.refresh()


if __name__ == "__main__":
    try:
        os.environ["API_KEY"]
        main()
    except Exception as error:
        print(error)
