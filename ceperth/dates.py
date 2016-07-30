from datetime import datetime, date, time, timedelta
from calendar import month_name

today = date.today()
curmonthstart =  today.replace(day=1)
curmonth = curmonthstart.month
        
def this_monthstart():
    return curmonthstart
    
def last_monthstart():
    lastmonth = curmonth -1
    return curmonthstart.replace(month=lastmonth)
    
def last_twomonthstart():
    lasttwomonth = curmonth -2
    lasttwomonthstart = curmonthstart.replace(month= lasttwomonth)
    return lasttwomonthstart
    
thismonth = month_name[this_monthstart().month]

lastmonth = month_name[last_monthstart().month]

lasttwomonth = month_name[last_twomonthstart().month]