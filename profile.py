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
    '''Takes created at component from database to create
    a heatmap(github style) in the profile page.'''
    today = datetime.utcnow().date()


    heatmap = {}


    
   
   