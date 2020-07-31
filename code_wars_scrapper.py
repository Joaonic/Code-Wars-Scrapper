# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 19:42:36 2020

@author: jaoni
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException        
import time
import os

site = 'https://www.codewars.com/users/sign_in'
path = r'YOUR PATH'
email = 'YOUR EMAIL'
password = 'YOUR PASSWORD'
def scrapping(site, path, email, password):
    filtro = {' ':'_', '?':'', '!':'', '.':'', '-':'', ':':'', ';':'', ',':'', "'":'', '<':'', '>':'', '=':'', '+':''}
    ##add the desired language and it extension like bellow
    languages = {'Python:':'.py', 'JavaScript:':'.js', 'C:':'.c'} ##if there are languages in 
                    ##your completed kata that are not here, some errors may happen.
    pause = 5
    browser = webdriver.Chrome()
    browser.get(site)
    create_dir(path)
    time.sleep(pause)
    login = browser.find_element_by_xpath("//*[@id='user_email']")
    login.send_keys(email)
    login = browser.find_element_by_xpath("//*[@id='user_password']")
    login.send_keys(password)
    login = browser.find_element_by_xpath("//*[@type='submit']")
    login.submit()
    time.sleep(pause)
    element = browser.find_element_by_xpath("//*[@id='main_header']/ul/li[4]/div/div/ul/li[1]/a")
    href = element.get_attribute('href')
    browser.get(href + '/completed_solutions')
    time.sleep(pause)
    check = check_exists_by_class("p-10px.js-infinite-marker",  browser)
    
    ##rolling the page down to the end
    while check == True:
        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(pause)
        check = check_exists_by_class("p-10px.js-infinite-marker", browser)
    
    time.sleep(pause)
    elements = browser.find_elements_by_class_name("item-title")
    elements1 = browser.find_elements_by_class_name("list-item.solutions")
    kata_titles = []
    kata_links = []
    kata_languages = []
    kata_codes = []
    kata_descriptions = []
    kata_kyu = []
    
    for element in elements:
        kata_links.append(element.find_element_by_css_selector('a').get_attribute('href'))
        kata_titles.append(element.find_element_by_css_selector('a').text)
        kata_kyu.append(element.find_element_by_css_selector('span').text)
    
    for element in elements1:
        if isinstance(element.find_elements_by_css_selector('h6'), list) == True and len(element.find_elements_by_css_selector('h6')) > 1:
            multiples_languages = []
            multiples_codes = []
            solutions_languages = element.find_elements_by_css_selector('h6')
            solutions_codes = element.find_elements_by_css_selector('code')
            for i in range(len(solutions_languages)):
                multiples_languages.append(solutions_languages[i].text)
                multiples_codes.append(solutions_codes[i].text)
            kata_languages.append(multiples_languages)
            kata_codes.append(multiples_codes)
        else:
            kata_languages.append(element.find_element_by_css_selector('h6').text)
            kata_codes.append(element.find_element_by_css_selector('code').text)
    
    for i in range(len(kata_links)):
        browser.get(kata_links[i])
        for simbols in filtro:
            kata_titles[i] = kata_titles[i].replace(simbols, filtro[simbols])
        time.sleep(2)
        if os.path.exists(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i]) == True:
            break
        print(kata_titles[i])
        kata_descriptions.append(browser.find_element_by_id('description').text)
    
    for i in range(len(kata_descriptions)):
        if isinstance(kata_languages[i], list) == True:
            for j in range(len(kata_languages[i])):
                for language in languages:
                    kata_languages[i][j] = kata_languages[i][j].replace(language, languages[language])
                if os.path.exists(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i]) == True:
                    pass
                else:
                    os.mkdir(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i])
                with open(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i] + "\\" + kata_titles[i] + kata_languages[i][j], 'wt') as file:
                    file.write(kata_codes[i][j])
                with open(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i] + "\\" + 'README.md', 'wt', encoding = 'utf8') as file:
                    file.write(kata_descriptions[i])
        else:        
            for language in languages:
                kata_languages[i] = kata_languages[i].replace(language, languages[language])
            if os.path.exists(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i]) == True:
                pass
            else:
                os.mkdir(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i])
            with open(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i] + "\\" + kata_titles[i] + kata_languages[i], 'wt') as file:
                file.write(kata_codes[i])
            with open(path + "\\" + kata_kyu[i] + "\\" + kata_titles[i] + "\\" + 'README.md', 'wt', encoding = 'utf8') as file:
                file.write(kata_descriptions[i])
    
    a = input('All files created :)\nPress return to quit.')
    browser.quit()

def check_exists_by_class(clas, browser):
    try:
        browser.find_element_by_class_name(clas)
    except NoSuchElementException:
        return False
    return True

def create_dir(path):
    for i in range(1,9):
        if os.path.exists(path + "\\" + str(i) + " kyu") == True:
            pass
        else:
            os.mkdir(path + "\\" + str(i) + " kyu")

scrapping(site, path, email, password)