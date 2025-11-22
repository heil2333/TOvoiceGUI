import os
import shutil
import asyncio
from edge_tts import Communicate
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 支持的语言列表（可根据需要扩展）
SUPPORTED_VOICES = [
    "en-US-AvaNeural",
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "zh-CN-XiaoyanNeural",
    "ja-JP-NanamiNeural"
]

async def text_to_speech(text, output_file, voice, rate):
    communicate = Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

def ensure_output_folder():
    folder = "output"
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(folder)
    return folder

class TTSGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edge-TTS 批量生成器")
        self.root.geometry("600x400")

        self.input_file = None

        # 选择文件部分
        self.file_label = tk.Label(root, text="未选择文件")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(root, text="选择文本文件", command=self.select_file)
        self.select_button.pack(pady=5)

        # 语音选择
        tk.Label(root, text="选择语音角色：").pack()
        self.voice_combo = ttk.Combobox(root, values=SUPPORTED_VOICES)
        self.voice_combo.set(SUPPORTED_VOICES[0])
        self.voice_combo.pack(pady=5)

        # 语速设置
        tk.Label(root, text="语速（例如 +25% 或 -10%）：").pack()
        self.rate_entry = tk.Entry(root)
        self.rate_entry.insert(0, "+25%")
        self.rate_entry.pack(pady=5)

        # 开始按钮
        self.start_button = tk.Button(root, text="开始转换", command=self.start_conversion)
        self.start_button.pack(pady=10)

        # 日志区域
        self.log_text = tk.Text(root, height=10, width=70)
        self.log_text.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.input_file = file_path
            self.file_label.config(text=os.path.basename(file_path))

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_conversion(self):
        if not self.input_file:
            messagebox.showerror("错误", "请先选择一个文本文件！")
            return

        voice = self.voice_combo.get()
        rate = self.rate_entry.get().strip()

        try:
            with open(self.input_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件：{e}")
            return

        output_folder = ensure_output_folder()
        self.log("开始生成语音文件...")

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            output_file = os.path.join(output_folder, f"out_{i+1}.wav")
            asyncio.run(text_to_speech(line, output_file, voice, rate))
            self.log(f"已生成：{output_file}")

        messagebox.showinfo("完成", f"语音文件已全部生成在 '{output_folder}' 文件夹中。")

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSGUIApp(root)
    root.mainloop()