import json

API_BOOKMAKER = [
  12, # Pinnacle
  3, # 1xbet
  4, # bet365
  19, # Unibet
  26, # Williamhill
]

with open('api.json') as f:
  df = json.load(f)

for bookie in df['response'][0]['bookmakers']:
  # if bookie['id'] in API_BOOKMAKER:
    for idx, bets in enumerate(bookie['bets'][0]['values']):
      line = str(bets['value'])
      odd = float(bets['odd'])
      if odd >= 1.85 or odd <= 2:
        line = line.split(" ")[1]
        print("{} - {}".format(line, odd))
        break