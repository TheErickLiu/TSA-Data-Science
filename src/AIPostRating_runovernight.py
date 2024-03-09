import requests
from collections import Counter

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=imagineKeyHere"
headers = {
    'Content-Type': 'application/json',
}

def process_and_predict(file_path, stock_check, company_name):
    print(f"Starting for {company_name}")
    counter = 0
 
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            counter += 1
            print(f"Line #{counter} started")
            votes = []
            for _ in range(7):
                data = {
                    "contents": [{
                        "parts": [{
                            "text": f"Based on the following statement, if the text indicates that {stock_check} is up, that the author believes that {stock_check} stock will perform well or outperform other companies, or that author invested money or has 'calls' into {stock_check}, then respond with 'true'. If the text indicates that {stock_check} is down, that author believes that {stock_check} stock will not perform well or will be outperformed by other companies, that the author  or has 'puts' or pulled money out of {stock_check}, then respond with 'false'. If neither can be determined, then respond with 'inconclusive'. Refer to this word legend when certain phrases appear: to the moon means up, YOLO means up, tendies means up, rocket emoji means up, hands emoji means down, bear emoji means down, bull emoji means up, Calls on {stock_check} means up, Puts on {stock_check} means down. Respond with only 'true', 'false', or 'inconclusive', No other words: {line}"
                        }]
                    }]
                }

                #print(f"Round #{_ + 1} started")
                res = requests.post(url, headers=headers, json=data)
                
                # Check response status code before proceeding
                if res.status_code != 200:
                    print(f"Error: Received status code {res.status_code}")
                    print("Response content:", res.text)
                    continue  # Skip processing this line and move to the next one
                
                try:
                    response_json = res.json()
                    ai_prediction = response_json["candidates"][0]["content"]["parts"][0]["text"]
                    if "true" in ai_prediction.lower():
                        post_grade = "true"
                    elif "false" in ai_prediction.lower():
                        post_grade = "false"
                    else:
                        post_grade = "inconclusive"
                
                except KeyError as e:
                    print(f"KeyError: {e} - prompt/prompt feedback was either sexually explicit, hate speech, harrassment, or dangerous in some way")

                #counter += 1
                #print(f"Response received: {counter}, {post_grade}")
                print(f"Round {_+1} winner: {post_grade}")
                votes.append(post_grade)
                current_item_counts = Counter(votes)
                current_most_common = current_item_counts.most_common(1)
                if current_most_common:
                    final_vote, count = current_most_common[0]
                    if count >= 4:
                        break

            #print(votes)
            #item_counts = Counter(votes)

            #most_common = item_counts.most_common(1)

            #if most_common:
                #final_vote, count = most_common[0]
                #print(f"Line {counter} ended: {final_vote}")
                #responses.append(final_vote)

            with open(f'ratedData/{company_name}Predictions.txt', 'a', encoding='utf-8') as out_file:
                out_file.write(f"{votes}\n")
            
    print(f"Predictions completed and saved to ratedData/{company_name}Predictions.txt.")

stock_checks = ["AMZN/Amazon", "AAPL/Apple", "META/Meta platforms", "MSFT/Microsoft", "NVDA/Nvidia", "TSLA/Tesla"]
company_names = ["Amazon", "Apple", "Meta", "Microsoft", "Nvidia", "Tesla"]

for i in range(len(stock_checks)):
    process_and_predict(f'scrubbedData/scrubbed{company_names[i]}.txt', stock_checks[i], company_names[i])