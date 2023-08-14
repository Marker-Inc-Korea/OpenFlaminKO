# OpenFlaminKO <🦩🇰🇷>
![OpenFlaminKO](https://github.com/Marker-Inc-Korea/OpenFlaminKO/assets/98331298/f45b07b7-f0bb-4a02-acff-19e20e933cfd)  
- [Polyglot-Ko](https://huggingface.co/EleutherAI/polyglot-ko-1.3b)을 활용한 image-text multimodal  
  
# Introduction
![Openflamingo 성능](https://github.com/Marker-Inc-Korea/OpenFlaminKO/assets/98331298/c27c8c32-e0a5-432d-b29e-c79d09e4b1b2)
- 최근 LLM열풍이 불고 있는 가운데, 한국어 LLM인 Polyglot-KO의 등장으로 국내에서도 ChatGPT와 유사한 LLM을 만들고자하는 시도와 노력들이 엄청 활발하게 이루어지고 있음.
- Polyglot-KO를 LORA 방식을 활용하여 여러 NLP 분야에서 접목하고 있지만, multimodal로 이용되는 사례가 아직 나오지 않음.
- MultiModal을 만들기 위해서는 엄청난 양의 데이터셋이 필요하지만, 현재 존재하는 multimodal dataset(i.e., [LAION](https://laion.ai/), [MMC4](https://github.com/allenai/mmc4))들은 대부분 영어 caption으로 이루어져 있고, 한국어의 비중이 거의 없기 때문에 한국어 Multimodal을 만드는 것을 사실상 쉽지 않은 도전임.
- 기존의 LLM을 활용하여 multimodal로 만든 [OpenFlamingo](https://github.com/mlfoundations/open_flamingo)로 부터 영감을 받아서, Polyglot-KO를 multimodal로 설계하고자 하는 마음이 생겨서 OpenFlminKO model를 만들기 시작함.
- 기존 SOTA multimodal들은 한국어에 대한 성능이 매우 안 좋았기 때문에, 한국어 multimodal를 만들기 위한 첫걸음이라는 것에 의의를 둔다.
- 본 연구는 (주)마커와 (주)미디어그룹사람과숲의 오픈소스 LLM 연구 컨소시엄에서 진행되었습니다.

# Dependencies
- [ChromeDriver](https://chromedriver.chromium.org/downloads) 설치
- [7-zip](https://www.7-zip.org/) 환경변수 등록
- Pytorch >= 2.0 권장
  
# KO-LAION Dataset
```
translation
├── sample                    
│   ├── complete
|   ├── shard_00001.tar # 번역할 tar 파일
│   ├── shard_00002.tar
│   └── ...
├── chromedriver.exe
├── txt_translation.py
├── set_translation.py
├── tar_txt_preprocessing.py
└── ...
```
> 데이터 번역을 위한 파일 경로는 위와 같다.
  
- [OpenFlamingo](https://github.com/mlfoundations/open_flamingo)에서 활용했던 LAION dataset을 기반으로 [DeepL](https://www.deepl.com/translator)을 통해서 번역을 시도하여 400만개 caption을 번역함.  
- [Webdataset](https://github.com/webdataset/webdataset) 형식을 지원하기 때문에 LAION 데이터셋을 tar파일로 이용해야 합니다. 관련 코드는 [LAION_TRAIN](https://github.com/mlfoundations/open_flamingo/tree/main/open_flamingo/train)를 참고해주세요.  
- HuggingFace에 [KO-LAION-SUBSET](Soon...)을 통해서 다운 받으실 수 있습니다. (Not update...)  
```
txt_translation.py # tar파일의 압축을 풀고, txt파일을 번역하는 과정
set_translation.py # 번역이 잘 되었는지 확인하고, tar파일로 다시 압축하는 과정
tar_txt_preprocessing.py # text 전처리 코드
```
> 위의 코드를 순차적으로 실행하여서 LAION dataset을 번역합니다.  
> 데이터 전처리: 1) 이모지 제거 2) 한국어가 없는 caption 제거 3) empty sentence 제거  
  
```
open_flamingo
├── laion_data                    
│   ├── shard_00000.tar
|   ├── shard_00001.tar       
│   ├── shard_00002.tar
│   └── ...
├── open_flamingo
├── OpenKyujinpie_v1
└── ...
```
> 데이터 경로는 위와 같이 설정합니다.  

# Training Code
- [COLAB](https://colab.research.google.com/drive/1_TEJopoN7a4jeDOQZ0Dse4fIEXUFtYRC#scrollTo=l_YCMEVRj3rp) 코드를 통해서 실행해보실 수 있습니다.
> 단, A100 GPU에서만 실행이 되기 때문에, 비용이 많이 발생합니다.  
> Polyglot-KO-1.3b에서 실행이 됩니다. 5.8b 이상은 원하실 경우, 더 많은 컴퓨팅 자원이 필요합니다.  
  
# Evaluation Code
- 모델의 checkpoint는 아래에서 다운받으실 수 있습니다. (Not update...)  
    
| Model | Dataset | Link |  
| ------------- | ------------- | ------------- |  
| `OpenFlaminKO-400K` | [KO-LAION-400K](Not) | NaN |  
| `OpenFlaminKO-1M` | [KO-LAION-1M](Not) | [Checkpoint](Not) |  
| `OpenFlaminKO-4M` | [KO-LAION-4M](Not) | [Checkpoint](Not) |  
   
```python
# 50 epoch model
from open_flamingo import create_model_and_transforms

# Default setting
model, image_processor, tokenizer = create_model_and_transforms(
    clip_vision_encoder_path="ViT-L-14",
    clip_vision_encoder_pretrained="openai",
    lang_encoder_path="EleutherAI/polyglot-ko-1.3b", # PolyGlot 1.3B
    tokenizer_path="EleutherAI/polyglot-ko-1.3b", # PolyGlot 1.3B
    cross_attn_every_n_layers=1
)

# load checkpoint
checkpoint_path = (Coming soon...)
print("Model path:", checkpoint_path)
model.load_state_dict(torch.load(checkpoint_path), strict=False)
model.eval() # Freeze
```
>Model implementation
  
```python
# Image captioning by github example
from PIL import Image
import requests
import torch

"""
Step 1: Load images
"""
demo_image_two = Image.open(
    requests.get(
        "http://images.cocodataset.org/test-stuff2017/000000028137.jpg",
        stream=True
    ).raw
)

query_image = Image.open(
    requests.get(
        "http://images.cocodataset.org/val2017/000000039769.jpg",
        stream=True
    ).raw
)

"""
Step 2: Preprocessing images
Details: For OpenFlamingo, we expect the image to be a torch tensor of shape
 batch_size x num_media x num_frames x channels x height x width.
 In this case batch_size = 1, num_media = 3, num_frames = 1,
 channels = 3, height = 224, width = 224.
"""
vision_x = [image_processor(demo_image_two).unsqueeze(0), image_processor(query_image).unsqueeze(0)]
vision_x = torch.cat(vision_x, dim=0)
vision_x = vision_x.unsqueeze(1).unsqueeze(0)

"""
Step 3: Preprocessing text
Details: In the text we expect an <image> special token to indicate where an image is.
 We also expect an <|endofchunk|> special token to indicate the end of the text
 portion associated with an image.
 +) Translation by DeepL.
"""
tokenizer.padding_side = "left" # For generation padding tokens should be on the left
lang_x = tokenizer(
    ["<image>해당 이미지는 욕실 세면대입니다.<|endofchunk|><image>해당 이미지는"], # new version
    return_tensors="pt",
)


"""
Step 4: Generate text
"""
generated_text = model.generate(
    vision_x=vision_x,
    lang_x=lang_x["input_ids"],
    attention_mask=lang_x["attention_mask"],
    max_new_tokens=20,
    num_beams=3, #
)

print("Generated text: ", tokenizer.decode(generated_text[0]))
```
>Simple test code  
  
# Performance (Not update...)  
- KO-VQAv2 (VQA accuracy)  
  
| Model | Dataset | 0-shot |  
| ------------- | ------------- | ------------- |  
| `OpenFlaminKO-400K` | [KO-LAION-400K](Not) | NaN |  
| `OpenFlaminKO-1M` | [KO-LAION-1M](Not) | NaN |  
| `OpenFlaminKO-4M` | [KO-LAION-4M](Not) | NaN |  

> Performance 측정을 위해 [VQAv2](https://visualqa.org/download.html)를 DeepL을 활용하여 번역함.
  
# Acknowledgement
[OpenFlamingo](https://github.com/mlfoundations/open_flamingo)  
[Polyglot-KO](https://huggingface.co/EleutherAI/polyglot-ko-1.3b)  
[CLIP-VIT](https://huggingface.co/openai/clip-vit-large-patch14)  



