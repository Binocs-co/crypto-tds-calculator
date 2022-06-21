from typing import Any
from fastapi import FastAPI
from tds.calculator.controllers.tds import router as tds_router

class TDSApplication(FastAPI):
    def __init__(self, **extra: Any):
        super().__init__(**extra)
        self.register_router()
   
    def register_router(self):
        self.include_router(tds_router)
