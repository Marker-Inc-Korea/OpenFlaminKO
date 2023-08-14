# OpenFlaminKO <🦩🇰🇷>
![OpenFlaminKO](https://github.com/Marker-Inc-Korea/OpenFlaminKO/assets/98331298/f45b07b7-f0bb-4a02-acff-19e20e933cfd)  
- Polyglot-Ko을 활용한 image-text multimodal  
  
# Introduction
![Openflamingo 성능](https://github.com/Marker-Inc-Korea/OpenFlaminKO/assets/98331298/c27c8c32-e0a5-432d-b29e-c79d09e4b1b2)
- 최근 LLM열풍이 불고 있는 가운데, 한국어 LLM인 Polyglot-KO의 등장으로 국내에서도 ChatGPT와 유사한 LLM을 만들고자하는 시도와 노력들이 엄청 활발하게 이루어지고 있음.
- Polyglot-KO를 LORA 방식을 활용하여 여러 NLP 분야에서 접목하고 있지만, multimodal로 이용되는 사례가 아직 나오지 않음.
- MultiModal을 만들기 위해서는 엄청난 양의 데이터셋이 필요하지만, 현재 존재하는 multimodal dataset(i.e., [LAION](https://laion.ai/), [MMC4](https://github.com/allenai/mmc4))들은 대부분 영어 caption으로 이루어져 있고, 한국어의 비중이 거의 없기 때문에 한국어 Multimodal을 만드는 것을 사실상 쉽지 않은 도전임.
- 기존의 LLM을 활용하여 multimodal로 만든 [OpenFlamingo](https://github.com/mlfoundations/open_flamingo)로 부터 영감을 받아서, Polyglot-KO를 multimodal로 설계하고자 하는 마음이 생겨서 OpenFlminKO model를 만들기 시작함.
- 기존 SOTA multimodal들은 한국어에 대한 성능이 매우 안 좋았기 때문에, 한국어 multimodal를 만들기 위한 첫걸음이라는 것에 의의를 둔다.
- 본 연구는 (주)마커와 (주)미디어그룹사람과숲의 오픈소스 LLM 연구 컨소시엄에서 진행되었습니다.  

# KO-LAION Dataset
- [OpenFlamingo](https://github.com/mlfoundations/open_flamingo)에서 활용했던 LAION dataset을 기반으로 DeepL을 통해서 번역을 시도하여 400만개 caption을 번역함.  
  
```
(Code coming soon...)
```


# Training Code
- 
```
(Code coming soon...)
```


# Evaluation Code


# Performance


# Acknowledgement
[OpenFlamingo](https://github.com/mlfoundations/open_flamingo)  
[Polyglot-KO](https://huggingface.co/EleutherAI/polyglot-ko-1.3b)  
[CLIP-VIT](https://huggingface.co/openai/clip-vit-large-patch14)  



