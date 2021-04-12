# 캡스톤디자인 연구

## 주제 : 머신러닝을 활용한 콘텐츠 추천시스템

### 프로젝트 도메인 : http://todayrecipe.kro.kr or http://www.todayrecipe.kro.kr
(chrome 에서 최적화 되어있습니다.)

---
## PC화면 구성(screen width>=768px 반응형)
### 메인 화면
![image](https://user-images.githubusercontent.com/22045179/114431281-48c60b80-9bfa-11eb-8801-c1c29ea0efc9.png)
가운데 검색란에 가지고 있는 재료를 띄어쓰기 단위로 입력을 하고, 자신에게 해당되는 건강정보를 아래의 체크박스를 체크하여 검색함.
추천알고리즘을 통해 재료와 건강정보가 가장 많이 포함된 음식들을 분류별로 3가지씩 추천하여 보여줌.(검색결과 page)

![image](https://user-images.githubusercontent.com/22045179/114431378-66937080-9bfa-11eb-920b-cb9cec80ea4c.png)
(our service 내용 수정 예정 - 검색에 시스템 소개, 개발자 소개, 챗봇 시스템 소개)

![image](https://user-images.githubusercontent.com/22045179/114431480-7d39c780-9bfa-11eb-9439-08fff6f83ede.png)
분류별로 대표적인 음식을 소개함.

---

### 검색결과 화면
![image](https://user-images.githubusercontent.com/22045179/114432287-7bbccf00-9bfb-11eb-961a-b243f6f24f26.png)
검색결과 페이지에서도 다른 음식을 검색할 수 있도록 검색란을 구성함.

![image](https://user-images.githubusercontent.com/22045179/114432439-a870e680-9bfb-11eb-8ccf-3a5c24f5ea06.png)
추천알고리즘을 통해 입력한 재료와 건강정보에 기반하여 가장 유사한 음식들을 분류별로 3가지씩 추천해줌.(분류 6가지 : 반찬, 피자/스파게티/스테이크, 국물요리, 면류/만두, 샐러드/스프, 밥/죽)

---

### 음식 상세정보 화면
![image](https://user-images.githubusercontent.com/22045179/114432865-1ae1c680-9bfc-11eb-8ed3-e5f8f814e169.png)
음식의 상세정보 페이지에서도 다른 음식을 검색할 수 있도록 검색란을 구성함.
음식명, 음식의 사진을 출력함.

![image](https://user-images.githubusercontent.com/22045179/114432994-42389380-9bfc-11eb-809c-0a7e0e45639a.png)
음식의 상세 정보(ex. 요리법, 요리재료, 기본정보, 요리과정, 음식정보)를 출력함.

![image](https://user-images.githubusercontent.com/22045179/114433243-8f1c6a00-9bfc-11eb-9ae9-7b264cc2973f.png)
모든 음식 상세정보의 하단에 youtube api를 이용하여 해당음식 만드는법에 대한 영상을 <iframe>으로 출력.
  
---

### 챗봇
재료의 상세 위주의 챗봇 시스템
재료에 대하여 자세히 알고 싶은 내용을 질문하면 NLP를 이용하여 질문의 핵심 재료를 찾고 미리 구성된 DB에 해당 재료가 있으면 DB의 문단에서 MRC를 이용하여 질문에 대한 답을 추론하여 사용자에게 출력하고, 미리 구성된 DB에 없다면 WIKIQA API를 이용하여 위키백과에서 답을 추론함.(사용된 open api : https://aiopen.etri.re.kr/)

![image](https://user-images.githubusercontent.com/22045179/114434760-54b3cc80-9bfe-11eb-9a8c-fe2c1fdf8da4.png)
우측 하단의 챗봇 버튼을 클릭하면 챗봇을 채팅방을 열 수 있음.
많은 홈페이지들이 챗봇버튼을 우측 하단에 위치시켰기 때문에 이 프로젝트에도 우측 하단에 자리함.(화면 스크롤시 우측 하단 위치에 고정되어 위치하여 있음)
X버튼 클릭시 채팅방 사라짐.

![image](https://user-images.githubusercontent.com/22045179/114434901-83ca3e00-9bfe-11eb-891d-294f7df82671.png)
NLP와 MRC를 이용하였기 때문에 질문의 형식을 다양하게 할 수 있음. (EX. 감자의 보관법은? | 감자 보관법은 뭐야? | 감자 보관법 | 감자 보관하는 방법알려줘 등등)

![image](https://user-images.githubusercontent.com/22045179/114435595-4ade9900-9bff-11eb-8609-7d8def71ccce.png)
채팅방의 형식으로 사용자가 한 질문과 그에 대한 대답을 출력함.

![image](https://user-images.githubusercontent.com/22045179/114435710-6fd30c00-9bff-11eb-9752-475fee5fe0c5.png)
채팅방처럼 계속하여 질문 할 수 있고, 전에 질문한 것들과 답들을 스크롤하여 볼 수 있음.

---

## 모바일화면 구성(screen width<=767px 반응형)
### 메인화면
![image](https://user-images.githubusercontent.com/22045179/114436658-8f1e6900-9c00-11eb-9761-d3cf5bd110de.png)
![image](https://user-images.githubusercontent.com/22045179/114436700-9e9db200-9c00-11eb-8e17-7298b70ec5e2.png)
![image](https://user-images.githubusercontent.com/22045179/114436749-ae1cfb00-9c00-11eb-89be-dbdb674d9049.png)

---

### 검색결과 화면
![image](https://user-images.githubusercontent.com/22045179/114436934-e4f31100-9c00-11eb-8ed7-35feac35a275.png)
![image](https://user-images.githubusercontent.com/22045179/114436978-f0463c80-9c00-11eb-9206-f3e89daedba7.png)

---

### 음식 상세정보 화면
![image](https://user-images.githubusercontent.com/22045179/114437040-03590c80-9c01-11eb-8698-bae8a6b39805.png)
![image](https://user-images.githubusercontent.com/22045179/114437084-0f44ce80-9c01-11eb-94f2-b1a76a246aa7.png)
![image](https://user-images.githubusercontent.com/22045179/114437137-1bc92700-9c01-11eb-9403-bb71fa5dee5b.png)

---

### 챗봇
![image](https://user-images.githubusercontent.com/22045179/114437313-5632c400-9c01-11eb-9a9b-43f2ada11a5b.png)
