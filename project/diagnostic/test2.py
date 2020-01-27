from datetime import datetime
inputstring = '12.05.1900'
ew_date = datetime.strptime(inputstring, '%d.%m.%Y').strftime('%Y-%m-%d')
f = "АБРАМОВ АЛЕКСЕЙ НИКОЛАЕВИЧ (26.12.1991)"
date = '12.05.1900'

print(ew_date)