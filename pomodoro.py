import time
import threading
import tkinter as tk
from tkinter import ttk , PhotoImage
from tkinter import * 

class PomodoroClock:

    def __init__(self):
        self.root = tk.Tk()  #creo la ventana
        self.root.geometry('600x300') #Defino el tamaño de la ventana
        self.root.title('Cronometro Pomodoro para la PRODUCTIVIDAD') #Titulo
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='Tomate_logo.png')) #Pone el logo

        #configuracion letras y botones
        self.s = ttk.Style()
        self.s.configure('TNotebook.Tab', font=('Segoe UI', 14))
        self.s.configure('TButton', font=('Segoe UI', 14))

        #configuracion de ventanas
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', pady=10, expand=True)

        #Crea las 3 ventanas dentro de la ventana mayor
        self.tab1 = ttk.Frame(self.tabs, width = 600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width = 600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width = 600, height=100)

        #Tiempo a contar del pomodoro
        self.pomodoro_timer_label = ttk.Label(self.tab1, text='25:00', font=('Segoe UI', 48))
        self.pomodoro_timer_label.pack(pady=20)
        #Tiempo a contar del descanso corto
        self.short_break_timer_label = ttk.Label(self.tab2, text='05:00', font=('Segoe UI', 48))
        self.short_break_timer_label.pack(pady=20)
        #Tiempo a contar del descanso largo
        self.long_break_timer_label = ttk.Label(self.tab3, text='15:00', font=('Segoe UI', 48))
        self.long_break_timer_label.pack(pady=20)

        self.tabs.add(self.tab1, text='Pomodoro')
        self.tabs.add(self.tab2, text='Descanso Corto')
        self.tabs.add(self.tab3, text='Descanso Largo')

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        self.start_button = ttk.Button(self.grid_layout, text='Start', command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.skip_button = ttk.Button(self.grid_layout, text='Saltar', command=self.skip_clock)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self.grid_layout, text='Reset', command=self.reset_clock)
        self.reset_button.grid(row=0, column=2)

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text='Pomodoros: 0', font=('Segoe UI',14))
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3)

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select())+1

        if timer_id == 1:
            full_seconds = 60*25
            #full_seconds = 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
                self.root.update()
                time.sleep(1)
                full_seconds -= 1

            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f'Pomodoros: {self.pomodoros}')
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()
        elif timer_id == 2:
            full_seconds = 60*5
            #full_seconds = 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        elif timer_id == 3:
            full_seconds = 15*5
            #full_seconds = 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.config(text=f'{minutes:02d}:{seconds:02d}')
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()

    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text='25:00')
        self.short_break_timer_label.config(text='05:00')
        self.long_break_timer_label.config(text='15:00')
        self.pomodoro_counter_label.config(text='Pomodoros: 0')
        self.running = False
    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 1:
            self.pomodoro_timer_label.config(text='25:00')
        elif current_tab == 2:
            self.short_break_timer_label.config(text='05:00')
        else:
            self.long_break_timer_label.config(text='15:00')
        self.stopped = True
        self.skipped = True
PomodoroClock()
