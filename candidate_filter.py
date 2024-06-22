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


def main():
    # Prompt the user for a keyword to filter
    keyword = input("Enter a keyword to filter candidates: ")

    # Prompt the user to select a site
    site = input("Enter the site to search (work.ua or robota.ua): ").strip().lower()

    # Define file paths depending on the selected site
    if site == "work.ua":
        input_file_path = "work_ua_parser_with_scores/resumes_from_work_ua.csv"
        output_file_path = "work_ua_parser_with_scores/filtered_candidates_from_work_ua.csv"
    elif site == "robota.ua":
        input_file_path = "robota_ua_parser_with_scores/resumes_from_robota_ua.csv"
        output_file_path = "robota_ua_parser_with_scores/filtered_candidates_from_robota_ua.csv"
    else:
        print("Invalid site selected. Please enter 'work.ua' or 'robota.ua'.")
        return

    # Perform candidate filtering
    filter_candidates_by_keyword(input_file_path, keyword, output_file_path)


if __name__ == "__main__":
    main()
