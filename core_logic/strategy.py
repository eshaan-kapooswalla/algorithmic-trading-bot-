class TradingStrategy:
    """Base class for trading strategies."""
    def __init__(self):
        pass

    def generate_signals(self, data):
        """Implement your signal generation logic here."""
        raise NotImplementedError 