# LINE Bot Designer & Image Recognition (Sushi)
> TibaMe AI班個人專題

串接LINE Bot與GCP以及結合AI影像辨識，透過故事引導做**握壽司辨識**的解謎遊戲，並從中**蒐集用戶資料**。

## ◆專題需求

### 做一個故事化的機器人

* 數據蒐集
* 故事設計
* 模型優化
* 數據分析
* 雲端技術架構圖

## ◆使用簡介

### 加入好友

<img src="https://drive.google.com/uc?export=view&id=1zMtGyQMMA2Us5NFZ1U2yvrAKe_UAJlEw" height="350"> <img src="https://drive.google.com/uc?export=view&id=1AC4bfGmw1e0hjSiyLojQKv3Gn4NQTT_Z" height="150">  

### 開頭故事、劇情遊玩、影像辨識解謎

<img src="https://drive.google.com/uc?export=view&id=1F6Xgxo6ozgU-kGQtgtUFqXlVnUQ10f9O" height="300"> <img src="https://drive.google.com/uc?export=view&id=1mdnpysREFyOOIGUtjsblkypMmuI5TOHj" height="300"> <img src="https://drive.google.com/uc?export=view&id=19c9S5ajnJV5-lJY36ls3wCgOMINo6aDO" height="300">

## ◆開發環境

### 雲端部署

使用GCP串接LINE API以及存放用戶資訊及AI模型

<img src="https://drive.google.com/uc?export=view&id=1g0YOWeQM0_UPHcE83Zak6x8VG8nTXaIB" height="350">

## ◆AI模型

### Teachable Machine

<img src="https://drive.google.com/uc?export=view&id=1KkZrnqER8Xr0ATAlThxlbRi65qywDDKA" height="400">

### 模型調整

* **效果差** ※ 類別多、分太細

> 同一種魚肉依照部位與處理方式會有不同外觀，每種建不同分類。   
> -> AI學習後會認定是不同的分類，容易辨識錯誤。   

* **效果好** ※ 類別少、同種類集中

> 同一種魚類不論外觀放入同一分類。   
> -> AI學習效果好，辨識正確率較高。 

* **分類數量比較**

<table>
    <tr>
        <td>選用</td>
		<td>目標</td>
		<td>非目標</td>
	    	<td>正確率</td>
	    	<td>備註</td>
    </tr>
	<tr>
        <td></td>
		<td>14</td>
		<td>8</td>
		<td>60%</td>
		<td>目標14種=鮭魚*4+鮪魚*3+鮮蝦*3+豆皮*2+茶碗蒸*2</td>
    </tr>
	<tr>
        <td></td>
		<td>14</td>
		<td>1</td>
		<td>70%</td>
		<td>非目標1種=合併8種(景物+食物+...+碗盤+非目標壽司)</td>
    </tr>
	<tr>
        <td>V</td>
		<td>5</td>
		<td>1</td>
		<td>85%</td>
		<td></td>
    </tr>
</table>

## ◆使用資料庫解決問題

在Firestore儲存LINE執行紀錄，判斷影像辨識順序。

### 區分題目做回覆

	# 變數定義
	ret = 圖片辨識結果
	plot_dict = {1: '鮭魚all', 2: '鮪魚all', 3: '豆皮all'}
	user_dict["image_plot"] = 用戶執行紀錄(Firestore)

	# 判斷是否在劇情中
	if ret == '鮭魚all' and user_dict["image_plot"] == 1:
	    辨識結果回覆(謎題1)
	elif ret == '鮪魚all' and user_dict["image_plot"] == 2:
	    辨識結果回覆(謎題2)
	elif ret == '豆皮all' and user_dict["image_plot"] == 3:
	    辨識結果回覆(謎題3)
	else:
	    TextSendMessage('這個似乎跟答案不一樣\n換張圖片試試吧')

### 未開始解謎不做辨識

	else:
	line_bot_api.reply_message(
	    event.reply_token, [
	    TextSendMessage('圖片辨識服務尚未啟用\n請嘗試觸發劇情\n感謝您的配合\n(ノ・ω・)ノヾ(・ω・ヾ)'),
	    ])

## ◆數據分析

### Firestore用戶資料統計

使用FlexSendMessage在LINE做呈現，內容包括選項比例、點擊次數、總人數。

* 壽司喜好  

<img src="https://drive.google.com/uc?export=view&id=1XQmsoH9I0WDzvuEX_c6QzgZAOENaYliJ" height="300">

* 點選次數  

<img src="https://drive.google.com/uc?export=view&id=1veSSNj5KTTYRT62D2U-yrvb5zXGyLREf" height="300">

## ◆使用套件、素材、參考文件

### 套件

* flask
* flask_cors
* gunicorn
* line-bot-sdk
* google-cloud-firestore
* google-cloud-storage
* google-cloud-logging
* tensorflow-cpu

### 素材  

* かわいいフリー素材集 いらすとや   
https://www.irasutoya.com/
* 國家教育研究院愛學網   
https://stv.naer.edu.tw/watch/289393   
  ※ LINE出現之圖像包括遊戲、漫畫、廣告等畫面作為課堂專題效果，不用於商業用途。  
### 參考  
* Github  
https://github.com/BingHongLi/ncu_gcp_ai_project

## ◆影片、簡報  
* YouTube Demo   
https://youtu.be/Zzl-CJYvd6g
* Google Slides   
https://docs.google.com/presentation/d/1e-n4lapAOJS_WogTwO4nzaMzoQs4G0P43-X8Pjkevok/edit?usp=sharing
