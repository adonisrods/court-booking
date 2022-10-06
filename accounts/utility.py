from datetime import datetime, timedelta
from datetime import date
def gen_previous_date(prev=date.today()): 
    previous_date = str(datetime.strptime(prev, '%Y-%m-%d') - timedelta(days = 1))
    previous_date_str=previous_date[0]+previous_date[1]+previous_date[2]+previous_date[3]+previous_date[5]+previous_date[6]+previous_date[8]+previous_date[9]
    return previous_date_str
def gen_next_date(next=date.today()):
    next_date=  str(datetime.strptime(next, '%Y-%m-%d') + timedelta(days = 1))
    next_date_str=next_date[0]+next_date[1]+next_date[2]+next_date[3]+next_date[5]+next_date[6]+next_date[8]+next_date[9]
    return next_date_str

def gen_today():
    today_date= str(date.today())
    today_date_str=today_date[0]+today_date[1]+today_date[2]+today_date[3]+today_date[5]+today_date[6]+today_date[8]+today_date[9]
    return today_date_str
