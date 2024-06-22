import csv

input_filename = "robota_ua_parser_with_scores/resumes_from_robota_ua.csv"
output_filename = "robota_ua_parser_with_scores/resumes_from_robota_ua_with_scores.csv"

age_lower_limit = 25
age_upper_limit = 45


# Open the CSV file for reading and create a new CSV file for writing with scores
with open(input_filename, mode="r", encoding="utf-8") as input_file, open(
        output_filename, mode="w", newline="", encoding="utf-8"
) as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Write the header for the new file with scores
    header = next(reader)
    header.append("Scores")
    writer.writerow(header)

    # Iterate over each record in the input file
    for row in reader:
        # Count the number of filled fields (non-empty values)
        filled_fields_count = sum(1 for field in row if field)

        # Initialize variables for additional bonuses

        age_bonus = 0

        # If the age is between 25 and 45, add an additional bonus point
        age = int(row[2]) if row[2].isdigit() else None
        if age and 25 <= age <= 45:
            age_bonus = 1

        # Calculate the candidate's score based on the number of filled fields and additional bonuses
        score = filled_fields_count + age_bonus

        row.append(score)
        writer.writerow(row)

print("File with scores successfully created")
