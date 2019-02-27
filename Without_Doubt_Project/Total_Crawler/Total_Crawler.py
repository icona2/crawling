#-----------------------------------------Time Recycle----------------------------------------------
from apscheduler.schedulers.blocking import BlockingScheduler
import threading


#-----------------------------------------crawling----------------------------------------------
import requests, time, datetime
from bs4 import BeautifulSoup
from selenium import webdriver


#---------------------------------------db connect----------------------------------------------
import pymysql


#---------------------------------------Icon SCORE Service--------------------------------------
import json
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet

'''
#time check
t = time.time()
now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
with open('/home/lyu/PycharmProjects/Without_Doubt_Project/Total_Crawler/log.txt', 'a+') as f:
    f.write(now+"\n")
'''


#---------------------------------------Icon SerFvice rink---------------------------------------
icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io/api/v3"))
_score_address = "cx58833c3d35953053ecc21bf814ce117765c640e4"
_keystore_address = "hx62ad26ca172e347300fa795bb5b554c9123b64ed"
wallet = KeyWallet.load("../testnet_keystore", "1q2w3e4r!")



#-------------------------------------------Main source------------------------------------------
class calltransaction_transaction_RT():
    while(1):
        # def Crawling_main():
        start_time = time.time()
        # t = time.time()
        # now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))
        # with open('/home/lyu/PycharmProjects/Without_Doubt_Project/Total_Crawler/Time_log.txt', 'a+') as f:
        #     f.write(now + "\n")

        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        nowTime = now.strftime('%H%M')


        html = requests.get('https://www.naver.com/').text
        soup = BeautifulSoup(html, 'html.parser')
        title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
        Machined_title_list = list()
        for idx, title in enumerate(title_list, 1):
            Machined_title_list.append(title.text)

        print(Machined_title_list)
        params = {
            "_date": nowDate,
            "_time": nowTime,
            "_div": 'NAVER',
            "_value": json.dumps(Machined_title_list)
        }

        transaction = CallTransactionBuilder() \
            .from_(_keystore_address) \
            .to(_score_address) \
            .step_limit(10_000_000) \
            .nid(3) \
            .nonce(100) \
            .method("transaction_RT") \
            .params(params) \
            .build()
        print(nowDate, nowTime, 'NAVER')
        signed_transaction = SignedTransaction(transaction, wallet)
        tx_hash = icon_service.send_transaction(signed_transaction)
        #
        # print(tx_hash)
        time.sleep(5)
        # tx_result = icon_service.get_transaction_result(tx_hash)
        # print(tx_result['status'])
        print("--- %s seconds ---" % (time.time() - start_time))

        #---------------------------------------------GOOGLE----------------------------------------
        now = datetime.datetime.now()
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=800x600')
        # options.add_argument("disable-gpu")
        # path = "/home/lyu/Downloads/chromedriver"
        # driver = webdriver.Chrome(path, chrome_options=options)

        # driver.get("https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all")
        #
        # #driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]').click()
        # element = driver.find_element_by_css_selector("body > div.trends-wrapper > div:nth-child(2) > div > div.feed-content > div > div.feed-load-more-button")
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        path = "/home/lyu/Downloads/chromedriver"
        driver = webdriver.Chrome(path, chrome_options=options)
        driver.get("https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all")

        # driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]').click()



        element = driver.find_element_by_css_selector("body > div.trends-wrapper > div:nth-child(2) > div > div.feed-content > div > div.feed-load-more-button")
        # element.click()
        # time.sleep(4)
        #element2 = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div[2]")
        #print(element)
        #print(element2)
        req = driver.page_source

        soup = BeautifulSoup(req, 'html.parser')

        # time.sleep(10)
        title_list = soup.select('div > span:nth-child(1) > a')
        if ((len(title_list)) <= 20):
            element.click()
            time.sleep(4)
            title_list = soup.select('div > span:nth-child(1) > a')


        # shit_list = soup.select('body > div.trends-wrapper > div:nth-child(2) > div > div.feed-content > div > div.feed-load-more-button')
        # print(shit_list)


        # while not title_list or len(title_list) < 10:
        #     now = datetime.datetime.now()
        #     options = webdriver.ChromeOptions()
        #     options.add_argument('headless')
        #     options.add_argument('window-size=800x600')
        #     options.add_argument("disable-gpu")
        #     path = "/home/lyu/Downloads/chromedriver"
        #     driver = webdriver.Chrome(path, chrome_options=options)
        #
        #     driver.get("https://trends.google.com/trends/trendingsearches/realtime?geo=US&category=all")
        #     element = driver.find_element_by_css_selector("body > div.trends-wrapper > div:nth-child(2) > div > div.feed-content > div > div.feed-load-more-button")
        #     element.click()
        #     time.sleep(2)
        #     # element = driver.find_element_by_xpath("body > div.trends-wrapper > div:nth-child(2) > div > div.feed-content > div > div.feed-load-more-button")
        #     # element2 = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div[2]")
        #     # print(element)
        #     # print(element2)
        #     #driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/div[2]').click()
        #     #driver.execute_script("arguments[0].click();", element)
        #     req = driver.page_source
        #
        #     soup = BeautifulSoup(req, 'html.parser')
        #     # time.sleep(10)
        #     title_list = soup.select('div > span:nth-child(1) > a')




        Temp_list = title_list[0:20]
        Machined_Google_title_list = list()

        for title in Temp_list:
            Machined_Google_title_list.append(title.text.strip())
        print(Machined_Google_title_list)

        params_G = {
            "_date": nowDate,
            "_time": nowTime,
            '_div': 'GOOGLE',
            "_value": json.dumps(Machined_Google_title_list)
        }
        transaction_G = CallTransactionBuilder() \
            .from_(_keystore_address) \
            .to(_score_address) \
            .step_limit(10_000_000) \
            .nid(3) \
            .nonce(100) \
            .method("transaction_RT") \
            .params(params_G) \
            .build()
        print(nowDate, nowTime, 'GOOGLE')
        signed_transaction_G = SignedTransaction(transaction_G, wallet)
        tx_hash_G = icon_service.send_transaction(signed_transaction_G)
        print("--- %s seconds ---" % (time.time() - start_time))
        #------------time sleep-------------------------------------
        # print(tx_hash_G)
        # time.sleep(10)
        # tx_result_G = icon_service.get_transaction_result(tx_hash_G)
        # print(tx_result_G['status'])

        # ------------------------Google DB Con------------------------

        # MySQL Connection 연결
        conn = pymysql.connect(host='127.0.0.1', user='admin', password='rootroot',
                               db='Crawling_DB', charset='utf8')

        # Connection 으로부터 Cursor 생성
        # curs = conn.cursor()
        curs = conn.cursor(pymysql.cursors.DictCursor)

        b = 20

        # 현재 1등 데이터가 TOP20 테이블에 이미 존재하고 있는지 검사
        check = Machined_Google_title_list[0]
        sql = "select * from crawling_App_receive_google_data where key1=%s and G_Word=%s"
        curs.execute(sql, (nowDate, check))
        check_resuit = curs.fetchall()
        if not check_resuit:
            print("Warning:%s" %check)

        # 가져온 20개의 키워드 insert, update
        for a in Machined_Google_title_list:
            # orgin score call

            # 검색된 단어의 점수가 존재하는 지, 몇점인지 확인한다.
            sql = "select G_Rating from crawling_App_receive_google_data where key1=%s and G_Word=%s"
            curs.execute(sql, (nowDate, a))
            num = curs.fetchall()

            if num:
                # print("already exist")
                for x in num:
                    d = list(x.values())
                    k = int(d[0])
                    k = k + b
                    # 만약 a[0]값이 crawling_receive_google_data에 없으며 주의 메세지 출력

                    sql = "UPDATE crawling_App_receive_google_data SET G_Rating=%s WHERE G_Word=%s"
                    #### 전날 날짜에 업데이트 하게되는 문제
                    curs.execute(sql, (k, a))
                    rows = curs.fetchall()
                    conn.commit()

            else:
                # print("New Input")
                sql = "INSERT INTO crawling_App_receive_google_data (key1,G_Word,G_Rating) VALUES(%s,%s,%s)"
                # sql = "select * from crawling_receive_google_data where key1=%s and G_Word='abc' and G_Rating=%s" % (nowDate, b)
                curs.execute(sql, (nowDate, a, b))
                rows = curs.fetchall()
                conn.commit()

            b = b - 1

        sql = "select G_Word from crawling_App_receive_google_data where key1=%s" % (nowDate)
        curs.execute(sql)
        rows = curs.fetchall()
        print(rows)

        # ------------------------Naver DB Con------------------------

        b=20

        check = Machined_title_list[0]
        sql = "select * from crawling_App_receive_naver_data where key1=%s and N_Word=%s"
        curs.execute(sql, (nowDate, check))
        check_resuit = curs.fetchall()
        if not check_resuit:
            print("Warning!!!")

        # 가져온 20개의 키워드 insert, update
        for a in Machined_title_list:
            # orgin score call

            # 검색된 단어의 점수가 존재하는 지, 몇점인지 확인한다.
            sql = "select N_Rating from crawling_App_receive_naver_data where key1=%s and N_Word=%s"
            curs.execute(sql, (nowDate, a))
            num = curs.fetchall()

            if num:
                # print("already exist")
                for x in num:
                    d = list(x.values())
                    k = int(d[0])
                    k = k + b
                    # 만약 a[0]값이 crawling_receive_google_data에 없으며 주의 메세지 출력

                    sql = "UPDATE crawling_App_receive_naver_data SET N_Rating=%s WHERE N_Word=%s"
                    #### 전날 날짜에 업데이트 하게되는 문제
                    curs.execute(sql, (k, a))
                    rows = curs.fetchall()
                    conn.commit()

            else:

                # print("New Input")
                sql = "INSERT INTO crawling_App_receive_naver_data (key1,N_Word,N_Rating) VALUES(%s,%s,%s)"
                # sql = "select * from crawling_receive_google_data where key1=%s and G_Word='abc' and G_Rating=%s" % (nowDate, b)
                curs.execute(sql, (nowDate, a, b))
                rows = curs.fetchall()
                conn.commit()

            b = b - 1

        sql = "select N_Word from crawling_App_receive_naver_data where key1=%s" % (nowDate)
        curs.execute(sql)
        rows = curs.fetchall()
        print(rows)

        conn.close()

        print("===========================================================================================================================================")
        print("start_time", start_time)
        k= (time.time() - start_time)
        print("--- %s seconds ---" % (time.time() - start_time))
        god = int((60 - (time.time() - start_time)))
        time.sleep(god)


    # threading.Timer(60,self.Crawling_main).start()
# sched = BlockingScheduler()
# sched.add_job(Crawling_main, 'interval', seconds=60)
# sched.start()
# def main():
#     at = calltransaction_transaction_RT()
#     at.Crawling_main()
#
# if __name__ == '__main__':
#     main()
