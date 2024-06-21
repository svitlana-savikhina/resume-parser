import csv


def filter_candidates_by_keyword(input_file_path, keyword, output_file_path):
    filtered_candidates = []

    with open(input_file_path, mode="r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        header = next(reader)

        # Iterate over each record in the input file
        for row in reader:
            # Check if the keyword is present in any field of the candidate's record
            if any(keyword.lower() in field.lower() for field in row):
                filtered_candidates.append(row)

    # Write filtered candidates to a new CSV file
    with open(output_file_path, mode="w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)
        writer.writerows(filtered_candidates)


keyword = "продавець"
input_file_path = "robota_ua_parser_with_scores/resume_from_robota_ua.csv"
output_file_path = "robota_ua_parser_with_scores/filtered_candidates_from_robota_ua.csv"
filter_candidates_by_keyword(input_file_path, keyword, output_file_path)

print(f"Filtered candidates by keyword '{keyword}' saved to {output_file_path}")
