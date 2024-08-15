# json to csv

import json
import csv

def convert_json_to_csv(table):
    with open(f'./data/{table}.json', 'r') as json_file:
        data = json.load(json_file)

    # open a csv file for writing
    with open(f'./data/{table}.csv', 'w', newline='') as csv_file:

        csv_writer = csv.writer(csv_file)

        # write the header
        header = data[f'{table}'][0].keys()
        csv_writer.writerow(header)

        # write the data rows
        for course in data[f'{table}']:
            row = []
            for key, value in course.items():
                if isinstance(value, list):
                    row.append('; '.join(str(item) for item in value))
                else:
                    row.append(str(value))
            csv_writer.writerow(row)

    print('CSV file has been created successfully.')

convert_json_to_csv('teachers')
##convert_json_to_csv('course_teachers')
##convert_json_to_csv('faq')
##convert_json_to_csv('course_topics')
