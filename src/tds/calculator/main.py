from tds.calculator.common.application import TDSApplication
import uvicorn
from tds.calculator.common.configuration import config

app = TDSApplication()

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.SERVER_HOST, port=config.SERVER_PORT, reload=True)