import os
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from discord_webhook import DiscordWebhook

# Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
client = gspread.authorize(CREDS)

# Discord webhook URL from environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def trade():
    sheet = client.open("TradingParameters").sheet1
    params = sheet.get_all_records()
    
    short_sma = int(params[0]['Value'])
    long_sma = int(params[1]['Value'])
    initial_amount = float(params[2]['Value'])
    current_balance = float(params[3]['Value'])

    # Simulate market data and trading logic
    market_data = [random.uniform(90, 110) for _ in range(100)]
    short_sma_value = sum(market_data[:short_sma]) / short_sma
    long_sma_value = sum(market_data[:long_sma]) / long_sma

    if short_sma_value > long_sma_value:
        profit = current_balance * 0.10
        current_balance += profit
    elif short_sma_value < long_sma_value:
        loss = current_balance * 0.05
        current_balance -= loss

    # Update Google Sheet
    sheet.update_cell(4, 2, current_balance)

    # Send update to Discord
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=f"New balance: ${current_balance:.2f}")
    webhook.execute()

    return f"Trade executed. New balance: ${current_balance:.2f}"

if __name__ == "__main__":
    trade()
