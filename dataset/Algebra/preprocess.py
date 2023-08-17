import csv
import json


def read_csv_to_dict(filename):
    data_list = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if "question" in row and "final_answer" in row:
                data_list.append(
                    {"question": row["question"], "answer": float(row["final_answer"]), "idx": i})
    return data_list


if __name__ == '__main__':
    filename = "dataset/Algebra/input/test.origin.csv"
    data = read_csv_to_dict(filename)
    with open('./dataset/Algebra/input/test.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
