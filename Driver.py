from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import warnings
warnings.filterwarnings('ignore')

import sys
import time
import datetime

from sqlalchemy import create_engine, text
import pymysql
from sqlalchemy.exc import IntegrityError
import pandas as pd



def db_connection():


    host = "localhost"
    port = 3306
    database = "test"
    username = "root"
    password = "1234qwer"

    db_connections = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(db_connections)
    conn = engine.connect()


    return engine, conn





def dump(tbname, df, engine):


    for i in range(len(df)):
        try:
            df.iloc[i:i+1].to_sql(name=tbname, con=engine, if_exists='append', method='multi', index=False, index_label = ['url', 'title'])
        except IntegrityError:
            print('Duplicated')
        except ValueError:
            print('Duplicated')
            pass 






def StartDriver(url):

    service = Service(executable_path=r'/usr/bin/chromedriver')
    option = webdriver.ChromeOptions()

    option.add_argument('headless')
    option.add_argument("disable-gpu")
    option.add_argument("no-sandbox")
    option.add_argument("--disable-extensions")
    option.add_argument('--disable-dev-shm-usage')

    
    driver = webdriver.Chrome(service=service, options=option)
   
    driver.implicitly_wait(3)
    driver.get(url)

    return driver



def Findelementbyxpath(driver, xpath):

    try:
        res = driver.find_element(By.XPATH, xpath)
        return res
    except:

        return None


def Findelementsbyxpath(driver, xpath):

    try:
        res = driver.find_elements(By.XPATH, xpath)
        return res
    except:

        return None


def Childelementbyxpath(parent, xpath):

    try:
        res = parent.find_element(By.XPATH, xpath)
        return res
    except:

        return None

def Childelementsbyxpath(parent, xpath):

    try:
        res = parent.find_elements(By.XPATH, xpath)
        return res
    except:

        return None


def Clickelement(element):


    try:
        element.click()
        time.sleep(1.5)
        return True

    except:
        try:
            element.send_keys(Keys.ENTER)
            time.sleep(1.5)
            return True
        except Exception as e:
            print(e)
            return False



def Getattribute(element_val, el):

    try:
        if el == 'text':
            res = element_val.text
        else:
            res = element_val.get_attribute(el)

        return res

    except Exception as e:
        return None


def Getattributebyxpath(driver, xpath, el):

    try:
        if el == 'text':
            res = Findelementbyxpath(driver, xpath).text
        else:
            res = Findelementbyxpath(driver, xpath).get_attribute(el)

        return res

    except Exception as e:
        return None



def Pagescrolldown(driver):

    prev_height = driver.execute_script("return document. body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        current_height = driver.execute_script("return document. body.scrollHeight")
        
        if current_height == prev_height:
            break
        
        prev_height == current_height
