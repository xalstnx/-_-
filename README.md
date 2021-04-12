# 캡스톤디자인 연구

## 주제 : 머신러닝을 활용한 콘텐츠 추천시스템

### 프로젝트 도메인 : http://todayrecipe.kro.kr or http://www.todayrecipe.kro.kr
(chrome 에서 최적화 되어있습니다.)

## PC화면 구성(screen width>=768px)
### 메인 화면
![image](https://user-images.githubusercontent.com/22045179/114431281-48c60b80-9bfa-11eb-8801-c1c29ea0efc9.png)
가운데 검색란에 가지고 있는 재료를 띄어쓰기 단위로 입력을 하고, 자신에게 해당되는 건강정보를 아래의 체크박스를 체크하여 검색함.
추천알고리즘을 통해 재료와 건강정보가 가장 많이 포함된 음식들을 분류별로 3가지씩 추천하여 보여줌.(검색결과 page)
![image](https://user-images.githubusercontent.com/22045179/114431378-66937080-9bfa-11eb-920b-cb9cec80ea4c.png)
(our service 내용 수정 예정 - 검색에 시스템 소개, 개발자 소개, 챗봇 시스템 소개)
![image](https://user-images.githubusercontent.com/22045179/114431480-7d39c780-9bfa-11eb-9439-08fff6f83ede.png)
분류별로 대표적인 음식을 소개함.


### 검색결과 화면
![image](https://user-images.githubusercontent.com/22045179/114432287-7bbccf00-9bfb-11eb-961a-b243f6f24f26.png)
검색결과 페이지에서도 다른 음식을 검색할 수 있도록 검색란을 구성함.
![image](https://user-images.githubusercontent.com/22045179/114432439-a870e680-9bfb-11eb-8ccf-3a5c24f5ea06.png)
추천알고리즘을 통해 입력한 재료와 건강정보에 기반하여 가장 유사한 음식들을 분류별로 3가지씩 추천해줌.(분류 6가지 : 반찬, 피자/스파게티/스테이크, 국물요리, 면류/만두, 샐러드/스프, 밥/죽)


### 음식 상세정보 화면
![image](https://user-images.githubusercontent.com/22045179/114432865-1ae1c680-9bfc-11eb-8ed3-e5f8f814e169.png)
음식의 상세정보 페이지에서도 다른 음식을 검색할 수 있도록 검색란을 구성함.
음식명, 음식의 사진을 출력함.
![image](https://user-images.githubusercontent.com/22045179/114432994-42389380-9bfc-11eb-809c-0a7e0e45639a.png)
음식의 상세 정보(ex. 요리법, 요리재료, 기본정보, 요리과정, 음식정보)를 출력함.
![image](https://user-images.githubusercontent.com/22045179/114433243-8f1c6a00-9bfc-11eb-9ae9-7b264cc2973f.png)
모든 음식 상세정보의 하단에 youtube api를 이용하여 해당음식 만드는법에 대한 영상을 <iframe>으로 출력.
