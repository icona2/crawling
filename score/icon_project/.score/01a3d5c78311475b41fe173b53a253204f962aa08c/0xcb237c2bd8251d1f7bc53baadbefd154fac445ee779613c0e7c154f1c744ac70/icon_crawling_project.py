from iconservice import *

TAG = 'ICON_CRAWLING_SCORE'

class ICON_CRAWLING_SCORE(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._RealTimeSearchWordDB = DictDB("Crawling", db, value_type=str, depth=2)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()
    
    @external(readonly=True)
    def hello(self) -> str:
        Logger.debug(f'Hello, world!', TAG)
        return "Hello"

    @external
    def transaction_RT(self, _date: int, _time: int, _value: str) -> str:
        self._RealTimeSearchWordDB[_date][_time] = _value
        # return

    @external(readonly=True)
    def inquiry_RT(self, _Call_date: int, _Call_time: int) -> str:
        # return "test"
        return self._RealTimeSearchWordDB[_Call_date][_Call_time]