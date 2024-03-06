#Required moudels
import tkinter
import tkinter as tk
import customtkinter
from pytube import YouTube
import urllib.request
from PIL import Image
import os

grab = ""

print("Application Started")

#progressBar
def on_progress(stream, chunk, bytes_remaining):
    
    totalsize = stream.filesize
    bytesdownloaded = totalsize - bytes_remaining
    percentage_complete = bytesdownloaded / totalsize * 100
    print(percentage_complete)
    pers = str(int(percentage_complete))
    progresstext.configure(text= pers + '%')
    progresstext.update()

    progressbar.set(float(percentage_complete) / 100)

def validatelink():
    try:
        #validates link and goes to activity 2
        #test link :: https://www.youtube.com/watch?v=TK4N5W22Gts
        grab = YouTube(ytlink.get())
        header.configure(text="Youtube Downloader 2.0",text_color='white')
        serachbutton.pack_forget()
        ytlink.pack_forget()
        back.pack(ipadx=7)
        back.place(x=20,y=20)
        ytitle.place(x=420, y=110)
        channel.place(x=420, y=140)
        len.place(x=420, y=170)
        menu.place(x=420, y=220)
        downloadbutton.place(x=420, y=260)

        image_label.pack()
        image_label.place(x=50, y=100)

        
        progresstext.pack()
        progresstext.place(x=350, y=330)
        progressbar.pack()
        progressbar.place(x=160,y=360)

        

        ytitle.configure (text="Title   : "+grab.title)
        channel.configure(text="Channel : "+grab.author)
        urllib.request.urlretrieve(grab.thumbnail_url,"vid.jpg")
        my_image = customtkinter.CTkImage(light_image=Image.open("vid.jpg"),size=(340, 200))
        image_label.configure(image=my_image)
        res = getres()
        menu.configure(values = res)

    except:
        print("link not valid")
        header.configure(text="LINK NOT VALID",text_color='red')

def downloadvideo():
    progressbar.set(0)
    progresstext.configure(text="")
    grab = YouTube(ytlink.get(), on_progress_callback=on_progress)
    ress = menu.get()
    print(ress)
    if(ress == "Audio Only"):
        audio = grab.streams.get_audio_only()
        filesize = audio.filesize/1000000
        filesize = "{:.2f}".format(filesize)
        audio.download()
        try:
            os.remove("vid.jpg")
        except:
            print("file does not exists")
    else:
        video = grab.streams.filter(res=ress).first()
        filesize = video.filesize/10000000
        filesize = "{:.2f}".format(filesize)
        video.download()
        try:
            os.remove("vid.jpg")
        except:
            print("file does not exists")

    


def getbacktoactivity1():
    print("Back button Clicked")
    header.configure(text="Youtube Downloader 2.0",text_color='white')
    ytlink.pack()
    serachbutton.pack(pady=20,ipady=3)
    back.place_forget()
    ytitle.place_forget()
    channel.place_forget()
    len.place_forget()
    menu.place_forget()
    downloadbutton.place_forget()
    progressbar.place_forget()
    progresstext.place_forget()
    image_label.place_forget()
    os.remove("vid.jpg")

#Getting resolution
def getres():
    print("Getting Available resolutions")

    grab = YouTube(ytlink.get())
    res = [stream.resolution for stream in grab.streams.filter(type="video")]
    uni_list = list(set(res))
    uni_list = sorted(uni_list)
    uni_list.insert(0,"Audio Only")
    return uni_list

#Ui Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme('blue')
app = customtkinter.CTk()
app.anchor(customtkinter.CENTER)
app.geometry("720x480")
app.title("YT 2.0")

#Activity 1
header = customtkinter.CTkLabel(app,text="Youtube Downloader 2.0")
header.pack(pady=20)

    #link stuff
url_var = tkinter.StringVar()
ytlink = customtkinter.CTkEntry(app, width=380, height=40, textvariable=url_var)
ytlink.pack()

serachbutton = customtkinter.CTkButton(app, text="Search", fg_color='Blue', command=validatelink)
serachbutton.pack(pady=20,ipady=2)


#ACTIVITY 2

#backbutton
back = customtkinter.CTkButton(app, text="<", height=30, width=30,fg_color='blue',command=getbacktoactivity1)
ytitle = customtkinter.CTkLabel(app, text="vidoe name comes here")
channel = customtkinter.CTkLabel(app, text="channel name")
len = customtkinter.CTkLabel(app, text="")
menu = customtkinter.CTkComboBox(app,values = ['Select here'], text_color="white")
menu.configure(state="readonly")
downloadbutton = customtkinter.CTkButton(app,text="DOWNLOAD", fg_color='green',command=downloadvideo)


image_label = customtkinter.CTkLabel(app,text="")

#Progress BAR
progresstext = customtkinter.CTkLabel(app, text="0%")

progressbar = customtkinter.CTkProgressBar(app, width=400)
progressbar.set(0)

app.mainloop()
