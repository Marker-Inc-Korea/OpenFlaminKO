# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 13:36:43 2023

@author: txt translation -> json dump
"""

import os
import json
import tarfile
import shutil
import demoji
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

import multiprocessing as mp
from multiprocessing.pool import Pool

from glob import glob
from tqdm import tqdm

# Start a Selenium driver
service = Service('./chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
#options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
#options.add_argument('window-size=1920x1080')
#options.add_argument("user-agent="+ua.random) # user-agent 값 변경
driver = webdriver.Chrome(service=service, options=options)

# Reach the deepL website
deepl_url = 'https://www.deepl.com/ko/translator' # 한국어
driver.get(deepl_url)

def remove_emojis(text):
    return demoji.replace(text, '')

def deepL_translation_KO(txt_path):
    
    if txt_path not in os.listdir('./sample/translation/'):
        tx_file = open('./sample/extract/'+txt_path, 'r', encoding='UTF8')
        text_to_translate = str(tx_file.read()) # txt
        #text_to_translate = text_to_translate[2:-1] # remove 'b' and final '.
        tx_file.close()
        
        content = ''
    
    
        # Get thie inupt_area 
        #input_xpath = '//*[@id="panelTranslateText"]/div[1]/div[2]/section[1]/div[3]/div[2]/d-textarea/div/p'
        input_css = 'div.lmt__inner_textarea_container d-textarea'
        input_area = driver.find_element(By.CSS_SELECTOR, input_css)
    
        # Send the text
        try:
            input_area.send_keys(text_to_translate)
        except:
            # There is BMP(이모지). // remove
            text_to_translate = remove_emojis(text_to_translate)
            input_area.send_keys(text_to_translate)
    
        # Wait for translation to appear on the web page    
        time.sleep(3)
            
        bug_count = 0
        while (len(content) == 0) and (bug_count < 20):
            try:
                translation_xpath = '//*[@id="panelTranslateText"]/div[1]/div[2]/section[2]/div[3]/div[1]/d-textarea/div' # /div/p
                translation_text = driver.find_element(By.XPATH, translation_xpath)
                content = translation_text.text
            except Exception as e:
                bug_count += 1
                print("Bug count:", bug_count)
                
                if bug_count == 20:
                    print(e)
                    sys.exit()
        
        # Display results
        print()
        print('Original    :', text_to_translate)
        print('Translation :', content)
        print()
        
        # clear(X) button
        try:
            button_css = 'div.lmt__clear_text_button_wrapper button'
            button = driver.find_element(By.CSS_SELECTOR, button_css)
            driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(e)
        
        
        # write file
        with open('./sample/translation/'+txt_path, 'w', encoding='utf-8') as new_tx:
            new_tx.write(content)
        
        num = txt_path.split(".")[0]
        json_path = num+'.json'
        img_path = num+'.jpg'
        
        # move
        try:
            shutil.move('./sample/extract/'+json_path, './sample/translation/'+json_path)
            shutil.move('./sample/extract/'+img_path, './sample/translation/'+img_path)
        except:
            pass
    
    else:
        print("There is same file")
        try:
            os.remove('./sample/extract/'+txt_path)
        except:
            pass
        
            
def parallel_json(txt_list):
    
    #content_result = parmap.map(deepL_translation_KO, caption_list, pm_pbar=True, processes=num_cores)

    pool = Pool(num_cores)
    content_result = pool.map(deepL_translation_KO, txt_list)

    pool.close()
    pool.join()
    
    driver.close()

    return content_result


if __name__ == '__main__':
    # check cpu
    print("CPU core:", mp.cpu_count()) # 16개
    num_cores = 10

    # check time
    start = time.time()
    
    # tar_list
    # Tar list
    tar_list = glob('./sample/shard_*.tar')
    print("List length:", len(tar_list))
    
    os.makedirs('./sample/extract/', exist_ok=True) # make sub folder
    os.makedirs('./sample/translation/', exist_ok=True) # make sub folder
    
    extract_flag = False # inital = True, other False
    if extract_flag:
        for t in tqdm(range(len(tar_list))):
            
            # extract tar file
            tar_file = tarfile.open(tar_list[t])
            tar_file.extractall('./sample/extract/', numeric_owner=True)
            tar_file.close()
        
    # check txt and json file
    extract_list = os.listdir('./sample/extract')
    
    # save file name and caption
    txt_list = []
    same_file=0
    for name in tqdm(extract_list):
        if 'json' in name:
            os.chmod('./sample/extract/'+name,  0o777)
        elif 'txt' in name:
            txt_list.append(name)
            os.chmod('./sample/extract/'+name,  0o777)
        elif 'jpg' in name:
            os.chmod('./sample/extract/'+name,  0o777)
            
    # merge list:
    #merge_list = []
    #for t,j,i in zip(txt_list, json_list, img_list):
    #    merge_list.append([t,j,i]) # txt, json, img
    
    # tranlation
    print("############ Stage 1 ############")
    content_result = parallel_json(txt_list) # Translation
    
    print("######### Complete!!!! #########")
    print("Length: ", len(glob('./sample/translation/*.txt')))
    
    ############## make new tar
    '''
    print("############ Stage 2 ############")
    for t in tqdm(range(len(tar_list))):
        os.remove(tar_list[t]) # remove original file
        
    translation_file = os.listdir('./sample/translation')
    chunk = 24000 # 8000 data (3x8000)
    num = 11
    for c in range(0, len(translation_file), chunk):
        tar_name = './sample/complete/shard_%05d.tar' % num
        with tarfile.open(tar_name, 'w') as tr:
            for name in translation_file[c:c+chunk]:
                tr.add('./sample/translation/'+name)
        num += 1
    '''
    # folder remove
    #shutil.rmtree('./sample/extract') 
    #shutil.rmtree('./sample/translation') 
    
    print("Time:", time.time() - start)
    time.sleep(10) # wait
    
    # terminate chrome
    driver.quit()
                








































