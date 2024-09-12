from notification_manager import NotificationManager
from web_scaper import search_jobs
import os

main_link = os.getenv('MLINK')
search_link = os.getenv('SLINK')
keywords = ["keyword", "list"]

notification_manager = NotificationManager()


job_list = search_jobs(main_link, search_link)
filtered_job_list = [
    job for job in job_list
    if all(keyword.lower() in job['title'].lower() for keyword in keywords)
]
print(filtered_job_list)
if filtered_job_list:
    message = "There is new opening with expected keywords. "

    for job in filtered_job_list:
        message += f"Title: {job['title']}. Link to offer: {job['link']}. "

    notification_manager.send_alert(message)
