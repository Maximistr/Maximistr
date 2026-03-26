import wave
import numpy as np
import matplotlib.pyplot as plt
import struct
import os
import sys
from PIL import Image

def sound_to_spectrogram(input_wav, output_image):
    """
    Converts a WAV sound file into a spectrogram image.
    This is for visualization only and is not reversible.
    """
    print(f"Opening {input_wav}...")
    with wave.open(input_wav, 'rb') as wav_file:
        # Extract Raw Audio from Wav File
        params = wav_file.getparams()
        print(f"Parameters: {params}")
        
        n_channels, sampwidth, framerate, n_frames = params[:4]
        str_data = wav_file.readframes(n_frames)
        
        # Convert to numpy array
        if sampwidth == 1:
            dtype = np.uint8
        elif sampwidth == 2:
            dtype = np.int16
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth}")
        
        wave_data = np.frombuffer(str_data, dtype=dtype)
        
        # Divide by channels
        if n_channels == 2:
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            # Use only one channel for spectrogram
            data = wave_data[0]
        else:
            data = wave_data

        # Normalize data
        if sampwidth == 2:
            data = data.astype(np.float32) / 32768.0
        else:
            data = (data.astype(np.float32) - 128.0) / 128.0

        print("Generating spectrogram...")
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        Pxx, freqs, bins, im = plt.specgram(data, Fs=framerate, NFFT=1024, noverlap=512, cmap='inferno')
        
        plt.title(f'Spectrogram of {os.path.basename(input_wav)}')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.colorbar(im).set_label('Intensity (dB)')
        
        print(f"Saving image to {output_image}...")
        plt.savefig(output_image)
        plt.close()
        print("Done!")

def sound_to_image_lossless(input_wav, output_image):
    """
    Encodes a WAV file losslessly into the pixels of a PNG image.
    This allows recovering the exact sound file later.
    """
    print(f"Opening {input_wav} for lossless encoding...")
    with wave.open(input_wav, 'rb') as wav_file:
        params = wav_file.getparams()
        n_channels, sampwidth, framerate, n_frames = params[:4]
        raw_data = wav_file.readframes(n_frames)
        
        # Pack metadata into 16 bytes: 
        # 4 bytes magic, 2 for channels, 2 for sampwidth, 4 for framerate, 4 for frames
        metadata = struct.pack('<4sHHII', b'WAV!', n_channels, sampwidth, framerate, n_frames)
        
        full_data = bytearray(metadata) + bytearray(raw_data)
        
        # Calculate image dimensions for RGB (3 bytes per pixel)
        num_bytes = len(full_data)
        pixels_needed = int(np.ceil(num_bytes / 3.0))
        
        width = int(np.ceil(np.sqrt(pixels_needed)))
        height = int(np.ceil(pixels_needed / width))
        
        padding_needed = (width * height * 3) - num_bytes
        if padding_needed > 0:
            full_data.extend(b'\x00' * padding_needed)
            
        img_array = np.frombuffer(full_data, dtype=np.uint8).reshape((height, width, 3))
        
        # Save as Lossless PNG
        img = Image.fromarray(img_array, 'RGB')
        img.save(output_image, format='PNG')
        print(f"Saved lossless image to {output_image}")

def image_to_sound_lossless(input_image, output_wav):
    """
    Decodes a WAV file from the pixels of a PNG image encoded by sound_to_image_lossless.
    """
    print(f"Opening image {input_image} for decoding...")
    img = Image.open(input_image)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img_array = np.array(img, dtype=np.uint8)
    full_data = img_array.tobytes()
    
    # Extract metadata
    metadata = full_data[:16]
    magic, n_channels, sampwidth, framerate, n_frames = struct.unpack('<4sHHII', metadata)
    
    if magic != b'WAV!':
        raise ValueError("Image does not contain valid audio data (magic bytes 'WAV!' not found). Make sure it was created with 'encode_audio'.")
        
    expected_audio_length = n_frames * n_channels * sampwidth
    
    audio_data = full_data[16:16+expected_audio_length]
    
    with wave.open(output_wav, 'wb') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(framerate)
        wav_file.writeframes(audio_data)
        
    print(f"Saved decoded sound to {output_wav}")

def any_image_to_sound(input_image, output_wav):
    """
    Encodes ANY image into a WAV sound file.
    """
    print(f"Opening {input_image} to encode into sound...")
    img = Image.open(input_image)
    
    # We will save the mode, width, height.
    mode_encode = img.mode.encode('ascii')
    mode_len = len(mode_encode)
    
    width, height = img.size
    
    # Pack metadata: magic(4), width(4), height(4), mode_len(1) = 13 bytes
    metadata = struct.pack('<4sIIB', b'IMG!', width, height, mode_len)
    
    full_data = bytearray(metadata) + bytearray(mode_encode) + bytearray(img.tobytes())
    
    # Save as 8-bit mono WAV at 44100Hz
    with wave.open(output_wav, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(1) # 1 byte per sample = 8-bit
        wav_file.setframerate(44100)
        wav_file.writeframes(full_data)
        
    print(f"Saved image as sound to {output_wav}")

def sound_to_any_image(input_wav, output_image):
    """
    Decodes an image that was hidden inside a WAV sound file.
    """
    print(f"Opening {input_wav} to extract image...")
    with wave.open(input_wav, 'rb') as wav_file:
        n_channels, sampwidth, framerate, n_frames = wav_file.getparams()[:4]
        full_data = wav_file.readframes(n_frames)
        
    # Extract metadata
    magic, width, height, mode_len = struct.unpack('<4sIIB', full_data[:13])
    
    if magic != b'IMG!':
        raise ValueError("Audio does not contain a hidden image (magic bytes 'IMG!' not found).")
        
    mode_str = full_data[13:13+mode_len].decode('ascii')
    image_data = full_data[13+mode_len:]
    
    img = Image.frombytes(mode_str, (width, height), image_data)
    img.save(output_image)
    print(f"Saved extracted image to {output_image}")


# --- GUI Implementation ---
import tkinter as tk
from tkinter import filedialog, messagebox

class TransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sound to Image Transfer")
        self.root.geometry("520x400")
        self.root.resizable(False, False)
        
        self.input_file = tk.StringVar()
        self.mode = tk.StringVar(value="spectrogram")
        
        # UI Elements
        tk.Label(root, text="Step 1: Select Mode", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        
        frame_modes = tk.Frame(root)
        frame_modes.pack()
        tk.Radiobutton(frame_modes, text="Spectrogram (Audio -> Image Viewer)", variable=self.mode, value="spectrogram", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Radiobutton(frame_modes, text="Hide Audio in Image (Lossless)", variable=self.mode, value="encode_audio", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Radiobutton(frame_modes, text="Extract Audio from Image", variable=self.mode, value="decode_audio", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Radiobutton(frame_modes, text="Hide Image in Audio (Lossless)", variable=self.mode, value="encode_img", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Radiobutton(frame_modes, text="Extract Image from Audio", variable=self.mode, value="decode_img", font=("Arial", 10)).pack(anchor=tk.W)
        
        tk.Label(root, text="Step 2: Select Input File", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        
        frame_input = tk.Frame(root)
        frame_input.pack(fill=tk.X, padx=20)
        tk.Entry(frame_input, textvariable=self.input_file, width=48, font=("Arial", 10)).pack(side=tk.LEFT, padx=(5, 10))
        tk.Button(frame_input, text="Browse", font=("Arial", 10), command=self.browse_input, width=8).pack(side=tk.LEFT)
        
        tk.Button(root, text="RUN TRANSFER", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.process, width=20, height=2).pack(pady=(25, 10))
        
    def browse_input(self):
        mode = self.mode.get()
        if mode in ["spectrogram", "encode_audio", "decode_img"]:
            filetypes = (("WAV files", "*.wav"), ("All files", "*.*"))
        else:
            filetypes = (("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*"))
            
        filename = filedialog.askopenfilename(title="Select Input File", filetypes=filetypes)
        if filename:
            self.input_file.set(filename)
            
    def process(self):
        input_path = self.input_file.get()
        mode = self.mode.get()
        
        if not input_path or not os.path.exists(input_path):
            messagebox.showerror("Error", "Please select a valid input file.")
            return
            
        base = os.path.splitext(input_path)[0]
        
        try:
            if mode == "spectrogram":
                output_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"{os.path.basename(base)}_spectrogram.png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
                if not output_path: return
                sound_to_spectrogram(input_path, output_path)
                messagebox.showinfo("Success", f"Spectrogram saved to:\n{output_path}")
                
            elif mode == "encode_audio":
                output_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"{os.path.basename(base)}_encoded.png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
                if not output_path: return
                sound_to_image_lossless(input_path, output_path)
                messagebox.showinfo("Success", f"Lossless encoded image saved to:\n{output_path}")
                
            elif mode == "decode_audio":
                output_path = filedialog.asksaveasfilename(defaultextension=".wav", initialfile=f"{os.path.basename(base)}_decoded.wav", filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
                if not output_path: return
                image_to_sound_lossless(input_path, output_path)
                messagebox.showinfo("Success", f"Decoded sound saved to:\n{output_path}")

            elif mode == "encode_img":
                output_path = filedialog.asksaveasfilename(defaultextension=".wav", initialfile=f"{os.path.basename(base)}_hidden.wav", filetypes=(("WAV files", "*.wav"), ("All files", "*.*")))
                if not output_path: return
                any_image_to_sound(input_path, output_path)
                messagebox.showinfo("Success", f"Image hidden in sound file and saved to:\n{output_path}")

            elif mode == "decode_img":
                output_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"{os.path.basename(base)}_extracted.png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
                if not output_path: return
                sound_to_any_image(input_path, output_path)
                messagebox.showinfo("Success", f"Image extracted from sound and saved to:\n{output_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file:\n{str(e)}")

def run_gui():
    root = tk.Tk()
    app = TransferApp(root)
    root.mainloop()

# --- Main Entry Point ---
def main():
    if len(sys.argv) < 2:
        # If no arguments provided, launch GUI automatically
        run_gui()
        sys.exit(0)
        
    # Check if first arg is a command
    command = sys.argv[1].lower()
    
    if command in ['encode_audio', 'decode_audio', 'encode_image', 'decode_image']:
        if len(sys.argv) < 3:
            print(f"Usage: python transfer.py {command} <input_file> [output_file]")
            sys.exit(1)
        input_file = sys.argv[2]
        if len(sys.argv) > 3:
            output_file = sys.argv[3]
        else:
            base = os.path.splitext(input_file)[0]
            if command == 'encode_audio':
                output_file = f"{base}_encoded.png"
            elif command == 'decode_audio':
                output_file = f"{base}_decoded.wav"
            elif command == 'encode_image':
                output_file = f"{base}_hidden.wav"
            elif command == 'decode_image':
                output_file = f"{base}_extracted.png"
                
        if not os.path.exists(input_file):
            print(f"Error: File {input_file} not found.")
            sys.exit(1)
            
        try:
            if command == 'encode_audio':
                sound_to_image_lossless(input_file, output_file)
            elif command == 'decode_audio':
                image_to_sound_lossless(input_file, output_file)
            elif command == 'encode_image':
                any_image_to_sound(input_file, output_file)
            elif command == 'decode_image':
                sound_to_any_image(input_file, output_file)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
            
    else:
        # Default fallback to original spectrogram behavior
        input_wav = sys.argv[1]
        
        # Print help if not a valid file
        if not os.path.exists(input_wav) and input_wav in ['-h', '--help']:
            print("Usage:")
            print("  GUI Mode:                python transfer.py")
            print("  1. Spectrogram:          python transfer.py <input.wav> [output.png]")
            print("  2. Encode audio to PNG:  python transfer.py encode_audio <input.wav> [output.png]")
            print("  3. Decode PNG to audio:  python transfer.py decode_audio <input.png> [output.wav]")
            print("  4. Encode img to WAV:    python transfer.py encode_image <input.png/jpg> [output.wav]")
            print("  5. Decode WAV to img:    python transfer.py decode_image <input.wav> [output.png]")
            sys.exit(0)
            
        if len(sys.argv) > 2:
            output_image = sys.argv[2]
        else:
            base = os.path.splitext(input_wav)[0]
            output_image = f"{base}_spectrogram.png"
            
        if not os.path.exists(input_wav):
            print(f"Error: File {input_wav} not found.")
            sys.exit(1)
            
        try:
            sound_to_spectrogram(input_wav, output_image)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
