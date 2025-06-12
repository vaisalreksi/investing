from scraper import CommodityScraper
from excel_handler import ExcelHandler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

def scrape_and_save():
    scraper = CommodityScraper()
    handler = ExcelHandler()
    
    data = scraper.get_data()
    if data:
        # Save to both files
        handler.save_all_data(data)
        handler.save_hourly_data(data)

def main():
    scheduler = BlockingScheduler()
    
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=12)
    
    scheduler.add_job(
        scrape_and_save,
        'interval',
        minutes=10,
        start_date=start_time,
        end_date=end_time
    )
    
    print(f"Starting scheduler at {start_time}")
    print(f"Will run for 12 hours until {end_time}")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('Scheduler stopped')

if __name__ == '__main__':
    main()