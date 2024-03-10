import pprint
from multiclient import MultiClient


def main():
    with MultiClient({"PLN": "123456", "USD": "987654"}, "P4$$w0rd", mode="demo") as client:
        pprint.pprint(client.get_trades())


if __name__ == "__main__":
    main()
