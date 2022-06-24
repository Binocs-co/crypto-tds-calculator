from fastapi import APIRouter
from typing import List
from tds.calculator.services.tds_service import TDSService
from tds.calculator.models.binocs_model import BinocsId
from tds.calculator.models.tds import UserTDSDetail, TDSDetail
from tds.calculator.models.trade import UserTradeDetail
from tds.calculator.models.user import User
from tds.calculator.custom_router.ExceptionHandlerLoggingRoute import ExceptionHandlerLoggingRoute

private_key = ''      #TODO: @Shakun, to fetch the key which was downloaded from the partner dashboard
escrow_account = None #TODO: @Exchange team to define the format of the account. Will be used to
                      #      deduct the TDS
data_store = None     #Redis DB Access
tds_service = TDSService('bitbns', private_key, escrow_account, data_store)
router = APIRouter(prefix="/tds", tags=["tds"], route_class=ExceptionHandlerLoggingRoute)

'''
    NOTE: this API registers on Binocs server as well with exchange_user_id & PAN
    POST /tds-register-user/
    Parameters:
        exchange_user_id | string | mandatory | unique_id of the user (e.g. email)
        PAN     | string  | mandatory     | PAN details of the user
                                            The value can be “NA” for non-residents
                                            In case PAN is missing, we will consider the user as
                                            non-resident.
        ITR_ack | boolean | mandatory     | Acknowledgement from the user that they are filing ITR in
                                            the last 2 years. This
        exempt  | boolean | default=false | If the user is exempted from the TDS deduction.
                                            This is required for scenarios when the user is a broker.
                                            This can also be used for Binocs escrow account.
                                            In case it is not passed, we will assume the user's TDS
                                            needs to be deducted always.
    Response:
        binocs-id | string
'''
@router.post(path="/tds-register-user", response_model=BinocsId)
async def registerUser(user: User):
    registered_id: BinocsId = await tds_service.registerUser(user)
    return registered_id

'''
    GET /tds-value/
    Parameters
        taker_id: string | mandatory | exchange_user_id of the taker
        maker_id: string | mandatory | exchange_user_id of the maker
        tx-detail | json | mandatory | [{type: string, timestamp: int,
                                amount: [value: int, coin: string, decimal: int]}]
    tx_type: buy_trade | sell_trade | lending | fixed-income | coupon | …
    Return
        tds | [{exchange_user_id: amount: [value: int, coin: string, decimal: int]}]
        binocs-account-details | account details in the exchange [TBD]
'''
@router.get(path="/tds-value", response_model=List[UserTDSDetail])
async def tradeTDS(userTradeDetail: UserTradeDetail):
    userTDSDetail: UserTDSDetail = await tds_service.tdsValue(userTradeDetail)
    return userTDSDetail

'''
    Get /tds-status/
    Parameters:
        user_id | string | exchange_user_id of the user
        trade_id | string | optional
    Return:
        [trade_id: string, fiat_value: float, challan: url, status: string | (Paid/Liquidated/Pending/..)]

'''
@router.get(path="/tds-status", response_model=List[UserTDSDetail], response_model_exclude_unset=True)
async def status(user: User, trade_id: str = None, page: int = 1, limit: int = 10):
    userTDSDetail: UserTDSDetail = await tds_service.getTDSStatus(user, trade_id, page, limit)
    return userTDSDetail
