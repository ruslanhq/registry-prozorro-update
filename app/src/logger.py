from app.prozorro_sale.models import Log
from app.src.database import sync_session
import traceback
import logging


class SQLAlchemyHandler(logging.Handler):

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']

        if exc:
            trace = traceback.format_exc()
        log = Log()
        log.logger = record.__dict__['name']
        log.level = record.__dict__['levelname']
        log.trace = trace
        log.msg = str(record.__dict__['msg'])

        session = sync_session()
        session.add(log)
        session.commit()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = SQLAlchemyHandler()

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
logger.addHandler(ch)
