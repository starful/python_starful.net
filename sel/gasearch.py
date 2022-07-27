from flask import Flask, render_template, session
from flask import url_for, redirect, request
from flask import Blueprint
from selenium import webdriver
from datetime import datetime
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session
from PIL import Image

import os
import os.path
import time
import json
import logging
import chromedriver_binary
import math
import io
import requests
import hashlib

gasearch = Blueprint('gasearch', __name__, url_prefix='/api/gasearch')
logger = logging.getLogger(__name__)

filename = 'result_list.txt'

@gasearch.route('/filelistdown')
def filelistdown():
    search_keywords = load_set(filename)
    for search_keyword in search_keywords:
        run(search_keyword)

@gasearch.route('/imagedown')
def imagedown():
    run(request.args.get('keyword'))

@gasearch.route('/makelist')
def make_list():
    # URL
    search_url = "https://www.seprace.com/category/1?gender=1,4"

    # Chrome webdriver setting
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(search_url)
    time.sleep(2)

    all_count = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[4]/div[1]/div/h1/div/span").text
    # print(all_count.split("/t")[0])
    all_count_int = int(all_count.replace("(", '').split()[0])
    page_count = 60
    print(str(all_count_int))
    print(str(page_count))
    print(str(all_count_int/page_count))
    print(str(math.ceil(all_count_int/page_count)))

    # click load button
    for i in range(math.floor(all_count_int/page_count)):
        load_button()

    # get data
    temp_result_list = driver.find_elements_by_class_name('product-name')
    result_list = []
    for x in range(len(temp_result_list)):
        result_list.append(temp_result_list[x].text)
    print(len(result_list))

    # make file
    with open("/Users/starful/work/result_list.txt", mode='w') as f:
        f.write("\n".join(result_list))
    f.close()
    driver.close()

def load_button():
    # load_button click
    load_button = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[4]/div[4]/a")
    load_button.click()
    time.sleep(3)

def save_image():
    # 画像のダウンロード
    image_save_folder_path = query
    if not os.path.isdir(image_save_folder_path):
        os.makedirs(image_save_folder_path)

    for url in image_urls:
        try:
            image_content = requests.get(url).content
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(image_save_folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=90)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")

def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

def load_set(filename):
    doc = load_doc(filename)
    dataset = list()
    # process line by line
    for line in doc.split('\n'):
        # skip empty lines
        if len(line) < 1:
            continue
        # get the image identifier
        identifier = line.split('.')[0]
        dataset.append(identifier)
    return set(dataset)

def run(search_keyword):
    # クリックなど動作後に待つ時間(秒)
    sleep_between_interactions = 2
    # ダウンロードする枚数
    download_num = 50
    # 検索ワード
    # query = "cat"
    query = search_keyword

    # 画像検索用のurl
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # サムネイル画像のURL取得
    # wd = webdriver.Chrome(executable_path=DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    wd = webdriver.Chrome(chrome_options=options)
    wd.get(search_url.format(q=query))

    # サムネイル画像のリンクを取得(ここでコケる場合はセレクタを実際に確認して変更する)
    thumbnail_results = wd.find_elements_by_css_selector("img.rg_i")

    # サムネイルをクリックして、各画像URLを取得
    image_urls = set()
    for img in thumbnail_results[:download_num]:
        try:
            img.click()
            time.sleep(sleep_between_interactions)
        except Exception:
            continue
        # 一発でurlを取得できないので、候補を出してから絞り込む(やり方あれば教えて下さい)
        # 'n3VNCb'は変更されることあるので、クリックした画像のエレメントをみて適宜変更する
        url_candidates = wd.find_elements_by_class_name('n3VNCb')
        for candidate in url_candidates:
            url = candidate.get_attribute('src')
            if url and 'https' in url:
                image_urls.add(url)
    # 少し待たないと正常終了しなかったので3秒追加
    time.sleep(sleep_between_interactions+3)
    wd.quit()

    # 画像のダウンロード
    image_save_folder_path = query
    if not os.path.isdir(image_save_folder_path):
        os.makedirs(image_save_folder_path)

    for url in image_urls:
        try:
            image_content = requests.get(url).content
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(image_save_folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=90)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")            