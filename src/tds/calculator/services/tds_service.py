
from tds.calculator.common.logger import get_logger
from tds.calculator.common.utils import generate_unique_account_id
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from tds.calculator.models.binocs_model import BinocsId
from tds.calculator.models.user import User
from tds.calculator.models.trade import UserTradeDetail
from tds.calculator.models.tds import UserTDSDetails, TDSDetails
from tds.calculator.common.datastore.datastore import Datastore

from datetime import datetime

TDS_VALUE_PERCENT = 100
logger = get_logger(__name__)
datastore = Datastore()

class TDSService:
    #TODO: use exchange_id for interaction with the binocs servers here (if any)
    #TODO: We should use the private key generated from the partner dashboard for secure
    #      communication
    def __init__(self, exchange_id: str, private_key: str, escrow_account: User):
        self.escrow_account = escrow_account
        self.private_key = private_key
        self.exchange_id = exchange_id

    def is_verified(self, exchange : str, signature : str) :
        return True

    async def registerUser(self, user: User, exchange : str, signature : str):
        logger.info("registering user with user body {}".format(user))

        binocs_id = BinocsId(id = generate_unique_account_id())
        user.exchange_id = exchange if exchange else self.exchange_id
        user.binocs_id = binocs_id
        #user.create_date = datetime.now()
        #user.updated_date = datetime.now()
        datastore.set_user(user.exchange_user_id, user)
        return binocs_id

    #Returns TDS
    def compute_tds(self, trade : UserTradeDetail):
        taker_tds = None
        maker_tds = None

        #If user is getting paid in fiat, is a seller of the VDA with its consideration in Fiat.
        # => the user need not hold anything for TDS
        maker_consideration_fiat = trade.taker_amount.is_fiat()
        if maker_consideration_fiat == False:
            percent_amt = trade.maker_amount.percent_amt(TDS_VALUE_PERCENT)
            tds_details = TDSDetails(amount = percent_amt)
            taker_tds = UserTDSDetails(user = trade.taker, trade_id = trade.trade_id, timestamp = trade.timestamp, tds_details = tds_details)

        taker_consideration_fiat = trade.maker_amount.is_fiat()
        if taker_consideration_fiat == False:
            percent_amt = trade.taker_amount.percent_amt(TDS_VALUE_PERCENT)
            tds_details = TDSDetails(amount = percent_amt)
            maker_tds = UserTDSDetails(user = trade.maker, trade_id = trade.trade_id, timestamp = trade.timestamp, tds_details = tds_details)

        return trade, taker_tds, maker_tds

    async def tdsValue(self, trade: UserTradeDetail, exchange : str, signature : str):
        trade.taker = datastore.get_user(trade.taker.exchange_user_id)
        trade.maker = datastore.get_user(trade.maker.exchange_user_id)

        trade, taker_tds, maker_tds = self.compute_tds(trade)

        if trade.taker.is_resident('IN') and taker_tds:
            err = trade.maker_amount.reduce_amt(taker_tds.tds_details.amount)
            if err == 0:
                trade.taker_tds_details = taker_tds

        if trade.maker.is_resident('IN') and maker_tds:
            err = trade.taker_amount.reduce_amt(maker_tds.tds_details.amount)
            if err == 0:
                trade.maker_tds_details = maker_tds
    
        trade.exchange_id = self.exchange_id
        
        # user_id, trade_id, timestamp
        #TODO: schedule a task to fetch the liquidation status (later)
        trade.create_date = datetime.now()
        trade.updated_date = datetime.now()
        datastore.set_trade(trade.trade_id, trade)
        #TODO: @shakun, please save the following in the datastore
            # trade_id, maker_id -> maker_tds
            # trade_id, taker_id -> taker_tds
        return trade

    async def getTDSStatus(self, user_id, trade_id, page, limit, exchange : str, signature : str):
        #TODO: schedule a task to fetch the liquidation status
        return datastore.get_tds_details(user_id, trade_id, page, limit)
