import tkinter as tk
import tkinter.ttk as ttk
import os
import youtube_dl
import subprocess
import ffmpeg

class YouTubeConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create a label and a text field for the YouTube link
        self.link_label = tk.Label(self, text="YouTube Link:")
        self.link_field = tk.Entry(self)

        # Create a button for initiating the conversion process
        self.convert_button = tk.Button(self, text="Convert", command=self.convert)
        self.exit_button = tk.Button(self, text="Exit", command=self.destroy)

        # Use the .pack() method to arrange the widgets in the user interface
        self.link_label.pack()
        self.link_field.pack()
        self.convert_button.pack()
        self.exit_button.pack()

    def convert(self):
        # Get the YouTube link from the text field
        link = self.link_field.get()

        # Use try-except blocks to handle any errors that may occur during the conversion process
        try:
            # Create a progress bar
            self.progress = tk.IntVar()
            self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate", variable=self.progress)
            self.progress_bar.pack()

            # Set the window title to "Downloading"
            self.title("Downloading")

            # Download the video in the best available quality
            ydl_opts = {"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
            "progress_hooks": [self.download_progress]}

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            # Get the title of the video
            title = subprocess.run(["youtube-dl", "--get-title", link], capture_output=True).stdout.decode().strip()

            # Set the window title to "Converting"

            mp3_file = title + ".mp3"
            if os.path.exists(mp3_file):
            # Overwrite the MP3 file if it already exists
                os.replace(mp3_file, mp3_file + ".bak")

            self.title("Converting")

            # Get the name of the video file
            video_file = subprocess.run(["youtube-dl", "--get-filename", link], capture_output=True).stdout.decode().strip()

            # Convert the video to an MP3 using multiple threads to speed up the process
            subprocess.run(["ffmpeg", "-i", video_file, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", "-threads", "4", mp3_file])

            # Delete the original video file if it exists
            if os.path.exists(video_file):
                os.remove(video_file)


                # Set the window title to "Completed"
                self.title("Completed")

                # Delete the backup file if it exists
                if os.path.exists(mp3_file + ".bak"):
                    os.remove(mp3_file + ".bak")

                subprocess.run(["open", os.path.dirname(video_file)])

                self.progress_bar.pack_forget()
        except Exception as e:
            # Print an error message if an exception is raised
            print(f"An error occurred: {e}")

    def download_progress(self, d):
        # Update the progress bar with the download progress
        self.progress.set(int(d["downloaded_bytes"] / d["total_bytes"] * 100))
        self.update()
    

if __name__ == '__main__':
    converter = YouTubeConverter()
    converter.mainloop()
