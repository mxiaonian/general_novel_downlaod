# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, ttk
from fontTools.ttLib import TTFont
import toml



class FontDecryptionApp:
    def __init__(self, master):
        self.master = master
        master.title("字体解密小工具")
        master.geometry("600x600")

        # 建立主窗口
        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # 保存路径
        ttk.Label(main_frame, text="选择字体编码文件:", anchor="center").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.font_path_entry = ttk.Entry(main_frame)
        self.font_path_entry.grid(row=0, column=1, columnspan=1,padx=5, pady=5, sticky="ew")
        ttk.Button(main_frame, text="选择", command=self.choose_font_file).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="选择文字映射配置:", anchor="center").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.mapping_entry = ttk.Entry(main_frame)
        self.mapping_entry.grid(row=1, column=1, columnspan=1,padx=5, pady=5, sticky="ew")
        ttk.Button(main_frame, text="选择", command=self.choose_font_mapping).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="选择输入文件:", anchor="center").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.input_file_entry = ttk.Entry(main_frame)
        self.input_file_entry.grid(row=2, column=1, columnspan=1,padx=5, pady=5, sticky="ew")
        ttk.Button(main_frame, text="选择", command=self.input_file).grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="选择保存位置:", anchor="center").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.output_path_entry = ttk.Entry(main_frame)
        self.output_path_entry.grid(row=3, column=1, columnspan=1,padx=5, pady=5, sticky="ew")
        ttk.Button(main_frame, text="选择", command=self.output_path).grid(row=3, column=2, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="保存名称:", anchor="center").grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.save_name_entry = ttk.Entry(main_frame)
        self.save_name_entry.grid(row=4, column=1, columnspan=1,padx=5, pady=5, sticky="ew")

        # 解密按钮
        self.download_button = ttk.Button(main_frame, text="开始解密", command=self.start_decry)
        self.download_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # 日志窗口
        self.log_text = tk.Text(main_frame, height=12, width=70)
        self.log_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # 配置每一列的权重
        main_frame.columnconfigure(0, weight=1)  # 第一列权重为1
        main_frame.columnconfigure(1, weight=3)  # 第二列权重为6
        main_frame.columnconfigure(2, weight=1)  # 第三列权重为3
        # 配置行的权重
        main_frame.rowconfigure(6, weight=1)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.master.update_idletasks()

    def choose_font_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("字体文件", "*.ttf")])
        if file_path:
            self.font_path_entry.delete(0, tk.END)
            self.font_path_entry.insert(0, file_path)
            self.font_file = file_path

    def choose_font_mapping(self):
        file_path = filedialog.askopenfilename(filetypes=[("配置文件", "*.toml")])
        if file_path:
            self.mapping_entry.delete(0, tk.END)
            self.mapping_entry.insert(0, file_path)
            self.mapping_file = file_path

    def input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)
            self.input_file = file_path

    def output_path(self):
        file_path = filedialog.askdirectory()
        if file_path:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, file_path)
            self.output_path = file_path

    def start_decry(self):
        try:
            font_path = self.font_path_entry.get()
            mapping = self.mapping_entry.get()
            input_file = self.input_file_entry.get()
            save_dir = self.output_path_entry.get()
            save_name = self.save_name_entry.get()

            if not os.path.exists(font_path) or not os.path.exists(input_file) or not os.path.exists(mapping):
                self.log("文件路径无效")
                return

            raw_text = open(input_file, 'r', encoding='utf-8').read()
            font = TTFont(font_path)
            with open(mapping, 'r', encoding='utf-8') as f:
                config = toml.load(f)
            cmap = font.getBestCmap()

            output_text = raw_text
            for code, name in cmap.items():
                if name in config:
                    char = config[name]
                    custom_char = chr(code)
                    output_text = output_text.replace(custom_char, char)
            self.log(output_text)

            if save_dir:
                save_path = os.path.join(save_dir, save_name)
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                self.log(f"文件已保存到: {save_path}")
            else:
                self.log("未指定保存路径")
        except Exception as e:
            self.log(f"发生错误: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FontDecryptionApp(root)
    root.mainloop()