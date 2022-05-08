from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from typing import Optional, List
import datetime

from database import Base


class DbModbusDataTypes(Base):
    __tablename__ = "modbus_data_types"

    modbus_type_id = Column(Integer, primary_key=True)
    modbus_tcp_address = Column(String, unique=True, nullable=False)
    readable_name = Column(String, unique=True, nullable=False)
    description = Column(String)


class DbModbusData(Base):
    __tablename__ = "modbus_data"

    modbus_type_id = Column(Integer, ForeignKey("modbus_data_types.modbus_type_id"), primary_key=True)
    ins_date = Column(DateTime, primary_key=True)
    reale = Column(Boolean, nullable=False)
    value = Column(Float, nullable=False)
    merged = Column(Boolean, nullable=False)

    modbus_type = relationship("DbModbusDataTypes")


class DbModbusDataTmp(Base):
    __tablename__ = "modbus_data_temp"

    modbus_type_id = Column(Integer, ForeignKey("modbus_data_types.modbus_type_id"), primary_key=True)
    ins_date = Column(DateTime, primary_key=True)
    reale = Column(Boolean, nullable=False)
    value = Column(Float, nullable=False)

    modbus_type = relationship("DbModbusDataTypes")


class ModbusData(BaseModel):
    modbus_type_id: int
    ins_date: datetime.datetime
    value: float
    merged: bool
    reale: bool

    class Config:
        orm_mode = True


class ForecastDates(BaseModel):
    start_date: Optional[datetime.date] = None
    stop_date: Optional[datetime.date] = None
    