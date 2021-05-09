bestk.py 는 업비트에 존재하는 모든 암호화폐의 예전값을 조회하여 일마다의 (3~7일) k값을 대입하여 좋은 k값을 보여줍니다.<br>
.txt 확장자로 나오며, 업비트API가 빠르게 값을 불러오면 차단하여, sleep 기능을 넣었습니다. (딜레이 기능입니다.)<br>
실행하면 저장될 때까지 약 10분 넘게 걸립니다.<br>
~~메모장으로 열어 ctrl+f로 값을 검색해주세요.<br>
bestk.py 는 이후에 엑셀파일로 나오게 수정할 예정입니다.<br>~~

**이제 엑셀파일로 값이 나옵니다.**
![image](https://user-images.githubusercontent.com/61561973/116899903-19437580-ac73-11eb-81a4-eed642b6693b.png)<br>
엑셀파일 실행 후 필터설정 해주세요.<br>
![image](https://user-images.githubusercontent.com/61561973/116899954-295b5500-ac73-11eb-96ab-6d8738e4b0d9.png)<br>
그러면 이렇게 오름/내림차순 정렬을 할 수 있습니다.
<br><br>
backtest.py 는 해당 코인의 과거 7일의 값을 조회 한 후 수익률, 누적 수익률 등이 엑셀 파일로 저장됩니다.<br>
count 값에 몇일을 조회할 지 넣으시고, k 값에는 말 그대로 k 값을 넣으시면 됩니다.<br>

AutomaticTradeSlack.py 는 access, secret 에 각각 업비트 API에 있는 값을 넣고 myToken 는 slack 토큰 값을 넣으시면 됩니다.<br>
coinName 에는 코인 이름을 예 : BTC<br>
tradingCoin에는 KRW-코인 이름을 넣으시면 됩니다. 예 : KRW-BTC<br>
k 에는 말 그대로 k 값을 넣으시면 됩니다. 예 : 0.5<br>
나머지는 코드 내에 주석을 보시면 될 듯 합니다.<br>
<br><br>
이후 AutomaticTradeSlack.py 를 입맛에 맞게 수정하신 후 서버같은 곳에 돌리시면 됩니다.<br>
자세한 설명은 https://blog.naver.com/jungdol0202/222344158039 들어가시면 됩니다.
