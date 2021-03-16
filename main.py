import plyer
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import Tk, Label, Button, Entry, messagebox, filedialog, StringVar, RIDGE


def scrap():
    def notifyme(title, message):
        plyer.notification.notify(
            title=title,
            message=message,
            app_icon='covid.ico',
            timeout=50
        )

    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tablebody = soup.find('tbody')
    data = tablebody.find_all('tr')
    notifycountry = countrydata.get()
    if notifycountry == '':
        notifycountry = 'india'
    countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases = [
    ], [], [], [], [], [], []
    serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion, population = [], [], [], [], [], []
    headers = ['countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
               'serious', 'totalcases_permillion', 'totaldeaths_permillion', 'totaltests', 'totaltests_permillion',
               'population']

    for i in data:
        id = i.find_all('td')
        if id[1].text.strip().lower() == notifycountry.lower():
            totalcases1 = int(id[2].text.strip().replace(',', ''))
            totaldeaths1 = id[4].text.strip()
            newcases1 = id[3].text.strip()
            newdeaths1 = id[5].text.strip()
            notifyme(f'Corona Virus Stats In {notifycountry}',
                     f'Total Cases : {totalcases1}\nTotal Deaths : {totaldeaths1}\nNew Cases : {newcases1}\nNew Deaths : {newdeaths1}')
        countries.append(id[1].text.strip())
        total_cases.append(int(id[2].text.strip().replace(',', '')))
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[8].text.strip())
        serious.append(id[9].text.strip())
        totalcases_permillion.append(id[10].text.strip())
        totaldeaths_permillion.append(id[11].text.strip())
        totaltests.append(id[12].text.strip())
        totaltests_permillion.append(id[13].text.strip())
        population.append(id[14].text.strip())
    df = pd.DataFrame(
        list(zip(countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious,
                 totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion, population)),
        columns=headers)
    sor = df.sort_values('total_cases', ascending=False)
    for k in formatlist:
        if k == 'html':
            path2 = '{}/alldata.html'.format(path)
            sor.to_html(r'{}'.format(path2))
        if k == 'json':
            path2 = '{}/alldata.json'.format(path)
            sor.to_json(r'{}'.format(path2))
        if k == 'csv':
            path2 = '{}/alldata.csv'.format(path)
            sor.to_csv(r'{}'.format(path2))
    if len(formatlist) != 0:
        messagebox.showinfo(
            "Notification", f'Corona Record Is saved {path2}', parent=root)


def download():
    global path
    if len(formatlist) != 0:
        path = filedialog.askdirectory()
    else:
        pass
    scrap()
    formatlist.clear()
    InHtml.configure(state='normal')
    InJson.configure(state='normal')
    InCsv.configure(state='normal')


def inhtml():
    formatlist.append('html')
    InHtml.configure(state='disabled')


def incsv():
    formatlist.append('csv')
    InCsv.configure(state='disabled')


def injson():
    formatlist.append('json')
    InJson.configure(state='disabled')


root = Tk()
root.title('Corona Virus Info ')
root.geometry('530x300+200+80')
root.configure(bg='LightGrey')
root.iconbitmap('covid.ico')
root.resizable(0, 0)
formatlist = []
path = ''

IntroLabel = Label(root, text='COVID-19 Info', font=('Bahnschrift SemiLight', 25, 'roman bold'), bg='MediumTurquoise',
                   width=28, justify='center')
IntroLabel.place(x=0, y=0)
EntryLabel = Label(root, text='Enter Country : ', font=(
    'Bahnschrift SemiLight', 20, 'roman bold'), bg='LightGrey')
EntryLabel.place(x=10, y=70)
FormatLabel = Label(root, text='Download In : ', font=(
    'Bahnschrift SemiLight', 20, 'roman bold'), bg='LightGrey')
FormatLabel.place(x=10, y=150)

countrydata = StringVar()
ent1 = Entry(root, textvariable=countrydata, font=('Bahnschrift SemiLight', 20, 'roman bold'), relief=RIDGE, bd=2, bg='Lavender',
             width=20)
ent1.place(x=220, y=70)

InHtml = Button(root, text='HTML', bg='LightSteelBlue', font=('Bahnschrift SemiLight', 15, 'roman bold'), relief=RIDGE,
                activebackground='SteelBlue', activeforeground='white',
                bd=5, width=5, command=inhtml)
InHtml.place(x=210, y=150)

InJson = Button(root, text='JSON', bg='LightSteelBlue', font=('Bahnschrift SemiLight', 15, 'roman bold'), relief=RIDGE,
                activebackground='SteelBlue', activeforeground='white',
                bd=5, width=5, command=injson)
InJson.place(x=320, y=150)

InCsv = Button(root, text='CSV', bg='LightSteelBlue', font=('Bahnschrift SemiLight', 15, 'roman bold'), relief=RIDGE,
               activebackground='SteelBlue', activeforeground='white',
               bd=5, width=5, command=incsv)
InCsv.place(x=430, y=150)

Submit = Button(root, text='Submit', bg='CadetBlue', font=('Bahnschrift SemiLight', 15, 'roman bold'), relief=RIDGE,
                activebackground='DarkCyan', activeforeground='white',
                bd=5, width=25, command=download)
Submit.place(x=110, y=250)
root.mainloop()
