import os
import json
from tqdm import tqdm
import tarfile

if __name__ == '__main__':
    file_list = os.listdir('./sample/translation')

    check_translation = False
    if check_translation:
        txt_list = []
        for name in tqdm(file_list):
            if 'txt' in name:
                txt_list.append(name)

        # json, img checking
        for name in tqdm(txt_list):
            num = name.split(".")[0]   
            json_name = num+'.json'
            img_name = num+'.jpg'

            if (json_name in file_list) and (img_name in file_list):
                # json 수정
                tx_file = open('./sample/translation/'+name, 'r', encoding='UTF8')
                content = str(tx_file.read()) # txt
                tx_file.close()

                with open('./sample/translation/'+json_name, 'r',  encoding='utf-8') as js:
                    json_file = json.load(js)
                    json_file['caption'] = content

                    with open('./sample/translation/'+json_name, 'w', encoding='utf-8') as new_js:
                        json.dump(json_file, new_js, indent='\t', ensure_ascii=False) # ensure korean word.

            else:
                print('Error:', num) # Wrong
    
    check_file = False
    if check_file:
        json_list = []
        img_list = []
        txt_list = []
        for name in tqdm(file_list):
            if 'json' in name:
                json_list.append(name)
            if 'jpg' in name:
                img_list.append(name)
            if 'txt' in name:
                txt_list.append(name)
        
        json_length = len(json_list)
        img_length = len(img_list)
        txt_length = len(txt_list)

        if (json_length != txt_length) or (img_length != txt_length):
            print("json length:", json_length)
            print("img length:", img_length)
            print("txt length:", txt_length)

            for js_name in tqdm(json_list):
                num = js_name.split(".")[0]
                txt_name = num + '.txt'

                if txt_name not in txt_list:
                    print("Error:", num)
            
            print()
            print("#########################################")
            print()

            for im_name in tqdm(img_list):
                num = im_name.split(".")[0]
                txt_name = num + '.txt'

                if txt_name not in txt_list:
                    print("Error:", num)
        
        else:
            print("Perfect")
            
    make_flag = True
    if make_flag:
        print("############ Stage 2 ############")
        
        translation_file = []
        for name in tqdm(file_list):
            if 'txt' in name:
                translation_file.append(name)
        #print(len(translation_file))
        
        chunk = 8000 # 8000 data (3x8000)
        num = 81 # ~98, 1,2,3,4 61~65
        for c in range(0, len(translation_file), chunk):
            tar_name = './sample/complete/shard_%05d.tar' % num
            with tarfile.open(tar_name, 'w') as tr:
                for name in tqdm(translation_file[c:c+chunk]):
                    number = name.split(".")[0]
                    js_name = number + '.json'
                    im_name = number + '.jpg'
                    tr.add('./sample/translation/'+name, name)
                    tr.add('./sample/translation/'+js_name, js_name)
                    tr.add('./sample/translation/'+im_name, im_name)
            num += 1
        