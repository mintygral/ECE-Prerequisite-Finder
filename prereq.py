import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def main():
    # read csv
    data = pd.read_csv("ece-undergrad-courses.csv")

    # get course number
    course_number = int(input("Enter a course number: "))

    # hurr durr
    found = False
    for num, url, title in zip(data["Course Number"], data["URL"], data["Title"]):
        if num == course_number:
            found = True
            break

    if found:
        print(f"Course ECE {course_number}: {title} exists in the data.\n")
        print(f"The corresponding url is {url}.\n")
        requisites = get_requisites(url)
        if requisites:
          print(f"Requisites: {requisites}")
        else:
          print("Requisites not found.")
    else:
        print(f"Course number {course_number} not found in the data.")

def get_requisites(url):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')

    # find element containing requisites
    requisites_element = soup.find('h3', string='Requisites:')
    
    if requisites_element:
        # find prereq
        requisites_text = requisites_element.find_next_sibling('p')
        
        if requisites_text:
            # get the text content without the <p> tag
            prerequisites = requisites_text.get_text(strip=True)
            return prerequisites
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    main()
