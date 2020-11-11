from temperatures import data_colector
from temperatures import data_adjuster
import numpy as np
import pandas as pd
import seaborn as sns
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import datetime


#data_colector()
data,norma = data_adjuster()

class mainWindow(Frame):
    def __init__(self,master=None):


        Frame.__init__(self,master)
        self.label = Label(master,text = 'Graf namerana teplota vs. internetova teplota',font='Verdana 10 bold')
        self.label.place(x=10,y=10)
        self.window_setting()
        self.button()
        self.labels()
        self.frames()
    def window_setting(self):
        self.master.title("Weather station")                             # Nazov okna
        self.master.geometry("{}x{}".format(360, 220))                         # Rozmer okna
        self.pack(fill=BOTH, expand=1)                          # Zapisanie nastaveni

    def button(self):

        butt1 = Button(self, text="5 hodin!", command= self.create_figure1)
        butt1.place(x=20, y=40)
        butt2 = Button(self, text="10 hodin!", command= self.create_figure2)
        butt2.place(x=150, y=40)
        butt3 = Button(self, text="15 hodin!", command= self.create_figure3)
        butt3.place(x=280, y=40)
        butt4 = Button(self, text="Teplota vs. Predpovede (1-5 dni)", command=self.create_figure_real_for)
        butt4.place(x=80, y=80)

    def labels(self):
        self.label1 = Label(self, text='Predpoved o 1 den: ', font='Verdana 10 bold')
        self.label2 = Label(self, text='Predpoved o 2 den: ', font='Verdana 10 bold')
        self.label3 = Label(self, text='Predpoved o 3 den: ', font='Verdana 10 bold')
        self.label4 = Label(self, text='Predpoved o 4 den: ', font='Verdana 10 bold')


        self.label1.place(y=120, x=20)
        self.label2.place(y=140, x=20)
        self.label3.place(y=160, x=20)
        self.label4.place(y=180, x=20)


    def frames(self):
        text1 = data_plotter(norma,1,1).future_forecast()
        text2 = data_plotter(norma,2, 2).future_forecast()
        text3 = data_plotter(norma,2, 3).future_forecast()
        text4 = data_plotter(norma,2, 4).future_forecast()


        self.hodnota1 = Label(self, text=str(text1) + "\N{DEGREE SIGN}C", font='Verdana 10')
        self.hodnota2 = Label(self, text=str(text2) + "\N{DEGREE SIGN}C", font='Verdana 10')
        self.hodnota3 = Label(self, text=str(text3) + "\N{DEGREE SIGN}C", font='Verdana 10')
        self.hodnota4 = Label(self, text=str(text4) + "\N{DEGREE SIGN}C", font='Verdana 10')

        position_x = 200

        self.hodnota1.place(y=120, x=position_x)
        self.hodnota2.place(y=140, x=position_x)
        self.hodnota3.place(y=160, x=position_x)
        self.hodnota4.place(y=180, x=position_x)






    def create_figure1(self):
        self.figure1 = data_plotter(norma,5,5)
        self.figure1.plot_net_real()

    def create_figure2(self):
        self.figure1 = data_plotter(norma,10,10)
        self.figure1.plot_net_real()

    def create_figure3(self):
        self.figure1 = data_plotter(norma,20,20)
        self.figure1.plot_net_real()

    def create_figure_real_for(self):
        self.figure2 = data_plotter(norma,20,20)
        self.figure2.real_forecast()

class data_plotter():

    def __init__(self,norma,mod,forecast):
        self.n = norma
        self.mod = mod
        self.forecast = forecast
    def plot_net_real(self):
        current_time = datetime.datetime.now()
        wanted_time = current_time - datetime.timedelta(hours=self.mod)
        #g1df = self.d.filter(['Cas','Namerana teplota','Aktualna teplota'])
        g1df = self.n.reset_index()
        g1df = g1df[g1df['index'] > wanted_time]
        sns.set_theme()
        sns.lineplot(x='index',y='Namerana teplota',data=g1df)
        sns.lineplot(x='index',y='Aktualna teplota',data=g1df)
        plt.xlabel('Cas')
        plt.ylabel('Teplota C\N{DEGREE SIGN}')
        plt.show()

    def real_forecast(self):
        current_time = datetime.datetime.now()
        wanted_time = current_time - datetime.timedelta(hours=10)
        sns.set_theme()
        g2df = self.n

        g2df = g2df.drop(['Aktualna teplota'], axis=1)
        g2df = g2df.fillna(value=np.nan)
        g2df = g2df.loc[wanted_time:current_time]


        sns.set_theme()

        sns.lineplot(data=g2df)

        plt.xlabel('Cas')
        plt.ylabel('Teplota C\N{DEGREE SIGN}')
        plt.show()

    def future_forecast(self):

        time = datetime.datetime.now() + datetime.timedelta(days=self.forecast)
        time = time - datetime.timedelta(minutes=time.minute % 10,
                                     seconds=time.second,
                                     microseconds=time.microsecond)


        y_pozicia = str(self.forecast) + '_day_forecast'
        data = self.n.loc[time, [y_pozicia]].item()

        return data

root = Tk()
win = mainWindow(root)
root.mainloop()

#
#
# data = data_adjuster()
# figure = data_plotter(data)
#
# figure.plot_net_real()
