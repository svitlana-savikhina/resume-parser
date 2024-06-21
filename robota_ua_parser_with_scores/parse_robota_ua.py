import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

url = "https://robota.ua/ru/candidates/all/ukraine"


def process_page(driver, page_num):
    driver.get(f"{url}?page={page_num}")
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    # print(soup.prettify())

    resumes = []

    resume_containers = soup.find_all("section", class_="cv-card")

    for container in resume_containers:
        position, name, age, location, percentage = "", "", "", "", ""

        position_elem = container.find(
            "p", class_="santa-m-0 santa-typo-h3 santa-pb-10").text.strip()

        name = container.find(
            "p", class_="santa-pr-20 santa-typo-regular santa-truncate"
        ).get_text(strip=True)

        div_element = container.find(
            "div",
            class_="santa-flex santa-items-center santa-space-x-10 santa-pr-20 "
                   "santa-whitespace-nowrap",
        )
        if div_element:
            age_elem = div_element.find("p", class_="santa-typo-secondary")
            if age_elem:
                age = age_elem.get_text(strip=True).split()[0]
            else:
                print("Age element not found")

        location_elem = container.find(
            "p", class_="santa-typo-secondary santa-truncate"
        )
        if location_elem:
            location = location_elem.get_text(strip=True)
        else:
            print("Location element not found")

        percentage_classes = [
            "santa-text-yellow-500",
            "santa-text-green-600",
            "santa-text-green-500",
        ]

        percentage_elem = None
        for cls in percentage_classes:
            percentage_elem = container.find(
                "div",
                class_=f"760:santa-mt-10 santa-inline-block santa-leading-30 "
                       f"santa-text-14 {cls}",
            )
            if percentage_elem:
                break

        if percentage_elem:
            percentage_text = percentage_elem.get_text(strip=True)
            percentage_match = re.search(r"\d+%", percentage_text)
            if percentage_match:
                percentage = percentage_match.group()

        resumes.append(
            {
                "Position": position_elem,
                "Name": name,
                "Age": age,
                "Location": location,
                "Percentage": percentage,
            }
        )

    return resumes


def scrape_resume_data():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        max_pages = 4
        num_threads = 2

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            all_resumes = []
            for page_num in range(1, max_pages + 1):
                future = executor.submit(process_page, driver, page_num)
                all_resumes.append(future.result())

        return all_resumes

    finally:
        driver.close()


if __name__ == "__main__":
    resumes = scrape_resume_data()

    with open("./resumes_from_robota_ua.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Position", "Name", "Age", "Location", "Percentage"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for page_resumes in resumes:
            for resume in page_resumes:
                writer.writerow(resume)
