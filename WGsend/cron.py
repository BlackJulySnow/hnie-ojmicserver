from apscheduler.schedulers.blocking import BlockingScheduler
from run import sendNoneDo


print("启动成功")
scheduler = BlockingScheduler()
scheduler.add_job(sendNoneDo, 'cron', day_of_week="mon,tue,wed,thu,sun", hour=22, minute=30, second=0, args=[])
scheduler.start()
