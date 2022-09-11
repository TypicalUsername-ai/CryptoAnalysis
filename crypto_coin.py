class crypto:
    id = None
    symbol = None
    name = None
    def __init__(self, json):
        self.id = json["id"]
        self.symbol = json["symbol"]
        self.name = json["name"]

    def __str__(self) -> str:
        return (f"name: {self.name}, id: {self.id}, symbol: {self.symbol}")
