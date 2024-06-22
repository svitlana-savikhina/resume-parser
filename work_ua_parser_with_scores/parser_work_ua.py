import csv
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup


def parse_resumes(soup):
    resume_blocks = soup.find_all(
        "div", class_="card card-hover card-search resume-link card-visited wordwrap"
    )
    resumes = []

    for block in resume_blocks:
        position_text = block.find("h2", class_="cut-top").text.strip()

        name_age_location_block = block.find("p", class_="add-top-xs cut-bottom")
        name_age_location = (
            name_age_location_block.text.strip().split(", ")
            if name_age_location_block
            else ["", "", ""]
        )
        name = name_age_location[0] if len(name_age_location) > 0 else ""

        age_str = (
            name_age_location[1].replace(" років", "")
            if len(name_age_location) > 1
            else ""
        )
        age = re.findall(r"\d+", age_str)[0] if re.findall(r"\d+", age_str) else ""

        location = name_age_location[2] if len(name_age_location) > 2 else ""

        salary_block = block.find(
            "p", class_="h5 strong-600 add-top-xs cut-bottom nowrap"
        )
        salary = salary_block.text.strip().replace("\xa0", " ") if salary_block else ""

        education_block = block.find("p", class_="cut-bottom add-top-xs text-default-7")
        education = education_block.text.strip() if education_block else ""
        education_words = education.split()[:2]
        education_ = " ".join(education_words)

        resumes.append(
            {
                "Position": position_text,
                "Name": name,
                "Age": age,
                "Location": location,
                "Expected_salary": salary,
                "Education": education_,
            }
        )

    return resumes


class ResumeParser:
    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.soup = None

    def fetch_html(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")

    def save_to_csv(self, resumes, filename="resumes_from_work_ua.csv"):
        fieldnames = [
            "Position",
            "Name",
            "Age",
            "Location",
            "Expected_salary",
            "Education",
        ]
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for resume in resumes:
                writer.writerow(resume)

    def parse_page(self, page):
        url = f"{self.url}?page={page}"
        soup = self.fetch_html(url)
        resumes = parse_resumes(soup)
        return resumes

    def parse_all_pages(self, max_pages=None, num_threads=10):
        all_resumes = []
        max_pages_num = 40000
        pages_to_parse = (
            range(1, max_pages + 1) if max_pages else range(1, max_pages_num)
        )

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_page = {
                executor.submit(self.parse_page, page): page for page in pages_to_parse
            }
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    resumes = future.result()
                    all_resumes.extend(resumes)
                    print(f"Page {page} parsed successfully")
                except Exception as exc:
                    print(f"Page {page} generated an exception: {exc}")

        return all_resumes


URL = "https://www.work.ua/resumes/"
parser = ResumeParser(URL)
all_resumes = parser.parse_all_pages(max_pages=100, num_threads=10)
parser.save_to_csv(all_resumes)
