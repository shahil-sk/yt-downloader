from pytube import YouTube
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip,AudioFileClip
import socket
import tkinter
import tkinter as tk
import customtkinter
import urllib.request
from PIL import Image

os.system('cls' if os.name == 'nt' else 'clear')
 #test link ::   https://www.youtube.com/watch?v=TK4N5W22Gts


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
internet()

title = ""
author = ""
duration = ""
descirption = ""
resolutions = ['144p', '240p', '360p', '480p', '720p', '1080p', 'Audio only']

print("|------------------|")
print("|:::: Author : SK  |")
print("|------------------|\n")

def directoryVerification():
    if(internet() == 1):
        print("(INTERNET AVAILABLE)\n")
    else:
        print("(INTERNET UNAVAILABLE)\n")

    if os.path.exists("Video") :
        print(" >>> Video Folder existes!")
    else:
        os.mkdir("Video")
        print(" >>> Video Folder Created")
    if os.path.exists("Audio"):
        print(" >>> Audio Folder exists")
    else:
        os.mkdir("Audio")
        print(" >>> Audio Folder Created")
    if os.path.isfile("vid.jpg"):
        os.remove("vid.jpg")
        print(" >>> Old file Removed")
    else:
        print(" >>> Directory Status : GOOD")
    print("-------------------------------------------")
directoryVerification()

def GatherInfo(): 
    print("\n         (SEARCH BUTTON CLICKED)\n")

    try:
        print(" >>> Gathering Info about ( ",YouTube(link.get()).title," )\n")
        grab = YouTube(link.get(), on_progress_callback = on_progress)

        title    = grab.title
        author   = grab.author
        duration = grab.length
        descirption = grab.description

        print(" title       : ",title)
        print(" Author      : ",author)
        print(" Duration    : ",duration)
        print(" Description : ",descirption)

        #header.configure(text=title)
        #GettingRes(grab,title)
        getThumb(grab)
        activitySecond(grab)

    except:
        header.configure(text="Invalid Link!",text_color='red')
        print(" >>> Invalid Link! ")

def getThumb(grab):
    print(" >>> Getting Thumbnail")
    try:
        os.remove('vid.jpg')
        print(" >>> Removed Existing Thumbnail file")
    except:
        print(" >>> Thumbnail file not found")
    urllib.request.urlretrieve(grab.thumbnail_url,'vid.jpg')
    print(" >>> Thumbnail Retrived")

def GettingRes(grab,title):
    print("\n >>> Getting Available resolutions for ( ",title," )")
    res = [stream.resolution for stream in grab.streams.filter(type="video")]
    uni_list = sorted(list(set(res)))
    #uni_list.insert(0,"Audio Only")
    print("     Final resolutoin : ",uni_list)
    '''audio = grab.streams.get_audio_only()
    filesize = audio.filesize/1000000
    filesize = "{:.2f}".format(filesize)
    print("     Getting filesize for res : Audio Only (",file," Mb )")
    ress = [sub[: -1] for sub in uni_list]
    l = len(ress)
    for i in range(l):
        vid = grab.streams.filter(res=ress[i]).first()
        file = vid.filesize/1000000
        file = "{:.2f}".format(file)
        print("     Getting filesize for res : ",ress[i]," (",file," Mb )")
    
    print("\n >>> Resolution Retrived ")'''
    menu.configure(values = uni_list)

def activityMain():
    print(" >>> On Main Activity")
    #Adding activityMain Elements
    check.pack(pady=5)
    header.pack(pady=3)
    link.pack(pady=10)
    search.pack(pady=10)

    #Removing activitySecond Elements
    back.place_forget()
    ytitle.place_forget()
    channel.place_forget()
    len.place_forget()
    downloadbutton.place_forget()
    menu.place_forget()
    image_label.place_forget()
    progresstext.place_forget()
    progressbar.place_forget()

def activitySecond(grab):
    print(" >>> On Second Activity")
    progressbar.set(0)
    #Removing activityMain Elements
    search.pack_forget()
    link.pack_forget()
    header.pack_forget()
    check.pack_forget()

    #Adding activitySecond Elements
    back.pack(ipadx=7)
    back.place(x=20,y=20)
    ytitle.place(x=420, y=110)
    channel.place(x=420, y=140)
    len.place(x=420, y=170)
    menu.configure(values = resolutions)
    menu.place(x=420, y=220)
    downloadbutton.place(x=420, y=260)
    
    progresstext.pack()
    progresstext.place(x=480, y=330)
    progressbar.pack()
    progressbar.place(x=230,y=360)
    ytitle.configure (text="Title   : "+grab.title)
    channel.configure(text="Channel : "+grab.author)
    try:
        my_image = customtkinter.CTkImage(light_image=Image.open('vid.jpg'), size=(40, 40))
        my_image._get_scaled_light_photo_image
        image_label.configure(Image=my_image)
        image_label.pack()
        image_label.place(x=50, y=100)
    except:
        print(" >>> Still problem in Thumbnail")

def on_progress(stream, chunk, bytes_remaining):  
    totalsize = stream.filesize
    bytesdownloaded = totalsize - bytes_remaining
    percentage_complete = bytesdownloaded / totalsize * 100
    print(percentage_complete)
    pers = str(int(percentage_complete))
    progresstext.configure(text= pers + '%')
    progresstext.update()
    progressbar.set(float(percentage_complete) / 100)

def Download():
    progressbar.set(0)
    grab = YouTube(link.get(), on_progress_callback=on_progress)
    print(" >>> Downloading Started")

    if menu.get() == 'Audio only':
        print(" >>> AUDIO ONLY SELECTED")
        progresstext.configure(text="Downloading")
        grab.streams.get_audio_only().download("Audio",filename=grab.title+'.mp3')
    else:
        progresstext.configure(text="Downloading")
        print(" >>> "+menu.get()+" IS SELECTED")
        video_stream = grab.streams.filter(res=menu.get()).first()
        audio_stream = grab.streams.get_audio_only()
        progresstext.configure(text="DONE",text_color='green')
        #file
        video_file = video_stream.download("Video",filename='video')
        audio_file = audio_stream.download("Video",filename='audio')
        #clip
        print(" >>> Converting")
        progresstext.configure(text="Converting...")
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        #merge
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile('Video/'+grab.title+'.mp4')
        progresstext.configure(text="DONE",text_color='green')
        print(" >>> Removing Unwanted file")
        os.remove(video_file)
        os.remove(audio_file)
    


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme('blue')


app = customtkinter.CTk()
app.anchor(customtkinter.CENTER)
app.geometry("900x420")
app.title("SK's Downloader")

header = customtkinter.CTkLabel(app,text="Insert your link here!")

if(internet() == 1 ):
    check = customtkinter.CTkLabel(app,text="Connected",text_color='green')
else:
    check = customtkinter.CTkLabel(app,text="No Internet",text_color='red')

check.pack(pady=5)
header.pack(pady=3)

url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=300, height=35,textvariable=url)
link.pack(pady=10)

search = customtkinter.CTkButton(app, text="Search",command=GatherInfo)
search.pack(pady=10)

#ActivitySecond.here
back = customtkinter.CTkButton(app, text="<", height=30, width=30,fg_color='blue',command=activityMain)
ytitle = customtkinter.CTkLabel(app, text="vidoe name comes here")
channel = customtkinter.CTkLabel(app, text="channel name")
len = customtkinter.CTkLabel(app, text="")
menu = customtkinter.CTkComboBox(app,values = ['Select here'], text_color="white")
menu.configure(state="readonly")
downloadbutton = customtkinter.CTkButton(app,text="DOWNLOAD", fg_color='green',command=Download)
image_label = customtkinter.CTkLabel(app,text="")
#Progress BAR
progresstext = customtkinter.CTkLabel(app, text="0%")
progressbar = customtkinter.CTkProgressBar(app, width=500)
progressbar.set(0)

app.mainloop()
print(" >>> Cleaning Up")
try:
    print(" >>> Removing Unwanted files")
    os.remove('vid.jpg')
except:
    print(" >>> Nothing to Clean Up")