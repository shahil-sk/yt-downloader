import tkinter
import tkinter as tk
from tkinter import ttk
import customtkinter
import os
from pytube import YouTube

print(" -- Application Started")

#function
def getres():
    ytlink = link.get()
    ytobj = YouTube(ytlink)
    #getting resolution
    ytstreams = ytobj.streams.filter(type="video")
    video_res1 = [stream.resolution for stream in ytstreams]
    print("-------------------------------------------")
    print(" -- Prints Duplicate resolution for some reason !!")
    print(video_res1)
    video_res = []
    for x in video_res1:
        if x not in video_res:
            video_res.append(x)
    print("-------------------------------------------")
    print(" -- Getting clean Values")
    print(video_res)
    menu.configure(state="normal")
    return video_res
    
#seacrh function

def search():
    print("\n -- Search Button clicked ::\n")

    try:
        ytlink = link.get()
        ytobj = YouTube(ytlink)
        title.configure(text=ytobj.title,text_color="white")
        download.configure(fg_color="green", state='enabled')
        search.configure(state="hidden")
        print(" -- Link Valid")
        print(" -- Getting Channel Deatials")
    
        detail.configure(text="Channel Name : "+ ytobj.author)
        video_res = getres()
        print("----------------------------------------")
        print(" -- Adding Resolution Values to Menu :-) ")
        video_res.insert(0,"Audio Only")
        menu.configure(values=video_res)
        print(" -- DONE Adding ")
        print(video_res)
        print("----------------------------------------")
        menu.configure(text_color="black")

    except:
        print(" -- invalid link")
        finishlabel.configure(text="Invalid Youtube Link !!", text_color="red")

#download function
def startdownload():
    print("---------------------------------------")
    print(" -- Download Button Clicked ::")
    try:
        print(" -- Downloading Started ")
        ytlink = link.get()
        ytobject = YouTube(ytlink, on_progress_callback=on_progress)
        reso = menu.get()
        print(" -- Resolution : ",reso)
        
        if(reso == "Audio Only"):
            print(" -- Getting Audio file")
            audio = ytobject.streams.get_audio_only()
            finishlabel.configure(text="")
            filesize = audio.filesize / 1000000
            filesize = "{:.2f}".format(filesize)
            print(" -- File Size : ",filesize)
            detail.configure(text=f"Channel :{ytobject.author} || Filesize : {filesize}")
            audio.download()
            print(" -- File Download Complete")
            finishlabel.configure(text="Download Complete !", text_color="green")
        else:
            print(" -- Getting Video file")
            video = ytobject.streams.filter(res=reso).first()
            finishlabel.configure(text="")
            filesize = video.filesize / 1000000
            filesize = "{:.2f}".format(filesize)
            print(" -- File Size : ",filesize)
            detail.configure(text=f"Channel :{ytobject.author}  ||  Filesize : {filesize} Mb")
            video.download()
            print(" -- File Download Complete")
            finishlabel.configure(text="Download Complete !",text_color="green")
    except:
        print(" -- invalid Link")
        finishlabel.configure(text="Invalid Youtube Link !!", text_color="red")

#progressBar
def on_progress(stream, chunk, bytes_remaining):
    
    totalsize = stream.filesize
    bytesdownloaded = totalsize - bytes_remaining
    percentage_complete = bytesdownloaded / totalsize * 100
    print(percentage_complete)
    pers = str(int(percentage_complete))
    pPercentage.configure(text= pers + '%')
    pPercentage.update()

    progressbar.set(float(percentage_complete) / 100)


#System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#App frame
app = customtkinter.CTk()
app.geometry("620x380")
app.title("Youtube Downloader")

#Adding UI elements
title = customtkinter.CTkLabel(app, text="Insert Youtube link !!")
title.pack(padx=10, pady=7)

#misc
detail = customtkinter.CTkLabel(app, text="")
detail.pack()

#link Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40,textvariable = url_var)
link.pack()

#Seacrh button
search = customtkinter.CTkButton(app,text="Search", command=search)
search.pack(pady=15)

#dropdown_list
menu = customtkinter.CTkComboBox(app,values=["Select Resolution"], text_color="white")
menu.pack(pady=3)
menu.configure(state="disabled")

#Download button
download = customtkinter.CTkButton(app, text="Download", fg_color="grey", command =startdownload,state='disabled')
download.pack(pady=7)

#message
finishlabel = customtkinter.CTkLabel(app, text="")
finishlabel.pack()

#prgressbar
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressbar = customtkinter.CTkProgressBar(app, width=400)
progressbar.set(0)
progressbar.pack(padx=10, pady=10)

#Run app
app.mainloop()
