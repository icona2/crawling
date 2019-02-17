from iconservice import *

TAG = 'ABToken'

# class ABToken(IconScoreBase):
#
#     def __init__(self, db: IconScoreDatabase) -> None:
#         super().__init__(db)
#
#     def on_install(self) -> None:
#         super().on_install()
#
#     def on_update(self) -> None:
#         super().on_update()
#
#     @external(readonly=True)
#     def hello(self) -> str:
#         Logger.debug(f'Hello, world!', TAG)
#         return "Hello"
#
#     @external
#     def transaction_RT(self, _datetime: int, _value: str) -> str:
#         self._RealTimeSearchWordDB[_datetime] = _value
#         # return
#
#     @external(readonly=True)
#     def inquiry_RT(self, _Call_datetime: int) -> str:
#         # return "test"
#         return self._RealTimeSearchWordDB[_Call_datetime]

class ABToken(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._RealTimeSearchWordDB = DictDB("Crawling", db, value_type=str,depth=2)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def hello(self) -> str:
        Logger.debug(f'Hello, world!', TAG)
        return "Hello"

    @external
    def transaction_RT(self, _datetime_Ymd: int,_datetime_HM: int, _value: str) -> str:
        self._RealTimeSearchWordDB[_datetime_Ymd][_datetime_HM] = _value
        # return

    @external(readonly=True)
    def inquiry_RT(self, _Call_datetime_Ymd: int,_Call_datetime_HM:int) -> str:
        # return "test"
        return self._RealTimeSearchWordDB[_Call_datetime_Ymd][_Call_datetime_HM]
