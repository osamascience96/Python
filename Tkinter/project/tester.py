import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *
from PIL import ImageTk
import pandas as pd
import os
import sys
import sqlite3
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from statistics import mean
from matplotlib import style

style.use('fivethirtyeight')


# define classes for each page

# Welcome Page


class Page0(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        tk.Label(self, text='SAS EAGLES', font='Times 24 bold', background="#2E2E2E", foreground='#EAEAEA').pack()
        self.logo = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/Eagle.png')
        tk.Label(self, image=self.logo, background='#2E2E2E').pack(fill='both', expand=1)
        self.config(background='#2E2E2E')

class Page3(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.config(background='#CDCDCD')
        self.canvas1 = None
        self.canvas2 = None

        # Graphing Function
        def get_info(e):

            # Variables for dynamic graphing
            global last_name
            last_name = n_entry.get()
            global c_metric
            c_metric = m_entry.get()
            ds = ds_entry.get()
            de = de_entry.get()
            populate()

            # Pull out info for selected athlete
            conn = sqlite3.connect('Wellness.db')
            c = conn.cursor()
            c.execute("""SELECT Name, Date, Sleep, Fatigue, Soreness, Stress, Mood, Diet, RPE, Duration
                                          FROM metrics INNER JOIN date ON metrics.date_id = date.date_id
                                          INNER JOIN athName ON metrics.athlete_id=athName.athlete_id 
                                          WHERE athName.Name == ? AND date.date >= ? AND date.date <= ?""",
                      (last_name, ds, de))

            # Variables for metrics
            global day, sleep, fatigue, soreness, stress, mood, diet, rpe
            day = []
            sleep = []
            fatigue = []
            soreness = []
            stress = []
            mood = []
            diet = []
            rpe = []

            # Adding metrics to variables
            for row in c.fetchall():
                day.append(row[1])
                sleep.append(row[2])
                fatigue.append(row[3])
                soreness.append(row[4])
                stress.append(row[5])
                mood.append(row[6])
                diet.append(row[7])
                rpe.append(row[8])



            # Averaging and normalizing variables for Radar Chart
            sle = (mean(sleep) - 3) / (10 - 3)
            fat = (mean(fatigue) - 0) / (5 - 0)
            sor = (mean(soreness) - 0) / (5 - 0)
            ste = (mean(stress) - 0) / (5 - 0)
            moo = (mean(mood) - 1) / (5 - 1)
            die = (mean(diet) - 1) / (5 - 1)
            rpe2 = (mean(rpe) - 6) / (20 - 6)

            # Pull out info for non-selected athletes
            conn.commit()
            c.execute("""SELECT Name, Date, Sleep, Fatigue, Soreness, Stress, Mood, Diet, RPE, Duration
                                                      FROM metrics INNER JOIN date ON metrics.date_id = date.date_id
                                                      INNER JOIN athName ON metrics.athlete_id=athName.athlete_id
                                                      WHERE athName.Name != ? AND date.date >= ? AND date.date <= ?""",
                      (last_name, ds, de))

            # Variables for non-selected athlete
            t_day = []
            t_sleep = []
            t_fatigue = []
            t_soreness = []
            t_stress = []
            t_mood = []
            t_diet = []
            t_rpe = []

            # Adding metrics to variables for non-selected athletes
            for row in c.fetchall():
                t_day.append(row[1])
                t_sleep.append(row[2])
                t_fatigue.append(row[3])
                t_soreness.append(row[4])
                t_stress.append(row[5])
                t_mood.append(row[6])
                t_diet.append(row[7])
                t_rpe.append(row[8])

            # Averaging and normalizing variables for Radar Chart non-selected athletes
            t_sle = (mean(t_sleep) - 3) / (10 - 3)
            t_fat = (mean(t_fatigue) - 0) / (5 - 0)
            t_sor = (mean(t_soreness) - 0) / (5 - 0)
            t_ste = (mean(t_stress) - 0) / (5 - 0)
            t_moo = (mean(t_mood) - 1) / (5 - 1)
            t_die = (mean(t_diet) - 1) / (5 - 1)
            t_rpe2 = (mean(t_rpe) - 6) / (20 - 6)

            # Pulling out info for non-selected athletes grouped by day for bar/line chart
            conn.commit()
            c.execute("""SELECT Date, Sleep, Fatigue, Soreness, Stress, Mood, Diet, RPE,
                        avg(Sleep), avg(Fatigue), avg(Soreness), avg(Stress), avg(Mood), avg(Diet), avg(RPE)      
                        FROM metrics INNER JOIN date ON metrics.date_id = date.date_id
                        INNER JOIN athName ON metrics.athlete_id=athName.athlete_id 
                        WHERE athName.Name != ? AND date.date >= ? AND date.date <= ?
                        GROUP BY metrics.date_id""", (last_name, ds, de))

            # Variables for averaging metrics by day for bar/line chart
            a_sleep = []
            a_fatigue = []
            a_soreness = []
            a_stress = []
            a_mood = []
            a_diet = []
            a_rpe = []

            # Adding day averaged to variables for non-selected athletes for bar/line chart
            for row in c.fetchall():
                a_sleep.append(row[8])
                a_fatigue.append(row[9])
                a_soreness.append(row[10])
                a_stress.append(row[11])
                a_mood.append(row[12])
                a_diet.append(row[13])
                a_rpe.append(row[14])

            # Variables for Radar Graph
            categories = ['Sleep', 'Fatigue', 'Soreness', 'Stress', 'Mood', 'Diet', 'RPE', 'Sleep']
            categories2 = ['Sleep', 'Fatigue', 'Soreness', 'Stress', 'Mood', 'Diet', 'RPE']
            lbls = [0., 0.8975979, 1.7951958, 2.6927937, 3.5903916, 4.48798951, 5.38558741]
            global graph
            graph = [sle, fat, sor, ste, moo, die, rpe2, sle]
            global others
            others = [t_sle, t_fat, t_sor, t_ste, t_moo, t_die, t_rpe2, t_sle]
            global t_metric
            t_metric = []
            global metric
            metric = []

            # Picking which metric is to be used based on user choice.
            # c = chosen, metric is for selected athlete, t = team averages
            if c_metric == 'Sleep':
                metric = sleep
                t_metric = a_sleep
            elif c_metric == 'Fatigue':
                metric = fatigue
                t_metric = a_fatigue
            elif c_metric == 'Soreness':
                metric = soreness
                t_metric = a_soreness
            elif c_metric == 'Stress':
                metric = stress
                t_metric = a_stress
            elif c_metric == 'Mood':
                metric = mood
                t_metric = a_mood
            elif c_metric == 'Diet':
                metric = diet
                t_metric = a_diet
            elif c_metric == 'RPE':
                metric = rpe
                t_metric = a_rpe

            generate()


            # Creating radar chart
            label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(categories))
            fig = plt.figure(figsize=(5, 4.5), dpi=39, facecolor='#2E2E2E')
            ax = plt.subplot(polar=True)
            plt.fill(label_loc, others, color='#D23C1E', alpha=.25)
            plt.plot(label_loc, others, label='Team', color='#D23C1E', linestyle='dashed', lw=3)
            plt.plot(label_loc, graph, label=last_name, color='#3769b9', lw=4)
            ax.set_yticklabels([])
            ax.set_ylim(0, max(graph) + .1)
            ax.set_facecolor('#2E2E2E')
            ax.spines['polar'].set_visible(False)
            plt.subplots_adjust(left=0.16, bottom=0.01, right=0.81, top=0.99)
            plt.thetagrids(np.degrees(lbls), categories2, size=13, color='white')
            for label, angle in zip(ax.get_xticklabels(), label_loc):
                if .1 < angle < 1:
                    label.set_horizontalalignment('left')
                    label.set_verticalalignment('bottom')
                elif 1.1 < angle < 2:
                    label.set_horizontalalignment('right')
                    label.set_verticalalignment('bottom')
                elif 2.1 < angle < 3:
                    label.set_horizontalalignment('right')
                    label.set_verticalalignment('bottom')
                elif 3.1 < angle < 4:
                    label.set_horizontalalignment('right')
                    label.set_verticalalignment('top')
                elif 4.1 < angle < 5:
                    label.set_horizontalalignment('right')
                    label.set_verticalalignment('top')
                elif 4.1 < angle < 5:
                    label.set_horizontalalignment('right')
                    label.set_verticalalignment('top')
                elif 4.1 < angle < 5:
                    label.set_horizontalalignment('left')
                    label.set_verticalalignment('top')
                else:
                    label.set_horizontalalignment('left')
                    label.set_verticalalignment('top')
                fig.cla()

            # Display radar chart
            canvas2 = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas2.get_tk_widget().grid(row=1, column=4, padx=0, pady=(100, 0), rowspan=6, sticky=N)
            canvas2.draw()

            # creating bar/line chart
            fig1 = plt.figure(figsize=(4, .5), dpi=45, facecolor='#2E2E2E')
            ax = plt.subplot()
            plt.plot(day, t_metric, color='#D23C1E', linewidth=1.5)
            plt.fill_between(day, t_metric, color='#D23C1E', alpha=.25)
            plt.bar(day, metric, color='#3769b9')
            ax.set_ylim(0, max(metric))
            plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99)
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#CDCDCD')
            ax.spines['left'].set_visible(False)
            plt.grid(visible=FALSE, axis='x')
            ax.set_facecolor('#2E2E2E')

            # Display bar/line graph
            canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
            canvas1.get_tk_widget().grid(row=0, rowspan=2, column=4, padx=10, pady=(30, 5), sticky=N)
            canvas1.draw()

        # Variables for dropdown boxes
        dates = []
        names = []
        sport = ['Sport']
        year = ['Year']
        categories2 = ['Sleep', 'Fatigue', 'Soreness', 'Stress', 'Mood', 'Diet', 'RPE']

        # Pull out dates for dates dropdowns
        try:
            conn = sqlite3.connect('Wellness.db')
            c = conn.cursor()
            c.execute("""SELECT Date FROM date""")
            conn.commit()

            for row in c.fetchall():
                dates.append(row[0])

            # Pull out names for namedrop downs
            c.execute("""SELECT Name FROM athName""")
            conn.commit()
            for row in c.fetchall():
                names.append(row[0])

        except:
            print("No Database")

        # Top frame in screen with dropdown boxes
        button_frame = LabelFrame(self, background='#3769B9', bd=0, height='150')
        button_frame.grid_propagate(False)
        button_frame.pack(fill='x', anchor='n')

        # Name label and drop down box
        n_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Athlete.png')
        n_imagelab = Label(button_frame, image=n_image, background='#3769B9')
        n_imagelab.grid(row=0, column=1, padx=(0, 0), rowspan=3, sticky=NW)
        n_imagelab.image = n_image
        n_entry = ttk.Combobox(button_frame, values=names, font=('none', 50), width=12, foreground='white',
                               justify='center')
        n_entry.set('Name')
        n_entry.bind('<<ComboboxSelected>>', get_info)
        n_entry.grid(row=0, column=2, rowspan=3, columnspan=3, pady=(15, 0), sticky=NE)

        sp_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Baseball.png')
        sp_imagelab = Label(button_frame, image=sp_image, background='#3769B9')
        sp_imagelab.grid(row=1, column=0, pady=(20, 0), padx=(240, 0))
        sp_imagelab.image = sp_image
        sp_entry = ttk.Combobox(button_frame, values=sport, font=('none', 35), width=7, foreground='white',
                               justify='center')
        sp_entry.current(0)
        sp_entry.grid(row=1, column=1, columnspan=2, pady=(40, 0), sticky=W)

        y_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Year.png')
        y_imagelab = Label(button_frame, image=y_image, background='#3769B9')
        y_imagelab.grid(row=1, column=3, pady=(35, 0), padx=(0, 0))
        y_imagelab.image = y_image
        y_entry = ttk.Combobox(button_frame, values=year, font=('none', 35), width=7, foreground='white',
                               justify='center')
        y_entry.current(0)
        # y_entry.bind('<<ComboboxSelected>>', get_info)
        y_entry.grid(row=1, column=4, columnspan=2, pady=(40, 0), sticky=W)

        # Date start label and drop down
        da_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Dates.png')
        da_imagelab = Label(button_frame, image=da_image, background='#3769B9')
        da_imagelab.grid(row=0, column=6, rowspan=2, pady=(0, 0), padx=(0, 0), sticky=N)
        da_imagelab.image = da_image
        ds_label = Label(button_frame, text="Start Date", background='#3769B9')
        ds_label.grid(row=0, column=7, pady=(15, 0), sticky=N)
        ds_entry = ttk.Combobox(button_frame, values=dates, font=('none', 20), width=10, foreground='white',
                                justify='center')
        ds_entry.set('Select')
        ds_entry.bind('<<ComboboxSelected>>', get_info)
        ds_entry.grid(row=0, column=8, pady=(15, 0), sticky=N)

        # Date end label and drop down
        de_label = Label(button_frame, text="End Date", background='#3769B9')
        de_label.grid(row=1, column=7, pady=(10, 0), sticky=N)
        de_entry = ttk.Combobox(button_frame, values=dates, font=('none', 20), width=10, foreground='white',
                                justify='center')
        de_entry.set('Select')
        de_entry.bind('<<ComboboxSelected>>', get_info)
        de_entry.grid(row=1, column=8, pady=(10, 0), sticky=N)

        # Metric label and drop down box
        m_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Search.png')
        m_imagelab = Label(button_frame, image=m_image, background='#3769B9')
        m_imagelab.grid(row=1, column=6, padx=(10, 0), pady=(20, 0))
        m_imagelab.image = m_image
        # m_label = Label(button_frame, text="Metric", background='#3769B9')
        # m_label.grid(row=1, column=1, padx=10, pady=10)
        m_entry = ttk.Combobox(button_frame, values=categories2, font=('none', 35), width=9, foreground='white',
                               justify='center')
        m_entry.set('Metric')
        m_entry.bind('<<ComboboxSelected>>', get_info)
        m_entry.grid(row=1, column=7, columnspan=2, pady=(40, 0))

        # Bottom frame in screen for graphs and metric scores
        graph_frame = LabelFrame(self, background='#2E2E2E', bd=0, height=100)
        graph_frame.pack(fill='x', anchor='n')

        # # Averages Label on top of all metrics for athlete
        # avm_label = Label(graph_frame, text='Averages', pady=10, font=(None, 40), foreground='white', background='#2E2E2E', justify=RIGHT)
        # avm_label.grid(row=0, column=0, padx=(0, 200), columnspan=6)

        # Sleep metric frame
        slm_frame = LabelFrame(graph_frame, text='Sleep', labelanchor='sw', fg='#8B8D8E', width=225, height=100,
                               background='#2E2E2E')
        slm_frame.grid(row=1, column=0, pady=(50, 5), padx=2.5)
        slm_frame.grid_propagate(False)
        # Sleep Metric Frame icon
        slmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Sleep.png')
        slmf_imagelab = Label(slm_frame, image=slmf_image, background='#2E2E2E')
        slmf_imagelab.grid(row=0, column=0, padx=10)
        slmf_imagelab.image = slmf_image
        slmf_data = Label(slm_frame, text='0.00', font=('none', 45), fg='white', background='#2E2E2E')
        slmf_data.grid(row=0, column=1, padx=10)

        # Fatigue metric frame
        fm_frame = LabelFrame(graph_frame, text='Fatigue', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                              background='#2E2E2E')
        fm_frame.grid(row=2, column=0, pady=5, padx=2.5)
        fm_frame.grid_propagate(False)
        # Fatigue Metric Frame icon
        fmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Fatigue.png')
        fmf_imagelab = Label(fm_frame, image=fmf_image, background='#2E2E2E')
        fmf_imagelab.grid(row=0, column=0, padx=10)
        fmf_imagelab.image = fmf_image
        fmf_data = Label(fm_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        fmf_data.grid(row=0, column=1, padx=10)

        # Stress metric frame
        stm_frame = LabelFrame(graph_frame, text='Stress', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                               background='#2E2E2E')
        stm_frame.grid(row=3, column=0, pady=5, padx=2.5)
        stm_frame.grid_propagate(False)
        # Stress Metric Frame icon
        stmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Stress.png')
        stmf_imagelab = Label(stm_frame, image=stmf_image, background='#2E2E2E')
        stmf_imagelab.grid(row=0, column=0, padx=17.5, pady=7.5)
        stmf_imagelab.image = stmf_image
        stmf_data = Label(stm_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        stmf_data.grid(row=0, column=1, padx=14, pady=7.5)

        # Soreness metric frame
        som_frame = LabelFrame(graph_frame, text='Soreness', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                               background='#2E2E2E')
        som_frame.grid(row=1, column=1, pady=(50, 5), padx=2.5)
        som_frame.grid_propagate(False)
        # Soreness Metric Frame icon
        somf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Soreness.png')
        somf_imagelab = Label(som_frame, image=somf_image, background='#2E2E2E')
        somf_imagelab.grid(row=0, column=0, padx=17.5, pady=7.5)
        somf_imagelab.image = somf_image
        somf_data = Label(som_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        somf_data.grid(row=0, column=1, padx=14, pady=7.5)

        # Mood metric frame
        mm_frame = LabelFrame(graph_frame, text='Mood', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                              background='#2E2E2E')
        mm_frame.grid(row=2, column=1, pady=5, padx=2.5)
        mm_frame.grid_propagate(False)
        # Mood Metric Frame icon
        mmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Mood.png')
        mmf_imagelab = Label(mm_frame, image=mmf_image, background='#2E2E2E')
        mmf_imagelab.grid(row=0, column=0, padx=17.5, pady=7.5)
        mmf_imagelab.image = mmf_image
        mmf_data = Label(mm_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        mmf_data.grid(row=0, column=1, padx=14, pady=7.5)

        # Diet metric frame
        dm_frame = LabelFrame(graph_frame, text='Diet', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                              background='#2E2E2E')
        dm_frame.grid(row=3, column=1, pady=5, padx=2.5)
        dm_frame.grid_propagate(False)
        # Diet Metric Frame icon
        dmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Diet.png')
        dmf_imagelab = Label(dm_frame, image=dmf_image, background='#2E2E2E')
        dmf_imagelab.grid(row=0, column=0, padx=10)
        dmf_imagelab.image = dmf_image
        dmf_data = Label(dm_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        dmf_data.grid(row=0, column=1, padx=0)

        # RPE metric frame
        rpem_frame = LabelFrame(graph_frame, text='RPE', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                                background='#2E2E2E')
        rpem_frame.grid(row=1, column=2, pady=(50, 5), padx=(2.5, 0))
        rpem_frame.grid_propagate(False)
        # Sleep Metric Frame icon
        rpemf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/RPE.png')
        rpemf_imagelab = Label(rpem_frame, image=rpemf_image, background='#2E2E2E')
        rpemf_imagelab.grid(row=0, column=0, padx=(10, 0))
        rpemf_imagelab.image = rpemf_image
        rpemf_data = Label(rpem_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        rpemf_data.grid(row=0, column=1, padx=4)

        # Load metric frame
        lm_frame = LabelFrame(graph_frame, text='Load', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                              background='#2E2E2E')
        lm_frame.grid(row=2, column=2, pady=5, padx=(2.5, 0))
        lm_frame.grid_propagate(False)
        # Load Metric Frame icon
        lmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/Load.png')
        lmf_imagelab = Label(lm_frame, image=lmf_image, background='#2E2E2E')
        lmf_imagelab.grid(row=0, column=0, padx=(10, 0))
        lmf_imagelab.image = lmf_image
        lmf_data = Label(lm_frame, text='0000', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        lmf_data.grid(row=0, column=1, padx=4)

        # AC metric frame
        acm_frame = LabelFrame(graph_frame, text='A:C Ratio', labelanchor='sw', fg='#CDCDCD', width=225, height=100,
                               background='#2E2E2E')
        acm_frame.grid(row=3, column=2, pady=5, padx=(2.5, 0))
        acm_frame.grid_propagate(False)
        # AC Metric Frame icon
        acmf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/medium/AC.png')
        acmf_imagelab = Label(acm_frame, image=acmf_image, background='#2E2E2E')
        acmf_imagelab.grid(row=0, column=0, padx=(10, 0))
        acmf_imagelab.image = acmf_image
        acmf_data = Label(acm_frame, text='0.00', font=('none', 45), fg='#CDCDCD', background='#2E2E2E')
        acmf_data.grid(row=0, column=1, padx=10)

        # school logo frame
        brand_frame = LabelFrame(self, width=250, height=100, bd=0, background='#CDCDCD')
        brand_frame.pack(fill='x', anchor='s')
        br_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/SASLong.png')
        br_imagelab = Label(brand_frame, image=br_image, background='#CDCDCD')
        br_imagelab.pack(pady=13, anchor=CENTER)
        br_imagelab.image = br_image

        # Creating bar/line chart
        day = [0]
        t_metric = [0]
        metric = [0]
        others = [0, 0, 0, 0, 0, 0, 0, 0]
        graph = [0, 0, 0, 0, 0, 0, 0, 0]
        categories = ['Sleep', 'Fatigue', 'Soreness', 'Stress', 'Mood', 'Diet', 'RPE', 'Sleep']
        categories2 = ['Sleep', 'Fatigue', 'Soreness', 'Stress', 'Mood', 'Diet', 'RPE']
        lbls = [0., 0.8975979, 1.7951958, 2.6927937, 3.5903916, 4.48798951, 5.38558741]

        fig1 = plt.figure(figsize=(4, .5), dpi=45, facecolor='#2E2E2E')
        ax = plt.subplot()
        ax.set_ylim(0, .5)
        plt.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#CDCDCD')
        ax.spines['left'].set_visible(False)
        plt.grid(visible=FALSE, axis='x')
        ax.set_facecolor('#2E2E2E')

        # Creating radar chart
        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(categories))
        fig = plt.figure(figsize=(5, 4.5), dpi=39, facecolor='#2E2E2E')
        ax = plt.subplot(polar=True)
        ax.set_yticklabels([])
        ax.set_ylim(0, 1)
        ax.set_facecolor('#2E2E2E')
        ax.spines['polar'].set_visible(False)
        plt.subplots_adjust(left=0.16, bottom=0.01, right=0.81, top=0.99)
        plt.thetagrids(np.degrees(lbls), categories2, size=13, color='white')
        for label, angle in zip(ax.get_xticklabels(), label_loc):
            if .1 < angle < 1:
                label.set_horizontalalignment('left')
                label.set_verticalalignment('bottom')
            elif 1.1 < angle < 2:
                label.set_horizontalalignment('right')
                label.set_verticalalignment('bottom')
            elif 2.1 < angle < 3:
                label.set_horizontalalignment('right')
                label.set_verticalalignment('bottom')
            elif 3.1 < angle < 4:
                label.set_horizontalalignment('right')
                label.set_verticalalignment('top')
            elif 4.1 < angle < 5:
                label.set_horizontalalignment('right')
                label.set_verticalalignment('top')
            elif 4.1 < angle < 5:
                label.set_horizontalalignment('right')
                label.set_verticalalignment('top')
            elif 4.1 < angle < 5:
                label.set_horizontalalignment('left')
                label.set_verticalalignment('top')
            else:
                label.set_horizontalalignment('left')
                label.set_verticalalignment('top')

            canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
            canvas1.get_tk_widget().grid(row=0, rowspan=2, column=4, padx=10, pady=(30, 5), sticky=N)
            canvas1.draw()

            # Display radar chart
            canvas2 = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas2.get_tk_widget().grid(row=1, column=4, padx=0, pady=(100, 0), rowspan=6, sticky=N)
            canvas2.draw()

        pic_frame = LabelFrame(self, height=200, width=250, background='#D23C1E')
        pic_frame.place(x=0, y=0)
        pic_frame.grid_propagate(False)
        pf_image = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/SASPD.png')
        pf_imagelab = Label(pic_frame, image=pf_image, background='#D23C1E')
        pf_imagelab.grid(row=0, column=0, padx=20)
        pf_imagelab.image = pf_image

        def populate():
            c.execute("""SELECT Sport FROM athName WHERE athName.Name == ?""", (last_name,))
            conn.commit()
            for row in c.fetchall():
                sport[0] = row[0]
                sp_entry['values'] = row[0]
                sp_entry.current(0)
            c.execute("""SELECT Year FROM athName WHERE athName.Name == ?""", (last_name,))
            conn.commit()
            for row in c.fetchall():
                year[0] = row[0]
                y_entry['values'] = row[0]
                y_entry.current(0)

        def generate():
            slmf_data['text'] = "%.2f" % round(mean(sleep), 2)
            fmf_data['text'] = "%.2f" % round(mean(fatigue), 2)
            somf_data['text'] = "%.2f" % round(mean(soreness), 2)
            stmf_data['text'] = "%.2f" % round(mean(stress), 2)
            mmf_data['text'] = "%.2f" % round(mean(mood), 2)
            dmf_data['text'] = "%.2f" % round(mean(diet), 2)
            rpemf_data['text'] = "%.2f" % round(mean(rpe), 2)

root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width, height))
root.configure(background='white')
root.title("Wellness Tracker")

# Style the screen
style = ttk.Style()
style.theme_use('clam')
root.option_add('*TCombobox*Listbox*Background', '#CDCDCD')
root.option_add('*TCombobox*Listbox*Foreground', '#2E2E2E')
root.option_add('*TCombobox*Listbox*selectBackground', '#2E2E2E')
root.option_add('*TCombobox*Listbox*selectForeground', '#CDCDCD')
style.configure('TCombobox', fieldbackground='#3769B9', background='#CDCDCD', bordercolor='#3769B9',
                selectforeground='white', selectbackground='#3769B9')
style.map('TCombobox', focuscolor=[('focus', 'red')])
style.configure('TNotebook', tabposition='wn', background='#EAEAEA', tabmargins=0, borderwidth=0, relief='flat',
                bordercolor="#EAEAEA")

# configure tab with white background initially
style.configure('TNotebook.Tab', background='#EAEAEA', width=10, borderwidth=0, relief='flat', bordercolor="#EAEAEA",
                padding=(0, 75))
style.map('TNotebook.Tab', bordercolor=[('selected', '#CDCDCD')], background=[('selected', 'gray')],
          padding=[('selected', (0, 75))])

nb = ttk.Notebook(root, height=700, width=1100)
nb.pack(padx=(50, 0), pady=(40, 5), side=LEFT)
logo_frame2 = Frame(root, height=700, width=125, background='#EAEAEA')
logo_frame2.pack(pady=(40, 5), side=LEFT)
logo_frame2.pack_propagate(False)
eag = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/MedEagle.png')
eaglabel = Label(logo_frame2, image=eag, background='#EAEAEA')
eaglabel.pack(pady=(260, 0))
eaglabel.image = eag


# page0 = Page0(nb)
page3 = Page3(nb)

ath = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Athlete.png')
dat = ImageTk.PhotoImage(file=f'{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "photos")}/dark/Data.png')

# nb.add(page0, text= 'Home Page', compound='center')
nb.add(page3, image=ath, compound="center")

root.mainloop()
