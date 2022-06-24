
from tds.calculator.common.logger import get_logger
from tds.calculator.common.utils import generate_unique_account_id
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from tds.calculator.models.binocs_model import BinocsId
from tds.calculator.models.user import User
from tds.calculator.models.trade import UserTradeDetail, TradeDetail, Amount
from tds.calculator.models.tds import UserTdsDetail, TdsDetail

logger = get_logger(__name__)

class TDSService:
    #TODO: use exchange_id for interaction with the binocs servers here (if any)
    #TODO: We should use the private key generated from the partner dashboard for secure
    #      communication
    def __init__(self, exchange_id: str, private_key: str, escrow_account, datastore):
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
        return {}

    async def tdsValue(self, trade: UserTradeDetail):
        tds_details = self.compute_tds(trade)

        #Buyer: Resident - Seller: Resident
        if buyer.is_resident('IN') and seller.is_resident('IN'):
            pass
        #Buyer: Resident - Seller: Non_Resident
        if buyer.is_resident('IN') and !seller.is_resident('IN'):
            del tds_details[seller.exchange_user_id]
        #Buyer: Non_resident - Seller: Resident
        if !buyer.is_resident('IN') and seller.is_resident('IN'):
            del tds_details[buyer.exchange_user_id]
        if !buyer.is_resident('IN') and !seller.is_resident('IN'):
            del tds_details[buyer.exchange_user_id]
            del tds_details[seller.exchange_user_id]

        #TODO: schedule a task to fetch the liquidation status (later)
        #TODO: @shakun, please save it in the datastore
        return tds_details

    async def getTDSStatus(self, account_flag, page, limit):
        #TODO: @shakun, get the user_tds_details (saved above in tdsValue) and return
        #TODO: schedule a task to fetch the liquidation status
        #TODO: update if there is any change in the state in the DB
        document_filter = {}
        extra_args = {}
        if account_flag:
            document_filter["linked_exchanges"] = {"$elemMatch": {"account_flag": True}}
            extra_args.update({'linked_exchanges.$': 1, "user_id": 1})
        return await self.mongo_util.get_list(page, limit, document_filter, extra_args)
