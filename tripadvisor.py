import requests
from trip_settings import url, headers
from bs4 import BeautifulSoup
import json 

def get_tripadvisor_html(url):
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		print("requests exitoso")
		return response.text
	else: 
		print("Error en requests")
		return None 


def urls_por_pagina(url, paginas):
	urls = []
	for i in range(paginas):
		if i == 0:
			urls.append(url)
		else:
			offset = i * 30
			salto = url.replace("-Hotels.html", f"-oa{offset}-Hotels.html")
			urls.append(salto)
	return urls

def parser_html(html):
	soup = BeautifulSoup(html, "html.parser")
	hotels_list = []
	hotels = soup.find_all('div', class_="rlqQt _T A")
	for hotel in hotels:
		name_tag = hotel.find('h3', class_ = "biGQs _P fiohW fOtGX")
		name = name_tag.get_text(strip = True)  if name_tag else "No name"
		score_tag = hotel.find('div', attrs = {"data-automation": "bubbleRatingValue"})
		score = score_tag.get_text(strip = True) if score_tag else "No score"
		reviews_tag = hotel.find('div', attrs = {"data-automation": "bubbleReviewCount"})
		reviews = reviews_tag.get_text(strip = True) if reviews_tag else "No reviwes"

		hotels_list.append({
			"name": name,
			"score": score,
			"reviews": reviews
			})
	return hotels_list

def scrape_hotels():
	paginas = 11
	urls = urls_por_pagina(url,paginas)
	list_of_hotels = []

	for u in urls:
		html = get_tripadvisor_html(u)
		if html:
			hotels_content = parser_html(html)
			list_of_hotels.extend(hotels_content)
	return list_of_hotels

Hotels_of_tripadvisor = scrape_hotels()

with open("hoteles_tripadvisor.json", "w", encoding="utf-8") as f:
        json.dump(Hotels_of_tripadvisor, f, ensure_ascii=False, indent=4)




