import yfinance as yf
import nltk
from nltk.chat.util import Chat, reflections


# Download the punkt tokenizer for basic NLP tasks
nltk.download('punkt')

# Define a simple chatbot for user interaction
pairs = [
    (r'what is the stock price of infosis', ['I can help with that! Let me check the stock price of %1.']),
    (r'how is my portfolio doing?', ['Let me show you your portfolio summary.']),
    (r'add stock coal india', ['Got it! Adding %1 to your portfolio.']),
    (r'quit|exit', ['Goodbye! Come back soon.']),
    (r'(.*)', ['Sorry, I didn’t quite understand that. Could you rephrase?'])
]

chatbot = Chat(pairs, reflections)

class StockPortfolio:
    def __init__(self):
        # Portfolio initialized as an empty dictionary (symbol: [shares, purchase price])
        self.portfolio = {}

    def add_stock(self, symbol, shares, price):
        """Add stock to portfolio."""
        self.portfolio[symbol] = [shares, price]

    @staticmethod
    def get_stock_price(symbol):
        """Fetch the real-time stock price from Yahoo Finance."""
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        current_price = stock_info['Close'].iloc[0]
        return current_price

    def portfolio_summary(self):
        """Return portfolio summary including current value and profit/loss."""
        summary = {}
        total_value = 0
        total_investment = 0
        for symbol, (shares, purchase_price) in self.portfolio.items():
            current_price = self.get_stock_price(symbol)
            current_value = current_price * shares
            profit_loss = (current_value - (purchase_price * shares))

            summary[symbol] = {
                'shares': shares,
                'purchase_price': purchase_price,
                'current_price': current_price,
                'current_value': current_value,
                'profit_loss': profit_loss
            }

            total_value += current_value
            total_investment += purchase_price * shares

        total_profit_loss = total_value - total_investment
        summary['total_value'] = total_value
        summary['total_profit_loss'] = total_profit_loss

        return summary

    def display_portfolio(self):
        """Print the portfolio in a readable format."""
        summary = self.portfolio_summary()
        for symbol, data in summary.items():
            if symbol not in ['total_value', 'total_profit_loss']:
                print(f"Stock: {symbol}")
                print(f"  Shares: {data['shares']}")
                print(f"  Purchase Price: ${data['purchase_price']}")
                print(f"  Current Price: ${data['current_price']}")
                print(f"  Current Value: ${data['current_value']}")
                print(f"  Profit/Loss: ${data['profit_loss']}")
                print("-" * 40)

        print(f"Total Portfolio Value: ${summary['total_value']}")
        print(f"Total Profit/Loss: ${summary['total_profit_loss']}")


def start_portfolio_tracker():
    portfolio = StockPortfolio()

    print("Stock Portfolio Tracker: How can I help you? (Type 'exit' to quit.)")

    while True:
        user_input = input("You: ")

        # If user asks for stock price
        if "stock price of" in user_input:
            stock_symbol = user_input.split("stock price of")[1].strip()
            price = portfolio.get_stock_price(stock_symbol)
            print(f"The current price of {stock_symbol} is ${price:.2f}")

        # If user asks for portfolio summary
        elif "how is my portfolio doing?" in user_input:
            portfolio.display_portfolio()

        # If user wants to add a stock to the portfolio
        elif "add stock" in user_input:
            parts = user_input.split("add stock")[1].strip().split()
            symbol = parts[0].upper()
            shares = int(parts[1])
            price = float(parts[2])

            portfolio.add_stock(symbol, shares, price)
            print(f"{symbol} added to your portfolio.")

        # Chatbot interaction
        elif user_input.lower() == 'exit' or user_input.lower() == 'quit':
            print("Goodbye! Have a great day.")
            break

        else:
            response = chatbot.respond(user_input)
            print(f"Chatbot: {response}")


if __name__ == "__main__":
    start_portfolio_tracker()
