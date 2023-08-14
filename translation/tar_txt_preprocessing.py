# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 22:01:14 2023

@author: Preprocessing Code
- empty word
- There is no korea word
---> remove
"""

import tarfile
import os
import glob
import re

from tqdm import tqdm


if __name__ == '__main__':
    
    tar_list = glob.glob("./sample/complete/*.tar")
    print(tar_list)
    
    for t in range(0, len(tar_list)):
        with tarfile.open(tar_list[t], "r") as tf: # reading option
            file_list = tf.getnames()
            
            remove_txt = []
            remove_json = []
            remove_img = []
            
            remove_count = 0
            max_len = 0
            max_count = 0
            
            for name in tqdm(file_list):
                if 'txt' in name:
                    num = name.split(".")[0]

                    with tf.extractfile(name) as tx:
                        content = str(tx.read(), encoding='UTF8') # binary type
                        content = content[2:-1] # remove 'b'
                        
                        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자
                        result = hangul.sub('', content) # 한글만 추출
                        
                        #if len(content) > max_len:
                        #    max_len = len(content)
                        
                        
                        if (len(result) == 0) or (len(content) >= 1000): # strange translation
                            remove_txt.append(name)
                            remove_json.append(num+'.json')
                            remove_img.append(num+'.jpg')
                            print(content)
                            remove_count += 1
                        
                        else: # 굿 translation
                            pass
            
            #print("Max length:", max_len) # examepl) shard_00021.tar: 1177
            #print("Max count:", max_count) # examepl) shard_00021.tar: 1
            print("remove data:", remove_count) # examepl) shard_00021.tar: 74 // 60~120 delete
  
        
        ################################ Second, remove old json and txt file
        print("############ Stage 2 ############")
        cmd_remove_json = '7z d ' + tar_list[t] 
        cmd_remove_txt = '7z d ' + tar_list[t] 
        cmd_remove_img = '7z d ' + tar_list[t] 
        for remove_name1, remove_name2, remove_name3 in zip(remove_txt, remove_img, remove_json):
            cmd_remove_json += " " + remove_name3
            cmd_remove_img += " " + remove_name2
            cmd_remove_txt += " " + remove_name1
        
        os.system(cmd_remove_json)
        os.system(cmd_remove_img)
        os.system(cmd_remove_txt)