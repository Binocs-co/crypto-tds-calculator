
from tds.calculator.common.logger import get_logger
from tds.calculator.common.utils import generate_unique_account_id
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from tds.calculator.models.binocs_model import BinocsId
from tds.calculator.models.user import User

logger = get_logger(__name__)


class TDSService:
    def __init__(self):
        pass
    
    async def registerUser(self, user: User):
        logger.info("registering user with user body {}".format(user))
        return BinocsId(id = generate_unique_account_id())

    async def addTade(self, user_id: str, user: User):
        logger.info("updating  user with user body {}".format(user))
        return await self.mongo_util.update_one({"user_id": user_id}, user)

    async def estimateTDS(self, user_id: str):
        return await self.mongo_util.get({"user_id": user_id})

    async def deductTDS(self, user_id: str):
        return await self.mongo_util.delete_one({"user_id": user_id})
    
    async def getTDSList(self, account_flag, page, limit):
        document_filter = {}
        extra_args = {}
        if account_flag:
            document_filter["linked_exchanges"] = {"$elemMatch": {"account_flag": True}}
            extra_args.update({'linked_exchanges.$': 1, "user_id": 1})
        return await self.mongo_util.get_list(page, limit, document_filter, extra_args)