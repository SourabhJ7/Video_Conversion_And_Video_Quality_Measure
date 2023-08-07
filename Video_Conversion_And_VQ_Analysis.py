import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import json
from PIL import Image, ImageTk

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(tk.END, file_path)

def convert_video():
    input_file = input_file_entry.get()
    if not input_file:
        return

    output_avi = "output.avi"
    output_m3u8 = "output.m3u8"

    
    subprocess.run(['ffmpeg', '-i', input_file, output_avi])

    
    subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-hls_list_size', '0', '-hls_time', '10', output_m3u8])

    
    original_info = get_video_info(input_file)
    converted_avi_info = get_video_info(output_avi)
    converted_m3u8_info = get_video_info(output_m3u8)

    
    resolution_label.config(text=f"Resolution: {original_info['width']}x{original_info['height']}")
    frame_rate_label.config(text=f"Frame Rate: {original_info['frame_rate']} fps")
    bit_rate_label.config(text=f"Bit Rate: {original_info['bit_rate']} kbps")

    converted_avi_resolution_label.config(text=f"Resolution: {converted_avi_info['width']}x{converted_avi_info['height']}")
    converted_avi_frame_rate_label.config(text=f"Frame Rate: {converted_avi_info['frame_rate']} fps")
    converted_avi_bit_rate_label.config(text=f"Bit Rate: {converted_avi_info['bit_rate']} kbps")

    converted_m3u8_resolution_label.config(text=f"Resolution: {converted_m3u8_info['width']}x{converted_m3u8_info['height']}")
    converted_m3u8_frame_rate_label.config(text=f"Frame Rate: {converted_m3u8_info['frame_rate']} fps")
    converted_m3u8_bit_rate_label.config(text=f"Bit Rate: {converted_m3u8_info['bit_rate']} kbps")

def get_video_info(file_path):
    result = subprocess.Popen(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,bit_rate', '-of', 'json', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = result.communicate()
    info = json.loads(output)
    stream = info['streams'][0]
    width = stream.get('width', 'N/A')
    height = stream.get('height', 'N/A')
    frame_rate = eval(stream.get('r_frame_rate', '0/1'))
    bit_rate = int(stream.get('bit_rate', '0')) / 1000  # Convert to kbps
    return {'width': width, 'height': height, 'frame_rate': frame_rate, 'bit_rate': bit_rate}


root.title("Video Converter")
root.geometry("500x400")


input_file_label = tk.Label(root, text="Select MP4 File:")
input_file_label.pack()

input_file_entry = tk.Entry(root, width=40)
input_file_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

convert_button = tk.Button(root, text="Convert", command=convert_video)
convert_button.pack()

resolution_label = tk.Label(root, text="------ Original Video Quality Parameters ------")
resolution_label.pack()

resolution_label = tk.Label(root, text="Resolution:")
resolution_label.pack()

frame_rate_label = tk.Label(root, text="Frame Rate:")
frame_rate_label.pack()

bit_rate_label = tk.Label(root, text="Bit Rate:")
bit_rate_label.pack()

converted_avi_resolution_label = tk.Label(root, text="------ AVI Video QUality Parameters ------")
converted_avi_resolution_label.pack()

converted_avi_resolution_label = tk.Label(root, text="Resolution:")
converted_avi_resolution_label.pack()

converted_avi_frame_rate_label = tk.Label(root, text="Frame Rate:")
converted_avi_frame_rate_label.pack()

converted_avi_bit_rate_label = tk.Label(root, text="Bit Rate:")
converted_avi_bit_rate_label.pack()

converted_m3u8_resolution_label = tk.Label(root, text="------ HLS Video Quality Parameters ------")
converted_m3u8_resolution_label.pack()

converted_m3u8_resolution_label = tk.Label(root, text="Resolution:")
converted_m3u8_resolution_label.pack()

converted_m3u8_frame_rate_label = tk.Label(root, text="Frame Rate:")
converted_m3u8_frame_rate_label.pack()

converted_m3u8_bit_rate_label = tk.Label(root, text="Bit Rate:")
converted_m3u8_bit_rate_label.pack()

root.mainloop()
