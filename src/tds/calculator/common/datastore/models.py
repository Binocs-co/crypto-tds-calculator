from contextlib import nullcontext
import datetime
import json
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import composite, relationship
from sqlalchemy.sql import func

from tds.calculator.common.datastore.composites import BinocsId, TDSDetails, Amount

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    exchange_id = Column(String(16), nullable=False)
    exchange_user_id = Column(String(32), nullable=False)
    pan = Column(String(16), nullable=False)
    itr_ack = Column(Boolean, default=False)
    exempt = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now)
    binocs_id_val = Column(String(64), nullable=False)
    binocs_id = composite(BinocsId, binocs_id_val)
    exchange_user_uniq = UniqueConstraint(exchange_user_id, exchange_id)

class UserTradeDetail(Base):
    __tablename__ = 'user_trade_detail'

    id = Column(Integer, primary_key=True)
    exchange_id = Column(String(16), nullable=False)
    trade_id = Column(String(64), nullable=False)
    timestamp = Column(Integer, nullable=False)
    trade_type = Column(String(16), nullable=False)
    maker_id = Column(Integer, ForeignKey("user.id"))
    maker = relationship("User", foreign_keys=[maker_id])
    maker_value = Column(Integer)
    maker_coin = Column(String(8))
    maker_decimal = Column(Integer)
    maker_coin_type = Column(String(8))
    maker_amount = composite(Amount, maker_value, maker_coin, maker_decimal, maker_coin_type)
    taker_id = Column(Integer, ForeignKey("user.id"))
    taker = relationship("User", foreign_keys=[taker_id])
    taker_value = Column(Integer)
    taker_coin = Column(String(8))
    taker_decimal = Column(Integer)
    taker_coin_type = Column(String(8))
    taker_amount = composite(Amount, taker_value, taker_coin, taker_decimal, taker_coin_type)
    txfee_value = Column(Integer, nullable=True)
    txfee_coin = Column(String(8), nullable=True)
    txfee_decimal = Column(Integer, nullable=True)
    txfee_coin_type = Column(String(8), nullable=True)
    txfee_amount = composite(Amount, txfee_value, txfee_coin, txfee_decimal, txfee_coin_type)
    gst_value = Column(Integer, nullable=True)
    gst_coin = Column(String(8), nullable=True)
    gst_decimal = Column(Integer, nullable=True)
    gst_coin_type = Column(String(8), nullable=True)
    gst_amount = composite(Amount, gst_value, gst_coin, gst_decimal, gst_coin_type)
    create_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now)
    maker_tds_details_id = Column(Integer, ForeignKey("user_tds_details.id"))
    maker_tds_details = relationship("UserTDSDetails", foreign_keys=[maker_tds_details_id])
    taker_tds_details_id = Column(Integer, ForeignKey("user_tds_details.id"))
    taker_tds_details = relationship("UserTDSDetails", foreign_keys=[taker_tds_details_id])
    exchange_trade_uniq = UniqueConstraint(trade_id, exchange_id)

class UserTDSDetails(Base):
    __tablename__ = 'user_tds_details'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id])
    trade_id = Column(String(64), nullable=False)
    timestamp = Column(Integer, nullable=False)
    value = Column(Integer)
    coin = Column(String(8))
    decimal = Column(Integer)
    coin_type = Column(String(8))
    fiat = Column(Float, default=0, nullable=True)
    currency  = Column(String(8), nullable=True)
    challan = Column(String(16), nullable=True)
    status = Column(String(16), nullable=True)
    tds_details = composite(TDSDetails._generate, value, coin, decimal, coin_type, fiat, currency, challan, status)
    create_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now)