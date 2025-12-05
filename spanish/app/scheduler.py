import time
from datetime import datetime

from .config import SCHEDULED_TIMES
from .job import run_once


def run_scheduler_forever() -> None:
    """
    Run the main job at the configured times every day, in an infinite loop.
    This replaces the external cron schedule.
    """
    last_run_for_time = {t: None for t in SCHEDULED_TIMES}

    print("Starting internal scheduler loop...")
    print(
        "Scheduled times (HH:MM): "
        + ", ".join(f"{h:02d}:{m:02d}" for h, m in SCHEDULED_TIMES)
    )

    while True:
        now = datetime.now()
        today = now.date()
        current_hm = (now.hour, now.minute)

        for sched in SCHEDULED_TIMES:
            if current_hm == sched:
                last_run_date = last_run_for_time.get(sched)
                if last_run_date != today:
                    h, m = sched
                    print(f"Triggering run for scheduled time {h:02d}:{m:02d}")
                    try:
                        run_once()
                    except Exception as e:
                        print(
                            f"Error during scheduled run at {h:02d}:{m:02d}: {e}"
                        )
                    else:
                        last_run_for_time[sched] = today

        time.sleep(20)


