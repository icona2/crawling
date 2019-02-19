# #
# import os
# import requests, time, datetime
# from iconsdk.builder.transaction_builder import DeployTransactionBuilder ,CallTransactionBuilder
# from iconsdk.builder.call_builder import CallBuilder
# from iconsdk.icon_service import IconService
# from iconsdk.libs.in_memory_zip import gen_deploy_data_content
# from iconsdk.providers.http_provider import HTTPProvider
# from iconsdk.signed_transaction import SignedTransaction
#
# from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
#
# DIR_PATH = os.path.abspath(os.path.dirname(__file__))
#---------------------------------------naver crawling-----------------------------------------
import requests, time, datetime
from bs4 import BeautifulSoup

#---------------------------------------Icon SCORE TEST-----------------------------------------
import os

# ICON Transaction lib
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
# ICON Transaction lib
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider

# SCORE integration unittest test class
from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS

DIR_PATH = os.path.abspath(os.path.dirname(__file__))




class TestABToken(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"
    SCORE_PROJECT= os.path.abspath(os.path.join(DIR_PATH, '..'))

    def setUp(self):
        super().setUp()

        self.icon_service = None
        # if you want to send request to network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3
        # self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))

        # install SCORE
        self._score_address = self._deploy_score()['scoreAddress']

    def _deploy_score(self, to: str = SCORE_INSTALL_ADDRESS) -> dict:
        # Generates an instance of transaction for deploying SCORE.
        transaction = DeployTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(to) \
            .step_limit(100_000_000_000) \
            .nid(3) \
            .nonce(100) \
            .content_type("application/zip") \
            .content(gen_deploy_data_content(self.SCORE_PROJECT)) \
            .build()

        # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)

        # process the transaction in local
        tx_result = self.process_transaction(signed_transaction, self.icon_service)

        self.assertTrue('status' in tx_result)
        self.assertEqual(1, tx_result['status'])
        self.assertTrue('scoreAddress' in tx_result)

        return tx_result

    def test_score_update(self):
        # update SCORE
        tx_result = self._deploy_score(self._score_address)

        self.assertEqual(self._score_address, tx_result['scoreAddress'])

    def test_call_hello(self):
        # Generates a call instance using the CallBuilder
        call = CallBuilder().from_(self._test1.get_address()) \
            .to(self._score_address) \
            .method("hello") \
            .build()

        # Sends the call request
        response = self.process_call(call, self.icon_service)

        self.assertEqual("Hello", response)

    def test_calltransaction_transaction_RT(self):

        html = requests.get('https://www.naver.com/').text
        soup = BeautifulSoup(html, 'html.parser')
        now = datetime.datetime.now()
        title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
        # while(1):
        #     time.sleep(5)
        for idx, title in enumerate(title_list, 1):

            nowDatetime_Ymd = now.strftime('%Y%m%d')
            nowDatetime_HM = now.strftime('%H%M')
            params = {
                "_datetime_Ymd": nowDatetime_Ymd,
                "_datetime_HM": nowDatetime_HM,
                "_value": title.text
            }
            transaction = CallTransactionBuilder() \
                .from_(self._test1.get_address()) \
                .to(self._score_address) \
                .step_limit(10_000_000) \
                .nid(3) \
                .nonce(100) \
                .method("transaction_RT") \
                .params(params) \
                .build()

            signed_transaction = SignedTransaction(transaction, self._test1)
            tx_result = self.process_transaction(signed_transaction, self.icon_service)
            # print(idx, nowDatetime, title.text)

            params = {
                "_Call_datetime_Ymd": nowDatetime_Ymd,
                "_Call_datetime_HM": nowDatetime_HM
            }

            Inquiry = CallBuilder().from_(self._test1.get_address()) \
                .to(self._score_address) \
                .method("inquiry_RT") \
                .params(params) \
                .build()

            # Sends the call request
            response = self.process_call(Inquiry, self.icon_service)
            #
            #
            #             # check call result
            print(response)


    # def call_receive(self):
    #     num = {
    #         "_datetime": 201902140913,
    #         "_value": "title.text"
    #     }
    #
    #     transaction = CallTransactionBuilder() \
    #         .from_(self._test1.get_address()) \
    #         .to(self._score_address) \
    #         .step_limit(10_000_000) \
    #         .nid(3) \
    #         .nonce(100) \
    #         .method("transaction_RT") \
    #         .params(num) \
    #         .build()
    #
    #     signed_transaction = SignedTransaction(transaction, self._test1)
    #     tx_result = self.process_transaction(signed_transaction, self.icon_service)
    #
    #     params = {
    #         "_Call_datetime": 201902140913
    #     }
    #
    #     Inquiry = CallBuilder().from_(self._test1.get_address()) \
    #         .to(self._score_address) \
    #         .method("inquiry_RT") \
    #         .params(params) \
    #         .build()
    #
    #     # Sends the call request
    #     response = self.process_call(Inquiry, self.icon_service)
    #
    #     # check call result
    #     print(response)
    #
    #
    #
    #
    #     count_default = 0
    #     count_total = 5
    #
    #     while (count_default < count_total):
    #
    #         html = requests.get('https://www.naver.com/').text
    #         soup = BeautifulSoup(html, 'html.parser')
    #         now = datetime.datetime.now()
    #
    #         title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
    #
    #         time.sleep(60)
    #         for idx, title in enumerate(title_list, 1):
    #             print(idx, now, title.text)