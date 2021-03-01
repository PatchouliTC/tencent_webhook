from datetime import datetime,timedelta,time

from app import scheduler
from fastapi_sqlalchemy import db
from app.models.db.models import NoticeReceiver
from utils import ConfigData

from utils.logger import get_logger

logger=get_logger(__name__)

class SendPlanScheduler(object):
    runningjobs=[]
    format = '%H:%M'
    executemethod=None

    def __init__(self,exemethod) -> None:
        super().__init__()
        self.executemethod=exemethod

    def initplans(self):
        if not self.executemethod:
            return False,"No method for plan running"
        #stop old job
        for job in self.runningjobs:
            job['instance'].remove()
        self.runningjobs.clear()

        with db():
            _receivers=db.session.query(NoticeReceiver).all()
            for receiver in _receivers:
                times=eval(receiver.stats_send_at)
                for t in times:
                    run_at=datetime.strptime(t,self.format).time()
                    _newjob=scheduler.add_job(self.executemethod,'cron',day_of_week='0-7',hour=run_at.hour,minute=run_at.minute,args=[receiver.id])
                    self.runningjobs.append({'name':f"{receiver.id}-{str(run_at)}","instance":_newjob})
        return True,"finish"

    def addplan(self,id:int,runtime:str):
        if not self.executemethod:
            return False,"No method for plan running"
        name=f"{id}-{str(runtime)}"
        run_at=datetime.strptime(runtime,self.format).time()
        #not check
        _newjob=scheduler.add_job(self.executemethod,'cron',day_of_week='0-6',hour=run_at.hour,minute=run_at.minute,args=[id])
        self.runningjobs.append({'name':name,"instance":_newjob})

