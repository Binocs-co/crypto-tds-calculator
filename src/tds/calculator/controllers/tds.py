from fastapi import APIRouter
from typing import List
from tds.calculator.services.tds_service import TDSService
from tds.calculator.models.binocs_model import BinocsId
from tds.calculator.models.tds import TDSDeductionDetail
from tds.calculator.models.tds import TDSDetail
from tds.calculator.models.trade import UserTradeDetail
from tds.calculator.models.trade import TradeAcknowledgement
from tds.calculator.models.trade import TradeDetail
from tds.calculator.models.user import User
from tds.calculator.custom_router.ExceptionHandlerLoggingRoute import ExceptionHandlerLoggingRoute

tds_service = TDSService()
router = APIRouter(prefix="/tds", tags=["tds"], route_class=ExceptionHandlerLoggingRoute)

@router.post(path="/register-user", response_model=BinocsId)
async def registerUser(user: User):
    registered_id: BinocsId = await tds_service.registerUser(user)
    return registered_id

@router.post(path="/add_trade", response_model=TradeAcknowledgement)
async def addTrade(tradeDetail: TradeDetail):
    tradeAcknowledgement: TradeAcknowledgement = await tds_service.addTade(tradeDetail)
    return tradeAcknowledgement

@router.get(path="/estimate_tds", response_model=TDSDetail)
async def estimateTDS(userTradeDetail: UserTradeDetail):
    tdsDetail: TDSDetail = await tds_service.estimateTDS(userTradeDetail)
    return tdsDetail

@router.post(path="/deduct_tds", response_model=TDSDeductionDetail)
async def deductTDS(userTradeDetail: UserTradeDetail):
    tdsDeductionDetail: TDSDeductionDetail = await tds_service.deductTDS(userTradeDetail)
    return tdsDeductionDetail

@router.get(path="/status", response_model=List[User], response_model_exclude_unset=True)
async def status(account_flag: bool = False, page: int = 1, limit: int = 10):
    user = await tds_service.getTDSList(account_flag, page, limit)
    return user