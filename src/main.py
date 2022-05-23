#利用するライブラリ(モジュール)をインポート

import requests
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import sys 
sys.path.append("lib.bs4")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10)

query = input("画像検索したいものや人のKWを入力してください！：")
url = "https://www.google.com/search?q={}&hl=ja&tbm=isch".format(query)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# すべての要素が読み込まれるまで待つ。タイムアウトは15秒。
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

driver.get(url)
html = driver.page_source.encode("utf-8")
soup = BeautifulSoup(html, "html.parser")

img_tags = soup.find_all("img",limit=100)
img_urls = []
print(len(img_tags))


img_urls = []
for img_tag in img_tags:
  url = img_tag.get("src")

  if url is None:
    url = img_tag.get("data-src")

  if url is not None:
    img_urls.append(url)



def download_image(url, file_path):
  r = requests.get(url, stream=True)

  if r.status_code == 200:
    with open(file_path, "wb") as f:
      f.write(r.content)
    
import base64
def save_base64_image(data, file_path):
  # base64の読み込みは4文字ごとに行う。4文字で区切れない部分は「=」で補う
  data = data + '=' * (-len(data) % 4)
  img = base64.b64decode(data.encode())
  with open(file_path, "wb") as f:
      f.write(img)



# save_dir = "../data/" + str(query)+"/"
# if not os.path.exists(save_dir):
#     os.mkdir(save_dir)
# a=1
# for elem_url in img_urls:
#     try:

#         r = requests.get(elem_url)
#         with open(save_dir + "data"+str(a)+".jpg","wb") as fp:
#             fp.write(r.content)
#         a += 1
#         sleep(0.1)
#     except:
#         pass


import os
import re
# ご自分の環境に合わせて任意のディレクトリパスを指定してください。
save_dir = "../data/" + str(query) + "/"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

base64_string = "data:image/jpeg;base64,"
png_base64_string = "data:image/png;base64,"

for index, url in enumerate(img_urls):
  file_name = "{}.jpg".format(index)

  image_path = os.path.join(save_dir, file_name)

  if len(re.findall(base64_string, url)) > 0 or len(re.findall(png_base64_string, url)) > 0:
    url = url.replace(base64_string, "")
    save_base64_image(data=url, file_path=image_path)
  else:
    download_image(url=url, file_path=image_path)

driver.quit()