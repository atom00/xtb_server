from XTBApi.api import BaseClient


class MultiClient:
    def __init__(self, account_ids: dict, password: str, mode: str):
        self.account_ids = account_ids
        self.password = password
        self.mode = mode
        self.clients = dict()

    def __enter__(self):
        for label, account_id in self.account_ids.items():
            self.clients[label] = BaseClient()
            self.clients[label].login(account_id, self.password, self.mode)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for client in self.clients.values():
            client.logout()

    def get_trades(self):
        retval = dict()

        def _reduce(portfolio):
            reduced_trades = dict()
            for trade in portfolio:
                symbol = trade["symbol"]
                if symbol in reduced_trades:
                    assert reduced_trades[symbol]["close_price"] == trade["close_price"]
                    reduced_trades[symbol]["volume"] += trade["volume"]
                else:
                    reduced_trades[symbol] = trade

            return reduced_trades.values()

        for label, client in self.clients.items():
            trades = client.get_trades()
            trades = list(map(lambda trade: dict(filter(lambda item: item[0] in ("symbol", "volume", "close_price"), trade.items())), trades))
            retval[label] = _reduce(trades)

        return retval
