from tkinter import Tk, Label, Button, Entry, END, W, E, S, N, Frame, Radiobutton, IntVar, Canvas, StringVar, Checkbutton, Scrollbar, RIGHT, Y
from pytube import YouTube
import os
import re

class YouTubeDownloader():

    def __init__ (self, master=None):
        self.master = master
        master.title = "YouTubeDownloader"
        self.track_check = {}

        # FRAMES
        self.input_url_frame = Frame(self.master, borderwidth=2, relief="flat")
        self.frame_options = Frame(self.master)
        self.frame_list = Frame(self.master)
        self.canvas_list = Canvas(self.frame_list)

        # input url frame's WIDGETS
        self.url_label = Label(self.input_url_frame, text="Paste yt url:", padx=20)
        
        self.download_path_label = Label(self.input_url_frame, text="Download path:", padx=20)
        
        self.paste_url = Entry(self.input_url_frame)
        self.paste_url.config(width=50)

        self.find_button = Button(self.input_url_frame, text="Find", command=self.find_files)

        home_path = os.path.expanduser('~')
        download_path = os.path.join(home_path, "Downloads")
        self.path_to_download = Entry(self.input_url_frame)
        self.path_to_download.config(width=50)
        self.path_to_download.insert(0, download_path)

        # options frame's WIDGETS
        self.options_label = Label(self.frame_options, text="Choose option:")
        v = IntVar()
        self.option = ""
        self.progressive_option = Radiobutton(self.frame_options, text="progressive", variable=v, value=0,
                selectcolor="grey", command=lambda: self.change_option("progressive")) 
        self.adaptive_option = Radiobutton(self.frame_options, text="adaptive", variable=v, value=1,
                selectcolor="grey", command=lambda: self.change_option("adaptive"))

        # list frame's WIdgets
        self.canvas_list.grid(row=0, column=0, sticky=N+W)

        # LAYOUT

        # input url frame
        self.input_url_frame.grid(row=0, column=0, sticky=W)
        self.url_label.grid(row=0, column=0, sticky=W)
        self.paste_url.grid(row=1, column=0, columnspan=3, sticky=W)
        self.find_button.grid(row=1, column=3)
        self.download_path_label.grid(row=2, column=0, columnspan=3, sticky=W)
        self.path_to_download.grid(row=3, column=0, sticky=W)
        

        # options frame
        self.frame_options.grid(row=1, column=0, sticky=W)
        self.options_label.grid(row=0, column=0, sticky=E)
        self.progressive_option.grid(row=1, column=0)
        self.adaptive_option.grid(row=1, column=1)

        # videos list
        self.frame_list.grid(row=2, column=0, sticky=W)

    def change_option(self, method):
        self.option = method

    def find_files(self):

        # reset frame and track_check
        self.track_check = {}
        
        self.frame_list.destroy()
        self.frame_list = Frame(self.master)
        self.frame_list.grid(row=2, column=0)

        self.canvas_list = Canvas(self.frame_list)
        self.canvas_list.grid(row=0, column=0)
        
        self.video_list = Frame(self.canvas_list)
        self.canvas_list.create_window((0,0), window=self.video_list, anchor=N+W)

        self.scrollbar = Scrollbar(self.frame_list, orient="vertical", command=self.canvas_list.yview)
        self.scrollbar.grid(row=0, column=2, sticky=N+S)
        self.canvas_list.configure(yscrollcommand=self.scrollbar.set)


        video_url = self.paste_url.get()
        if(len(video_url) > 0):
            try:
                video = YouTube(self.paste_url.get())
                self.create_list(video)
            except:
                print("Error")
        else:
            print("You didn't provide a url.")
    
    def create_list(self, video):
        if (self.option == "progressive"):
            list_of_files = video.streams.filter(progressive=True)
        elif (self.option == "adaptive"):
            list_of_files = video.streams.filter(adaptive=True)
        else:
            list_of_files = video.streams

        for i in range(len(list_of_files)):
            self.track_check[i] = Checkbutton(self.video_list, text=list_of_files[i], selectcolor="grey", onvalue=1, offvalue=0) 
            self.track_check[i].var = IntVar()
            self.track_check[i]['variable'] = self.track_check[i].var
            # self.track_check[i]['command'] = lambda x=self.track_check[i]: print(x.var.get())
            self.track_check[i].grid(row=i, column=0, columnspan=2, sticky=W)


        self.download_button = Button(self.frame_list, text="download", command=lambda: self.download_files(list_of_files, video))
        self.download_button.grid(row=i+2, column=0, sticky=W)
        # print(len(self.track_check))
    
        self.video_title_label = Label(self.frame_list, text=video.title)
        self.video_title_label.grid(row=i+1, column=0, sticky=W)

        self.video_list.update_idletasks()
        canvas_width = max(self.track_check[j].winfo_width() for j in range(len(self.track_check)))
        if(len(list_of_files)<10):
            canvas_height = sum(self.track_check[j].winfo_height() for j in range(len(self.track_check)))
        else:
            canvas_height = self.track_check[0].winfo_height()*10
        self.canvas_list.config(height=canvas_height, width=canvas_width)
        self.canvas_list.config(scrollregion=self.canvas_list.bbox("all"))
        
    def download_files(self, list_of_files, video):
        reg_title = re.compile(r"\w*")
        title_list = reg_title.findall(video.title)
        title = "".join(title_list)
        reg_file_format = re.compile(r"/\w*")
        for key, num in zip(self.track_check, range(len(self.track_check))):
            if (self.track_check[key].var.get() == 1):
                output = list_of_files[key].download(self.path_to_download.get())
                file_format = reg_file_format.search(list_of_files[key].mime_type)[0][1:]
                os.rename(output, f"{self.path_to_download.get()}/{title}{num}.{file_format}")
            else:
                continue
        

root = Tk()
you_tube_downloader = YouTubeDownloader(root)
root.mainloop()