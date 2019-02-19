#---------------------------------------naver crawling-----------------------------------------
import requests, time, datetime
from bs4 import BeautifulSoup

#---------------------------------------Icon SCORE TEST-----------------------------------------
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder

# Creates an IconService instance using the HTTP provider and set a provider.
from iconsdk.wallet.wallet import KeyWallet

icon_service = IconService(HTTPProvider("http://127.0.0.1:8000/api/v3"))

_score_address = "cx8230b22610d31d2f10e1a468ef1291fe110d6c79"
_keystore_address = "hx8c846f5747ccb9f41191de1c43061657fc066518"

wallet = KeyWallet.load("./master_key", "wjdgh1025!")

class call_hello():
    call = CallBuilder()\
        .from_(_keystore_address) \
        .to(_score_address) \
        .method("hello") \
        .build()

    # Sends the call request
    #response = self.process_call(call, self.icon_service)
    response = icon_service.call(call)

    #assertEqual("Hello", response)i
    print(response)

class calltransaction_transaction_RT():
        html = requests.get('https://www.naver.com/').text
        soup = BeautifulSoup(html, 'html.parser')
        now = datetime.datetime.now()
        title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
        Machined_title_list = list()
        for idx, title in enumerate(title_list, 1):
            Machined_title_list.append(title.text)
        print(Machined_title_list)
        nowDate = now.strftime('%Y%m%d')
        nowTime = now.strftime('%H%M')

        params = {
            "_date": nowDate,
            "_time": nowTime,
            "_ranking": idx,
            "_value": Machined_title_list
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

        signed_transaction = SignedTransaction(transaction, wallet)
        tx_hash = icon_service.send_transaction(signed_transaction)
        print(tx_hash)
        time.sleep(10)
        tx_result = icon_service.get_transaction_result(tx_hash)
        print(tx_result['status'])

        '''
            if(tx_result['status'] == 0):
                failure_Date = nowDate
                failure_Time = nowTime
                failure_idx = idx
                failure_title = title.text
            
            params = {
                "_Call_date": nowDate,
                "_Call_time": nowTime,
                "_Call_ranking": idx
            }

            Inquiry = CallBuilder()\
                .from_(_keystore_address) \
                .to(_score_address) \
                .method("inquiry_RT") \
                .params(params) \
                .build()

            # Sends the call request
            response = icon_service.call(Inquiry)

            # check call result
            print(response)
            '''