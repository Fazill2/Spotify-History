import json
import datetime as dt
from os import stat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os.path
import numpy as np
import PySimpleGUI as sg

class Spotify_data:
    @staticmethod
    def most_played_songs(data,artist_filter=None):
        time = {}
        for key in data:
            if not key["track&artist"] == "None - None":
                if key["track&artist"] in time:
                    time[key["track&artist"]] += key["ms_played"]
                else:
                    time[key["track&artist"]] = key["ms_played"]
        for el in time:
            time[el] = time[el]/3600000
        sorted_time = {k: v for k, v in sorted(time.items(), key=lambda item: item[1],reverse=True)}
        return sorted_time

    @staticmethod
    def most_played_artists(data):
        time={}
        for key in data:
            if not key["track&artist"] == "None - None":
                if key["master_metadata_album_artist_name"] in time:
                    time[key["master_metadata_album_artist_name"]] += key["ms_played"]
                else:
                    time[key["master_metadata_album_artist_name"]] = key["ms_played"]
        for el in time:
            time[el] = time[el]/3600000
        sorted_time = {k: v for k, v in sorted(time.items(), key=lambda item: item[1],reverse=True)}
        return sorted_time

    @staticmethod
    def time_sum(data):
        curr_sum = 0
        for key in data:
            curr_sum += key["ms_played"]
        return str(round(curr_sum/3600000,2)) + " h"

    @staticmethod
    def time_played_per_hour(data):
        time = {}
        for key in data:
            if key["hour"] in time:
                time[key["hour"]] += key["ms_played"]
            else:
                time[key["hour"]] = key["ms_played"]
        for el in time:
            time[el] = time[el]/3600000
        sorted_time = {k: v for k, v in sorted(time.items(), key=lambda item: item[0],reverse=False)}
        return sorted_time

    @staticmethod
    def time_played_per_hour_plot(data):
        time_per_hour = Spotify_data.time_played_per_hour(data)
        old_names = list(time_per_hour.keys())
        values = list(time_per_hour.values())
        old_sizes = [val/sum(values) for val in values]
        names = ["rest"]
        sizes = [0]
        for i in range(len(old_names)):
            if old_sizes[i] < 0.02:
                sizes[0] += old_sizes[i]
            else:
                names.append(int(old_names[i]))
                sizes.append(old_sizes[i])
        fig, ax = plt.subplots()
        ax.pie(sizes,labels=names, autopct='%1.1f%%', startangle=90, counterclock=False)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

    @staticmethod
    def time_played_per_date(data):
        time={}
        for key in data:
            
            if key["date"] in time:
                time[key["date"]] += key["ms_played"]
            else:
                time[key["date"]] = key["ms_played"]
        for el in time:
            time[el] = time[el]/3600000
        sorted_time = {k: v for k, v in sorted(time.items(), key=lambda item: item[0],reverse=False)}
        return sorted_time

    @staticmethod
    def time_played_per_date_for_plot(data,song_filter=None):
        time={}
        for key in data:
            
            if key["date_python_format"] in time:
                if song_filter is None:
                    time[key["date_python_format"]] += key["ms_played"]
                else:
                    if key["master_metadata_track_name"] == song_filter:
                        time[key["date_python_format"]] += key["ms_played"]
            else:
                if song_filter is None:
                    time[key["date_python_format"]] = key["ms_played"]
                else:
                    if key["master_metadata_track_name"] == song_filter:
                        time[key["date_python_format"]] = key["ms_played"]
        for el in time:
            time[el] = time[el]/3600000
        sorted_time = {k: v for k, v in sorted(time.items(), key=lambda item: item[0],reverse=False)}
        return sorted_time

    @staticmethod
    def time_played_per_date_plot(data,song_filter=None):
        time_per_date = Spotify_data.time_played_per_date_for_plot(data,song_filter)
        names = list(time_per_date.keys())
        values = list(time_per_date.values())
        fig,ax = plt.subplots()
        ax.bar(names, values)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        if song_filter is None:
            plt.title("Time_per_date")
        else:
            title = "Time_per_date - " + song_filter
            plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("time [h]")
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

    @staticmethod
    def get_data(filename):
        with open(filename,encoding='utf-8') as json_file:
            data = json.load(json_file)
        for key in data:
            key.pop("conn_country", None)
            key.pop("episode_name",None)
            key.pop("episode_show_name", None)
            key.pop("incognito_mode",None)
            key.pop("ip_addr_decrypted", None)
            key.pop("shuffle",None)
            key.pop("platform",None)
            key.pop("offline",None)
            key.pop("reason_end",None)
            key.pop("reason_start",None)
            key.pop("user_agent_decrypted",None)
            key.pop("spotify_episode_uri",None)
            key.pop("spotify_track_uri",None)
            key.pop("username",None)
            key.pop("skipped",None)
            if key["master_metadata_track_name"] == None:
                key["track&artist"] = "None - None"
            else:
                key["track&artist"] = key["master_metadata_track_name"] + " - " + key["master_metadata_album_artist_name"]
            key["date"] = key["ts"][:10]
            key["hour"] = key["ts"][11:13]
            key["date_python_format"] = dt.datetime.strptime(key["date"], '%Y-%m-%d').date()
        return data

    @staticmethod
    def print_time(data, num=0):
        i = 1
        print = sg.Print
        for key in data:
            print(key, " - ", round(data[key],2),"h")
            if i == num : break
            i += 1
    
    @staticmethod
    def merge_json_files(res_filename):
        result = list()
        i = 0
        filename = "endsong_"+str(i)+".json"
        while os.path.exists(filename):
            with open(filename, 'r',encoding='utf-8') as infile:
                result.extend(json.load(infile))
            i += 1
            filename = "endsong_"+str(i)+".json"

        with open(res_filename, 'w') as output_file:
            json.dump(result, output_file)


    
