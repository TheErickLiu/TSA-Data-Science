from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import json


def get_datetime(
    datetime_file_path: str, stock: str = ""
) -> List[Tuple[str, str]]:
    date_list = []
    counter = 0

    with open(datetime_file_path, "r", encoding="utf-8") as date_file:
        for line in date_file:
            date, time = line.strip().split()[-2:]
            time = time[:-1]
            date_list.append((date, time))
            counter += 1

        print(stock, counter, "records loaded")

    return date_list


def get_winner(sentiment_file_path: str) -> List[str]:
    winner_list = []

    with open(sentiment_file_path, "r", encoding="utf-8") as sent_file:
        for line in sent_file:
            sentiment = (
                line.strip()
                .replace("[", "")
                .replace("]", "")
                .replace(" ", "")
                .replace("'", "")
                .split(",")
            )
            winner = Counter(sentiment).most_common(1)[0][0]
            winner_list.append(winner)

    return winner_list


def get_price(price_path: str) -> Dict[str, List]:
    price_dict = {}

    with open(price_path, "r", encoding="utf-8") as price_file:
        for line in price_file:
            rec = line.strip().split(",")
            price_dict[rec[0]] = rec[1:]  # date as key, prices list as value

    return price_dict


def get_sentiment_list(
    datetime_list: List[Tuple[str, str]], winner_list: List[str]
) -> List[List[str]]:
    sent_list = []
    for i, sent in enumerate(datetime_list):
        sent_list.append([sent[0], sent[1], winner_list[i]])
    return sent_list


def get_prev_date(date: str):
    from datetime import datetime, timedelta

    date = datetime.strptime(date, "%Y-%m-%d")
    date = date - timedelta(days=1)
    return date.strftime("%Y-%m-%d")


def get_price_for_date(date: str, price_dict: Dict[str, List]) -> List[str]:
    if date in price_dict:
        return price_dict[date]
    else:
        prev_date = date
        for _ in range(2):  # try 2 days back for weekends
            prev_date = get_prev_date(prev_date)
            # print(date, prev_date)
            if prev_date in price_dict:
                return price_dict[prev_date]

    return ["", "", "", "", "", ""]


def combine_sentiment_and_price(
    sentiment_list: List[List[str]],
    price_dict: Dict[str, List],
) -> List[List[str]]:

    for i, sent in enumerate(sentiment_list):
        date = sent[0]
        sent.extend(date.split("-"))
        sent.extend(get_price_for_date(date, price_dict))

    return sentiment_list


def collapse_sentiment_by_date(
    sentiment_list: List[List[str]],
) -> List[List[str]]:

    combined_dict = defaultdict(list)
    price_dict = defaultdict(list)

    for i, sent in enumerate(sentiment_list):
        (date, time, winner) = sent[:3]
        price_dict[date] = sent[3:]

        if date not in combined_dict:
            combined_dict[date] = defaultdict(list)
        if winner not in combined_dict[date]:
            combined_dict[date][winner] = set()
        combined_dict[date][winner].add(time)

    combined_list = []
    for date in combined_dict:
        counts = []
        for v in ["true", "false", "inconclusive"]:
            cnt = 0
            if v in combined_dict[date]:
                cnt = len(combined_dict[date][v])
            counts.append(str(cnt))
        rec = [date] + counts + price_dict[date]
        combined_list.append(rec)

    return combined_list


def write_header(outfilename: str) -> None:
    header = [
        "stock",
        "date",
        "time",
        "sentiment",
        "year",
        "month",
        "day",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]
    with open(outfilename, "w") as outfile:
        outfile.write(",".join(header) + "\n")


def append_to_file(
    stock: str, outfilename: str, combined_list: List[str], sep: str = ","
) -> None:
    with open(outfilename, "a") as outfile:
        for rec in combined_list:
            outline = sep.join([stock] + [str(v) for v in rec])
            outfile.write(outline + "\n")


def write_collapsed_dataset(
    collapsed_dataset: Dict[str, List[List[str]]], outfilename: str
) -> None:

    with open(outfilename, "w") as outfile:
        header = [
            "stock",
            "date",
            "senti_raise",
            "senti_drop",
            "senti_inconclusive",
            "year",
            "month",
            "day",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
        outfile.write(",".join(header) + "\n")

    for stock in collapsed_dataset:
        append_to_file(stock, outfilename, collapsed_dataset[stock])


def combine_datasets(
    dataset_json, outfilename: str, base_dir: str = "."
) -> dict:

    with open(dataset_json, "r") as f:
        datasets = json.load(f)

    write_header(f"{base_dir}/{outfilename}")

    collapsed_dataset = defaultdict(list)

    for stock, paths in datasets.items():
        datetime_list = get_datetime(
            f"{base_dir}/{paths['date_file_path']}", stock
        )
        winner_list = get_winner(f"{base_dir}/{paths['sentiment_file_path']}")
        price_dict = get_price(f"{base_dir}/{paths['price_file_path']}")
        sentiment_list = get_sentiment_list(datetime_list, winner_list)
        combined_list = combine_sentiment_and_price(sentiment_list, price_dict)
        collapsed_dataset[stock] = collapse_sentiment_by_date(combined_list)
        write_header(f"{base_dir}/{paths['outfilename']}")
        append_to_file(
            stock, f"{base_dir}/{paths['outfilename']}", combined_list
        )
        append_to_file(stock, f"{base_dir}/{outfilename}", combined_list)

    return collapsed_dataset


def main():

    base_dir = "data"
    dataset_json = "data/datasets.json"
    outfilename = "combinedData/combined.csv"
    ds = combine_datasets(dataset_json, outfilename, base_dir)
    write_collapsed_dataset(ds, f"{base_dir}/combinedData/collapsed.csv")


if __name__ == "__main__":
    main()
