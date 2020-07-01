import requests
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mpl_dates
from datetime import datetime

states_codes = {
'AN': 'Andaman and Nicobar Islands',
'AP': 'Andhra Pradesh',
'AR': 'Arunachal Pradesh',
'AS': 'Assam',
'BR': 'Bihar',
'CH': 'Chandigarh',
'CT': 'Chhattisgarh',
'DD': 'Daman and Diu',
'DL': 'Delhi',
'DN': 'Dadra and Nagar Haveli',
'GA': 'Goa',
'GJ': 'Gujarat',
'HP': 'Himachal Pradesh',
'HR': 'Haryana',
'JH': 'Jharkhand',
'LA': 'Ladakh',
'KA': 'Karnataka',
'KL': 'Kerala',
'LD': 'Lakshadweep',
'MH': 'Maharashtra',
'ML': 'Meghalaya',
'MN': 'Manipur',
'MP': 'Madhya Pradesh',
'MZ': 'Mizoram',
'NL': 'Nagaland',
'OR': 'Odisha',
'PB': 'Punjab',
'PY': 'Puducherry',
'RJ': 'Rajasthan',
'SK': 'Sikkim',
'TG': 'Telangana',
'TN': 'Tamil Nadu',
'TR': 'Tripura',
'UP': 'Uttar Pradesh',
'UT': 'Uttarakhand',
'WB': 'West Bengal',
'JK': 'Jammu and Kashmir',
'TT': 'India'
}
date_format = mpl_dates.DateFormatter('%b %d')
plt.style.use('seaborn')
plt.figure(figsize=(50,30))
plt.rc('ytick', labelsize=10)
params = sys.argv

state_names = []

if len(params)==1:
    params.append('TT')
elif len(params)>11:
    print('Maximum 10 states can be entered')
    exit()
else:
    for i in range(1,len(params)):
        if params[i].upper() in states_codes:
            state_names.append(states_codes[params[i].upper()])
        else:
            print(params[i] + ' is not a valid state code')
            exit()
choice  = input('Display animation(Y/N) : ')
anim = True
if choice.upper()=='N':
    anim = False
elif choice.upper()=='Y':
    pass
else:
    print('Please enter a valid choice')
    exit()

choice = int(input('Enter 1 for daily increase in cases, and 2 for total cases: '))
if choice!=1 and choice!=2:
    print('Enter a valid input')
    exit()
r = requests.get('https://api.covid19india.org/states_daily.json')

data = r.json()
dates = []
nums = {}
for state in data['states_daily']:
    if state['status']=='Confirmed':
        dates.append(datetime.strptime(state['date'], '%d-%b-%y'))
        for i in range(1,len(params)):
            if params[i].lower() in nums:
                if choice==2:
                    nums[params[i].lower()].append(nums[params[i].lower()][-1] + int(state[params[i].lower()]))
                else:
                    nums[params[i].lower()].append(int(state[params[i].lower()]))
            else:
                nums[params[i].lower()] = [int(state[params[i].lower()])]
cur = 1
def animate(i):
    global cur
    if cur>len(dates):
        return
    plt.cla()
    for k,v in nums.items():
        plt.plot_date(dates[:cur], v[:cur], label=states_codes[k.upper()], linestyle='solid', marker=None)
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()
    cur+=1
    plt.legend()
    if choice==1:
        plt.title('Daily increase in cases since Mar 14')
    else:
        plt.title('Total cases')

if anim:
    ani = FuncAnimation(plt.gcf(), animate, interval=700)
else:
    if choice==1:
        plt.title('Daily increase in cases since Mar 14')
    else:
        plt.title('Total cases')
    for k,v in nums.items():
        print(v)
        plt.plot_date(dates, v, label=states_codes[k.upper()], linestyle='solid', marker=None)
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gcf().autofmt_xdate()
    plt.legend()
plt.show()
