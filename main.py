import requests
from fake_headers import Headers
import bs4
import json

headers = Headers(browser="firefox", os="win")
headers_data = headers.generate()

main_page_html = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers_data).text
main_page_soup = bs4.BeautifulSoup(main_page_html, "lxml")


div_vacancy_list_tag = main_page_soup.find("main", class_="vacancy-serp-content")
vacancy_tags = div_vacancy_list_tag.find_all("div", class_="vacancy-serp-item__layout")
parsed_vacancy = {}
parsed_vacancy['vacancy'] = []


def parse_vacancy():
    for vacancy_tag in vacancy_tags:
        h3_tag = vacancy_tag.find("h3")
        title = h3_tag.text

        a_tag = h3_tag.find("a")
        link = f'{a_tag["href"]}'

        headers_data = headers.generate()

        company_name_tag = vacancy_tag.find("div", class_="bloko-text")
        company_name = company_name_tag.text

        salary_tag = vacancy_tag.find("span", class_="bloko-header-section-3")
        if salary_tag is None:
            salary = "Зарплата не указана!"
        else:
            salary = salary_tag.text

        city_tag = vacancy_tag.find("div", class_="vacancy-serp-item__info")
        city = city_tag.find_all("div", class_="bloko-text")
        city_name = city[1].text.split(",")[0]

        vacancy_page_html = requests.get(link, headers=headers_data).text
        vacancy_page_soup = bs4.BeautifulSoup(vacancy_page_html, "lxml")

        description_tag = vacancy_page_soup.find("div", class_="vacancy-description")
        description = description_tag.find("div", class_="g-user-content")
        if description is None:
            continue

        key_words = ["Django", "Flask"]

        if key_words[0] in description.text or key_words[1] in description.text or (key_words[0] in description.text and key_words[1] in description.text):
            parsed_vacancy['vacancy'].append({
                "vacancy name": title,
                "link": link,
                "salary": salary,
                "company name": company_name,
                "city": city_name
            })

        with open("parsed_vacancy.txt", "w", encoding='utf-8') as outfile:
            json.dump(parsed_vacancy, outfile, ensure_ascii=False, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    parse_vacancy()
