from bs4 import BeautifulSoup
import requests

class WebScrap():
	def __init__(self):
		pass

	def getHTML(self, url):
		return requests.get(url).text

	def makeSoup(self, html_content):
		return BeautifulSoup(html_content, 'lxml')

	#This function will return all the links of a webpage except the links of particular focussing an element (starting with #)
	def getAllLinks(self, html_soup):
		all_links = html_soup.find_all('a')
		valid_links=[]

		for link_content in all_links:
			link_a = link_content['href']
			#Validating the link
			if len(link_a)>0 and (link_a[0]) is not '#':
				if '#' in link_a:
					char_idx = link_a.find('#')
					new_link = link_a[:char_idx]
				else:
					new_link = link_a

				if new_link not in valid_links:
					valid_links.append(new_link)
		return valid_links

	def getAllLinksText(self, html_soup):
		all_links = html_soup.find_all('a')
		valid_links_text=[]

		for link_content in all_links:
			link_a = link_content['href']
			#Validating the link
			if len(link_a)>0 and (link_a[0]) is not '#':
				if '#' in link_a:
					char_idx = link_a.find('#')
					new_link = link_a[:char_idx]
				else:
					new_link = link_a

				if new_link not in valid_links_text:
					valid_links_text.append(link_content.text)
		return valid_links_text

	#This function will get the urls of all the images in a page
	def getImgLinks(self, html_soup):
		img_links = html_soup.find_all('img')
		img_links = map(lambda x: x['src'], img_links)
		return list(img_links)

	#This function will get the urls of all the images in a page
	def getContent(self, elements):
		return list(map(lambda x: x.text, elements))

	#This function will get the text data in a page
	def getTextData(self, html_soup):
		text_data=[]
		text_data += self.getContent(html_soup.find_all('p'))
		text_data += self.getContent(html_soup.find_all('a'))
		text_data += self.getContent(html_soup.find_all('div',class_='bigtitle'))
		text_data += self.getContent(html_soup.find_all('h1'))
		text_data += self.getContent(html_soup.find_all('h2'))
		text_data += self.getContent(html_soup.find_all('h3'))
		text_data += self.getContent(html_soup.find_all('h4'))
		text_data += self.getContent(html_soup.find_all('h5'))
		return text_data

baseURL='http://midas.iiitd.edu.in'
midaslab = WebScrap()
web_content = midaslab.getHTML(baseURL)		
soup = midaslab.makeSoup(web_content) 
links = midaslab.getAllLinks(soup)
links_text = midaslab.getAllLinksText(soup)
#Navigation pages URL
nav_pages_links = links[:8]
nav_pages_links_text = links_text[:8]
#Iterating over all the navigation links to find out the urls of images and writing it to the file
pageno=1
with open('imglinks.txt', 'w') as f:
	for linkno in range(0,len(nav_pages_links)):
		nav_url=nav_pages_links[linkno]
		nav_text=nav_pages_links_text[linkno]
		web_content_navpage = midaslab.getHTML(baseURL+nav_url)
		soup_navpage = midaslab.makeSoup(web_content_navpage)
		imglinks = midaslab.getImgLinks(soup_navpage)
		f.write('Page No-{}, Name - {}\n'.format(pageno,nav_text))
		f.write('Page Link- {}{}\n'.format(baseURL,nav_url))
		f.write('Image Links--\n')
		for img_link in imglinks:
			f.write("{}{}\n".format(baseURL,img_link))
		f.write('----------------------------------\n'.format(pageno))
		pageno += 1

#Iterating over all the navigation links to find out the text data and writing it to the file
pageno=1
with open('textdata.txt', 'w') as f:
	for linkno in range(0,len(nav_pages_links)):
		nav_url=nav_pages_links[linkno]
		nav_text=nav_pages_links_text[linkno]
		web_content_navpage = midaslab.getHTML(baseURL+nav_url)
		soup_navpage = midaslab.makeSoup(web_content_navpage)
		textdata = midaslab.getTextData(soup_navpage)
		f.write('Page No-{}, Name - {}\n'.format(pageno,nav_text))
		f.write('Page Link- {}{}\n'.format(baseURL,nav_url))
		f.write('Text Data--\n')
		for textdata_row in textdata:
			f.write("{}\n".format(textdata_row))
		f.write('----------------------------------\n\n'.format(pageno))
		pageno += 1


