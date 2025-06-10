from apscheduler.schedulers.background import BackgroundScheduler
from routes.ads_routes import check_due_payments

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_due_payments, 'interval', days=1)  # Corre cada día
    scheduler.start()
