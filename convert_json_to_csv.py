import json
import csv

headers = ['ico_url', 'Name', 'Investment rating', 'Hype score', 'Risk score', 'Pre-ICO start date',
          'Pre-ICO end date', 'Pre-ICO Token Supply', 'ICO start date', 'ICO end date', 'ICO Token Supply',
          'Hard cap', 'Hard cap size', 'Soft cap', 'Soft cap size', 'Dividends', 'BTC', 'ETH', 'USD', 'Post-ICO',
          'Ticker', 'Type', 'Token Standard', 'Additional Token Emission', 'Token price in BTC',
          'Token price in ETH', 'Token price in USD', 'Accepted Currencies', 'Token distribution',
          'Funds allocation', 'ICO Platform', 'Country Limitations', 'Registration Country',
          'Registration Year', 'Office adress', 'Website', 'btctalk', 'Linkedin', 'Twitter', 'Facebook',
          'Instagram', 'Telegram', 'Youtube', 'Steemit', 'Reddit', 'Medium', 'Slack', 'Google Play',
          'App store', 'Github']

with open('<import_json_file>.json', encoding="utf8") as json_file:
    parsed_json = json.load(json_file)

# headers = []
## collect all available attributes
# for item in sorted(parsed_json, key=len, reverse=True):
#     for key in item.keys():
#         if key not in headers:
#             headers.append(key)

with open('<export_csv_file>.csv', 'w', newline='', encoding="utf8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()

    for item in parsed_json:
        writer.writerow(item)
