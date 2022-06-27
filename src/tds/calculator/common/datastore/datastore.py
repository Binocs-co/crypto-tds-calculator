from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tds.calculator.common.configuration import config
from tds.calculator.common.datastore.models import Base

from tds.calculator.models.user import User
from tds.calculator.models.trade import UserTradeDetail

from tds.calculator.common.datastore import models

class Datastore(object) :

    def __init__(self) :
        self.hostname = config.MYSQL_HOSTNAME
        self.username = config.MYSQL_USERNAME
        self.password = config.MYSQL_PASSWORD
        self.dbname = config.MYSQL_DBNAME
        self.__connect_db()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
 
    def __connect_db(self) :
        self.engine = create_engine("mysql+mysqlconnector://%s:%s@%s:3306/%s" % 
            (self.username, self.password, self.hostname, self.dbname), 
            pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)

        # Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
        retry_count = 1
        while (retry_count <= 3):
            try:
                Base.metadata.create_all(self.engine)
                break
            except Exception as e:
                print(('Exception occured - {}. Retrying.'.format(e)))
                retry_count += 1

        Base.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)

    def get_user(self, user_id : str) :
        with self.session_scope() as db_session :
            model_user = db_session.query(models.User).filter(models.User.exchange_user_id == user_id).first()
            if model_user :
                return User(exchange_user_id = model_user.exchange_user_id, pan = model_user.pan)
        return {}

    def set_user(self, user_id : str, user : User):
        with self.session_scope() as db_session :
            model_user = models.User(exchange_id = user.exchange_id, exchange_user_id = user.exchange_user_id,
                pan = user.pan, itr_ack = user.itr_ack, exempt = user.exempt, binocs_id_val = user.binocs_id.id)
            db_session.add(model_user)

    def set_trade(self, trade_id : str, trade : UserTradeDetail) :
        with self.session_scope() as db_session :
            maker_user = db_session.query(models.User).filter(models.User.exchange_user_id == trade.maker.exchange_user_id).first()
            maker_tds_detail = models.UserTDSDetails(user = maker_user, trade_id = trade.trade_id,
                                timestamp = trade.timestamp, 
                                value = trade.maker_tds_details.tds_details.amount.value,
                                coin = trade.maker_tds_details.tds_details.amount.coin,
                                decimal = trade.maker_tds_details.tds_details.amount.decimal,
                                coin_type = trade.maker_tds_details.tds_details.amount.coin_type, 
                                fiat = trade.maker_tds_details.tds_details.fiat,
                                currency = trade.maker_tds_details.tds_details.currency,
                                challan = trade.maker_tds_details.tds_details.challan,
                                status = trade.maker_tds_details.tds_details.status)
            db_session.add(maker_tds_detail)

            taker_user = db_session.query(models.User).filter(models.User.exchange_user_id == trade.taker.exchange_user_id).first()
            taker_tds_detail = models.UserTDSDetails(user = taker_user, trade_id = trade.trade_id,
                                timestamp = trade.timestamp, 
                                value = trade.taker_tds_details.tds_details.amount.value,
                                coin = trade.taker_tds_details.tds_details.amount.coin,
                                decimal = trade.taker_tds_details.tds_details.amount.decimal,
                                coin_type = trade.taker_tds_details.tds_details.amount.coin_type, 
                                fiat = trade.taker_tds_details.tds_details.fiat,
                                currency = trade.taker_tds_details.tds_details.currency,
                                challan = trade.taker_tds_details.tds_details.challan,
                                status = trade.taker_tds_details.tds_details.status)
            db_session.add(taker_tds_detail)

            user_trade_detail = models.UserTradeDetail(exchange_id = trade.exchange_id,
                                trade_id = trade.trade_id, timestamp = trade.timestamp,
                                trade_type = trade.trade_type, maker = maker_user,
                                maker_value = trade.maker_amount.value,
                                maker_coin = trade.maker_amount.coin,
                                maker_decimal = trade.maker_amount.decimal,
                                maker_coin_type = trade.maker_amount.coin_type,
                                taker = taker_user,
                                taker_value = trade.taker_amount.value,
                                taker_coin = trade.taker_amount.coin,
                                taker_decimal = trade.taker_amount.decimal,
                                taker_coin_type = trade.taker_amount.coin_type,
                                txfee_value = trade.txfee_amount.value,
                                txfee_coin = trade.txfee_amount.coin,
                                txfee_decimal = trade.txfee_amount.decimal,
                                txfee_coin_type = trade.txfee_amount.coin_type,
                                gst_value = 0,
                                gst_coin = 'NA',
                                gst_decimal = 0,
                                gst_coin_type = 'NA',
                                maker_tds_details = maker_tds_detail, taker_tds_details = taker_tds_detail)

            db_session.add(user_trade_detail)

    def _paginate(self, query, page, per_page=20):
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = query.order_by(None).count()

        return total, items

    def get_tds_details(self, user_id : str, trade_id : str, page : int, limit : int):
        with self.session_scope() as db_session :
            db_session.expire_on_commit = False
            tds_details_query = None
            model_user = db_session.query(models.User).filter(models.User.exchange_user_id == user_id).first()
            if trade_id :
                tds_details_query = db_session.query(models.UserTDSDetails).filter(models.UserTDSDetails.user_id == model_user.id 
                                    and models.UserTDSDetails.trade_id == trade_id)
            else :
                tds_details_query = db_session.query(models.UserTDSDetails).filter(models.UserTDSDetails.user_id == model_user.id)

            return self._paginate(tds_details_query, page, limit)