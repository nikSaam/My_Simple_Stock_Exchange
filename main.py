from exchange import Exchange
from cli import run_cli


def main():
    exchange = Exchange()
    run_cli(exchange)


if __name__ == "__main__":
    main()
