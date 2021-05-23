import pandas as pd
from os import link
from string import Template
from bs4 import BeautifulSoup
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage ")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(execution_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)



linkOption = input("Do you want to search product with link (yes/no): ")

if linkOption == 'yes' or linkOption == 'Yes' or linkOption == 'YES':
  reviewlist = []

  def get_url(search_term):
      template = "{}"
      return template.format(search_term)
  product = input("Enter the Product link of which you want to get Sentiment:")
  #print(product)          #product search
  url = get_url(product)  #Product link
  driver.get(url)
  """Extract the collection"""
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  sub_review_url = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})
  review_url = sub_review_url.get('href')
  driver.get("https://www.amazon.in"+review_url)
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  reviews = soup.find_all('div', {'data-hook': 'review'})
  for item in reviews:  
      review = [
      #'product': soup.title.text.replace('Amazon.in:Customer reviews:','').strip(),
      #'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
      #'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
      item.find('span', {'data-hook': 'review-body'}).text.strip(),
      ]
      #print(review)
      reviewlist.append(review)
  
  
  
  def view_comments():
      reviews = soup.find_all('div', {'data-hook': 'review'})
      for item in reviews:  
          review = [
          #'product': soup.title.text.replace('Amazon.in:Customer reviews:','').strip(),
          #'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
          #'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
          item.find('span', {'data-hook': 'review-body'}).text.strip(),
          ]
          #print(review)
          reviewlist.append(review)
  for x in range(1,30):
      next_page = soup.find('div', {'class': 'a-form-actions a-spacing-top-extra-large'})
      next_page1 = next_page.find('li', {'class': 'a-last'})
      next_page2 = next_page1.find('a')
      next_page3 = next_page2.get('href')
      driver.get("https://www.amazon.in"+next_page3)
      soup = BeautifulSoup(driver.page_source, 'html.parser')
      view_comments()
      if not soup.find('li', {'class':'a-disabled a-last'}):
          pass
      else:
          break
  #print(*reviewlist, sep = "\n")
  df = pd.DataFrame(reviewlist)
  df.to_excel('livedataset.xlsx', index=False)
  print('Finished..')
