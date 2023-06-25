import requests

# Counts for each answer the unique number of traders owning at least 1 YES share in a market with multiple answers.

####### CONFIG ##########
# Manifold Market API key
api_key = "YOUR_API_KEY_HERE"

# Contract-slug (the short name of the market in the url)
slug = "what-is-the-primary-value-users-get"

#########################

# API request headers
headers = {
    "Authorization": f"Key {api_key}",
}

# URL containing retrieve answer details
answer_url = f"https://manifold.markets/api/v0/slug/{slug}"

# URL containing bet details
bets_url = f"https://manifold.markets/api/v0/bets?contractSlug={slug}"

# API request headers
headers = {
    "Authorization": f"Key {api_key}",
}

# API request to get answer details
def get_answer_details(url):
    response = requests.get(url, headers=headers)
    return response.json()

# API request to get bets
def get_bets(url):
    response = requests.get(url, headers=headers)
    return response.json()

# Retrieve answer details
answer_details = get_answer_details(answer_url)
if "error" in answer_details:
    print("Error:", answer_details["error"])
    exit()

answers = get_answer_details(answer_url)["answers"]
bets = get_bets(bets_url)

# Dictionary to store answer details and filled YES bet count
answer_dict = {}

# Loop through each answer
for answer in answers:
    answer_id = answer["id"]
    answer_text = answer["text"]

    # URL to retrieve bets for the answer
    answer_bets_url = bets_url + f"&answerId={answer_id}"

    # Count unique traders with filled YES bets for the answer
    filled_yes_bets = set()
    for bet in bets:
        if bet["answerId"] == answer_id and bet["isFilled"] and bet["outcome"] == "YES":
            filled_yes_bets.add(bet["userId"])

    unique_trader_count = len(filled_yes_bets)

    # Add answer details and filled YES bet count to the dictionary
    answer_dict[answer_id] = {
        "answer_text": answer_text,
        "filled_yes_bet_count": unique_trader_count
    }

# Print answer details and filled YES bet count
print(f"Number of unique traders holding at least 1 YES share in market ({slug}) for each answer:")
print("")
for answer_id, answer_data in answer_dict.items():
    print(answer_data["filled_yes_bet_count"], " - ", answer_data["answer_text"])
    #print("Answer ID:", answer_id)
    #print("Answer Text:", answer_data["answer_text"])
    #print("Filled YES Bet Count:", answer_data["filled_yes_bet_count"])
