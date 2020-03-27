#!/usr/bin/env python3
import json
import os


RAW_DATA_PATH = './raw_data'
DATA_PATH = "./data"

date_values = {}


def main():
    os.makedirs(DATA_PATH, exist_ok=True)
    load_cumulative_total_tests()
    load_total_persons()
    load_total_positive()
    save_csv()


def load_raw_dataset(dataset_name):
    filename = os.path.join(RAW_DATA_PATH, f"{dataset_name}.json")
    with open(filename, "r") as f:
        return json.loads(f.read())


def update_date_record(date_key, updates):
    date_record = date_values.get(date_key, {})
    date_record.update(updates)
    date_values[date_key] = date_record


def load_cumulative_total_tests():
    data = load_raw_dataset('js-cummulative-total-tests-data')['values']
    last_cumulative = 0
    for item in data:
        cumulative_value = item['y']
        daily_number = cumulative_value - last_cumulative
        last_cumulative = cumulative_value
        update_date_record(item['x'], {
            'daily_tests': daily_number,
            'cumulative_tests': cumulative_value
        })


def load_total_persons():
    data = load_raw_dataset('js-total-persons-data')['values']
    for item in data:
        update_date_record(item['x'], {'daily_positive': item['y']})


def load_total_positive():
    data = load_raw_dataset('js-cummulative-total-positive-table-data')['body']
    for item in data:
        update_date_record(item[0], {'cumulative_positive': item[1]})


def table_row(values):
    return ','.join([str(value) for value in values])


def save_csv():
    table = [table_row(['date', 'daily_tests', 'cumulative_tests', 'daily_positive', 'cumulative_positive'])]
    for date_key in date_values.keys():
        fields = date_values[date_key]
        table.append(table_row([date_key, fields['daily_tests'], fields['cumulative_tests'], fields['daily_positive'], fields['cumulative_positive']]))
    filename = os.path.join(DATA_PATH, f"tests_and_infected.csv")
    with open(filename, "w") as f:
        f.write('\n'.join(table))


if __name__ == "__main__":
    main()
