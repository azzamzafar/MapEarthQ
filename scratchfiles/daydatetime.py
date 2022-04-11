
from datetime import date, datetime, timedelta

end = date.today()
print(end)
start = end-timedelta(7)
print(start)
newrow=[]
for i in range(10):
    newrow.append(i)
print(newrow)