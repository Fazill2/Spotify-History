from queue import Empty
from spotify_data import Spotify_data
import PySimpleGUI as sg
from os.path import exists
import sys

sg.theme('Dark Green 4')

left_col = [[sg.Text("Enter file name: "),sg.InputText(size=(30, 1)),sg.Push()],
            [sg.Text("Number:"),sg.InputText(size=(10, 1)),sg.Push()],
            [sg.Text("Plot Filter:"),sg.InputText(size=(30, 1)),sg.Push()],
            [sg.Button('Merge'),sg.Button('Load_data'),sg.Button('Sum'),sg.Button('Exit')],
            [sg.Button('Time_per_date'),sg.Button('Most_played_songs'),sg.Button('Most_played_artists')]]
layout = [[sg.Column(left_col, element_justification='l')]]
window = sg.Window("Spotify Stats", layout)

if __name__ == "__main__":
    data_loaded = 0
    while True:
        print = sg.Print
        event, values = window.read()
        if event == 'Merge':
            filename = values[0]
            Spotify_data.merge_json_files(filename)
            sg.popup("Files merged")
        if event == 'Load_data':
            filename = values[0]
            if exists(filename):
                data = Spotify_data.get_data(filename)
                data_loaded = 1
                sg.popup("Data loaded")
            else:
                sg.popup("File does not exist")
        if event == 'Sum':
            if data_loaded:
                filter = values[2] if values[2] != "" else None
                sg.Popup(Spotify_data.time_sum(data))
            else:
                sg.Popup("Load data first")
        if event == 'Time_per_date':
            if data_loaded:
                filter = values[2] if values[2] != "" else None
                Spotify_data.time_played_per_date_plot(data,filter)
            else:
                sg.Popup("Load data first")
        if event == 'Most_played_songs':
            if data_loaded:
                print("Songs: ")
                num = int(values[1]) if values[1] != "" else 10
                Spotify_data.print_time(Spotify_data.most_played_songs(data), num)
            else:
                sg.Popup("Load data first")
        if event == 'Most_played_artists':
            if data_loaded:
                print("Artists: ")
                num = int(values[1]) if values[1] != "" else 10
                Spotify_data.print_time(Spotify_data.most_played_artists(data), num)
            else:
                sg.Popup("Load data first")
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()
