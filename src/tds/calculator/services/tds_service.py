
from tds.calculator.common.logger import get_logger
from tds.calculator.common.utils import generate_unique_account_id
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from tds.calculator.models.binocs_model import BinocsId
from tds.calculator.models.user import User
from tds.calculator.models.trade import UserTradeDetail, TradeDetail, Amount
from tds.calculator.models.tds import UserTdsDetail, TdsDetail

TDS_VALUE_PERCENT = 1
logger = get_logger(__name__)

class TDSService:
    #TODO: use exchange_id for interaction with the binocs servers here (if any)
    #TODO: We should use the private key generated from the partner dashboard for secure
    #      communication
    def __init__(self, exchange_id: str, private_key: str, escrow_account: User, datastore):
        self.datastore = datastore
        self.escrow_account = escrow_account
        self.private_key = private_key
        self.exchange_id = exchange_id

    async def registerUser(self, user: User):
        logger.info("registering user with user body {}".format(user))

        binocs_id = BinocsId(id = generate_unique_account_id())
        self.datastore.save_user(binocs_id, user)
        #TODO: Securely register user on Binocs as well
        return binocs_id

    #Returns TDS
    def compute_tds(self, trade):
        taker_tds = None
        maker_tds = None

        #If user is getting paid in fiat, is a seller of the VDA with its consideration in Fiat.
        # => the user need not hold anything for TDS
        maker_consideration_fiat = trade.taker_amount.is_fiat()
        if maker_consideration_fiat == False:
            percent_amt = trade.maker_amount.percent_amt(TDS_VALUE_PERCENT)
            tds_details = TDSDetails(percent_amt)
            taker_tds = UserTDSDetail(trade.taker, tds_details)

        taker_consideration_fiat = trade.maker_amount.is_fiat()
        if taker_consideration_fiat == False:
            percent_amt = trade.taker_amount.percent_amt(TDS_VALUE_PERCENT)
            tds_details = TDSDetails(percent_amt)
            maker_tds = UserTDSDetail(trade.maker, tds_details)

        return trade, taker_tds, maker_tds

    async def tdsValue(self, trade: UserTradeDetail):
        trade, taker_tds, maker_tds = self.compute_tds(trade)

        if taker.is_resident('IN') and taker_tds:
            err = trade.maker_amount.reduce_amt(taker_tds)
            if err == 0:
                trade.add_tds(taker_tds)

        if maker.is_resident('IN') and maker_tds:
            err = trade.taker_amount.reduce_amt(maker_tds)
            if err == 0:
                trade.add_tds(maker_tds)

        #TODO: schedule a task to fetch the liquidation status (later)
        #TODO: @shakun, please save the following in the datastore
            # trade_id, maker_id -> maker_tds
            # trade_id, taker_id -> taker_tds
        return trade

    async def getTDSStatus(self, user, trade_id, page, limit):
        #TODO: @shakun, get the user_tds_details (saved above in tdsValue) and return
        #TODO: schedule a task to fetch the liquidation status
        #TODO: update if there is any change in the state in the DB
        document_filter = {}
        extra_args = {}
        if account_flag:
            document_filter["linked_exchanges"] = {"$elemMatch": {"account_flag": True}}
            extra_args.update({'linked_exchanges.$': 1, "user_id": 1})
        return await self.mongo_util.get_list(page, limit, document_filter, extra_args)
