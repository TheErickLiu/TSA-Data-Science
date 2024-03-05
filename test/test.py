import requests
from collections import Counter

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YourAPIKeyHere"
headers = {
    'Content-Type': 'application/json',
}

current_stock_check = "GOOGL/Alphabet/Google"

def process_and_predict(file_path):
    responses = []  
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            votes = []  # List to hold the results of the five requests
            for _ in range(5):  # Make 5 requests per line
                data = {
                    "contents": [{
                        "parts": [{
                            "text": f"Based on the following statement, if the text indicates that {current_stock_check} is up, that the author believes that {current_stock_check} stock will perform well or outperform other companies, or that author invested money or has 'calls' into {current_stock_check}, then respond with 'true'. If the text indicates that {current_stock_check} is down, that author believes that {current_stock_check} stock will not perform well or will be outperformed by other companies, that the author  or has 'puts' or pulled money out of {current_stock_check}, then respond with 'false'. If neither can be determined, then respond with 'inconclusive'. Refer to this word legend when certain phrases appear: to the moon means up, YOLO means up, tendies means up, rocket emoji means up, hands emoji means down, bear emoji means down, bull emoji means up, Calls on {current_stock_check} means up, Puts on {current_stock_check} means down. Respond with only 'true', 'false', or 'inconclusive', No other words: {line}"
                        }]
                    }]
                }

                res = requests.post(url, headers=headers, json=data)
                
                # Check response status code before proceeding
                if res.status_code == 200:
                    try:
                        response_json = res.json()
                        ai_prediction = response_json["candidates"][0]["content"]["parts"][0]["text"].lower()
                        votes.append(ai_prediction)
                    except KeyError:
                        print("Error in processing response")
                else:
                    print(f"Error: Received status code {res.status_code}")

            # Calculate majority vote
            if votes:
                vote_count = Counter(votes)
                majority_vote = vote_count.most_common(1)[0][0]
                responses.append(majority_vote)
            else:
                responses.append("Error in requests")
    
    # Save the majority responses to a file
    with open('TestPredictions.txt', 'w', encoding='utf-8') as out_file:
        for response in responses:
            out_file.write(f"{response}\n")
            
    print("Predictions completed and saved to test.txt.")

file_path = 'testpost.txt'
process_and_predict(file_path)