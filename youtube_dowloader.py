import PySimpleGUI as sg
from pytube import YouTube

# https://www.youtube.com/watch?v=MRjVdu_cLwI&ab_channel=TheLegendSongs

"""
Paste the youtube link into the GUI and click 'Submit'
On the download tab choose the quality of video you like 
"""

YouTube_icon = b"iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAA3hJREFUaIHtmc9rXFUYhp/3ZJJJmzGZTBGaCopUMCAGOxPEhRTdli514cKFC125kWoJFNGgaAX1HxBcuPIPUNFdKAFBG6O2uHHnj7SgmTv5xcztZO7rYhITpK1pcmYmgXngMpcD85z3O/dy+e490KdPnz69RJ3yGjQHAeAZyASmfcSd6L8DV2GQsbGnw4Aet3QSUwQXhQrAiM0IIi+TR+S9fQ6DhgFBcDu4dvkNWJC5XUwLaFqkMikmtdq/EhvAhvE6qIaoyb6ZtXyNlZX5aWjesYDF0thLJryLdCr2SkXBXjLZm5XqyqfbQ/8W8EOp+IHRG5I6dVtFwbbBH1aqtYuwVcD34+PngvjisIffxrZlzpeT5KsAEMTMUQkPIEkWMwBaLB17IGP4N0mh18HuBdtZoPFgsIfPHrXwAJKCPXw2WEz1Osx+sZgKiMP5yNwL4lQgYyKa0L4RzbUXMiaCxIlovlvNKTK/jv13LOfdkDgRDOOxhMvr6/Vyknx0C5125llnXo3lvh2G8SAYjS1+qlpdrSTJ22o2H8HZx9j12HMACEaDId8JOUB5ff2vcrV2YdM8amefYDf//197x5AP6mAB2zyZJL9XqrVXaG4+hrPPsVsxvIJ8MORiyPZCeW3t13K19oJa2bTtL9uN2f4x5EIveqAzKys/VqrJ+WBmDlKEJHVt9Xfz3djYmYGB8E4G5w66gDnb7tZVuFooTGooNwt6Lkb/Zds5wSYwGCHfHVkoFh+y9JbEizGvumAzZ0jVoQKuHz9+spHPX0K8HKToTztDmgNSoBBTfH10tNTIhYspejVIIzHdu9FWAasQpx+aGBkpLOQHX0vRhSAVYzjvhmE1ByTAwzGEzfzQL5JKMVx7QZAEzHI0YRfDA9gsBwLd7eFjErgRAvzZ6xz7xiyFLOPnXufYN+anQKNxJVZ32FXsFo3GlVCp15cM873Oc68Y5iv1+lIAsHn/oK1tN7FtzGXY+n4/nSTfyLx3ZIoQlytJ8nX7dBeLpdLztmctJg/jt1Jn/kPypXK19tn22O1CaqFUmJQHn7B8Gut+iXHDfbQ3N45JDGVmeOt1NC8Y2nqzy8nkEDl2NjpgZ3emJdGy2xsc4FQoNU5BKbiBtYHYEKxhaoaa7ZvAtbVa7dtn293zTtiOLFU7reZgAGAOslnIOjVXnz59+vSOfwA2Gm9nCgq3WQAAAABJRU5ErkJggg=="


def progress_check(stream, chunk, bytes_remaining):
    window["-DOWNLOAD_PROGRESS-"].update(
        100 - round(bytes_remaining / stream.filesize * 100)
    )


def on_complete(stream, file_path):
    window["-DOWNLOAD_PROGRESS-"].update(0)


sg.theme("DarkBrown4")
start_layout = [
    # [sg.Titlebar("YouTube Downloader")],
    [sg.Input(key="-INPUT-"), sg.Button("submit")],
]

info_tab = [
    [sg.Text("Title:"), sg.Text("", key="-TITLE-")],
    [sg.Text("Length:"), sg.Text("", key="-LENGTH-")],
    [sg.Text("Views:"), sg.Text("", key="-VIEWS-")],
    [sg.Text("Author:"), sg.Text("", key="-AUTHOR-")],
    [
        sg.Text("Description:"),
        sg.Multiline(
            "", key="-DESCRIPTION-", size=(40, 20), no_scrollbar=True, disabled=True
        ),
    ],
]

download_tab = [
    [
        sg.Frame(
            "Best Quality",
            [
                [
                    sg.Button("Download", key="-BEST-"),
                    sg.Text("", key="-BESTRES-"),
                    sg.Text("", key="-BESTSIZE-"),
                ]
            ],
        )
    ],
    [
        sg.Frame(
            "Worst Quality",
            [
                [
                    sg.Button("Download", key="-WORST-"),
                    sg.Text("", key="-WORSTRES-"),
                    sg.Text("", key="-WORSTSIZE-"),
                ]
            ],
        )
    ],
    [
        sg.Frame(
            "Audio",
            [[sg.Button("Download", key="-AUDIO-"), sg.Text("", key="-AUDIOSIZE-")]],
        )
    ],
    [sg.VPush()],
    [
        sg.Progress(
            100,
            orientation="h",
            size=(20, 20),
            key="-DOWNLOAD_PROGRESS-",
            expand_x=True,
        )
    ],
]

main_layout = [
    # [sg.Titlebar("Converter")],
    [sg.TabGroup([[sg.Tab("info", info_tab), sg.Tab("download", download_tab)]])],
]

sg.set_options(icon=YouTube_icon)
window = sg.Window("Youtube Downloader", start_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "submit":
        video_object = YouTube(
            values["-INPUT-"],
            on_progress_callback=progress_check,
            on_complete_callback=on_complete,
        )
        window.close()

        # main window info setup
        window = sg.Window("Converter", main_layout, finalize=True)
        window["-TITLE-"].update(video_object.title)
        window["-LENGTH-"].update(f"{round(video_object.length / 60,2)} minutes")
        window["-VIEWS-"].update(video_object.views)
        window["-AUTHOR-"].update(video_object.author)
        window["-DESCRIPTION-"].update(video_object.description)

        # main window download setup
        window["-BESTSIZE-"].update(
            f"{round(video_object.streams.get_highest_resolution().filesize / 1048576,1)} MB"
        )
        window["-BESTRES-"].update(
            video_object.streams.get_highest_resolution().resolution
        )

        window["-WORSTSIZE-"].update(
            f"{round(video_object.streams.get_lowest_resolution().filesize / 1048576,1)} MB"
        )
        window["-WORSTRES-"].update(
            video_object.streams.get_lowest_resolution().resolution
        )

        window["-AUDIOSIZE-"].update(
            f"{round(video_object.streams.get_audio_only().filesize / 1048576,1)} MB"
        )

    if event == "-BEST-":
        video_object.streams.get_highest_resolution().download()

    if event == "-WORST-":
        video_object.streams.get_lowest_resolution().download()

    if event == "-AUDIO-":
        video_object.streams.get_audio_only().download()

window.close()
