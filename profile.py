'''
profile data helpers - compute the heatma and stats for a user

Only data. The route in flask_app compute_heatmap() hamds the results to
the template.
'''



from datetime import datetime

import calendar
from collections import Counter
from datetime import date, datetime, timedelta

from models import LessonProgress

def calculate_heatmap(user_id:int, slug: str, weekss=4):
    """Build a one-month heatmap of challenge completions for a user.

    Every day in the requested calendar month becomes a cell. A cell is
    "done" if the user passed at least one challenge that day; otherwise
    it's empty. Cells before the 1st and after the last day of the month
    are returned as `placeholder` cells so the grid stays a clean
    rectangle of 7-column rows.

    Defaults to the current UTC year/month if `year` / `month` aren't given.

    Returns:
        {
            "year": int,
            "month": int,                  # 1-12
            "label": "June 2026",
            "weeks": [[cell, cell, ...]],  # length-7 rows, Sun..Sat
            "stats": {
                "total_completions": int,
                "active_days": int,
                "current_streak": int,     # 0 unless viewing the current month
                "longest_streak": int,
            },
        }

    Where each cell is one of:
        {"placeholder": True}                          # blank slot
        {"date": date, "count": int, "done": bool}     # real day
    """

    #1 reasolve requested month, defaulting to UTC for now
    today = datetime.utcnow().date()
    if year is None or month is None:
        year, month = today.year, today.month    


    heatmap = {}


    
   
   