from lib.service.feed import GTFSServiceFeed
import os


def main():
    feed = GTFSServiceFeed()
    feed.refresh("ace")


if __name__ == "__main__":
    try:
        os.environ["API_KEY"]
        main()
    except Exception as error:
        print(error)
