from celery.task import task
from celery.utils.log import get_task_logger

from profiles.services import send_activation_email

logger = get_task_logger(__name__)


@task(name="send_activation_email_task")
def send_activation_email_task(user_id, current_site, token):
    logger.info("Sent feedback email")
    return send_activation_email(user_id, current_site, token)
