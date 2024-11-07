# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, ttk
import time
import toml
from DrissionPage import Chromium
import threading
import os

class NovelDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("通用小说下载器")
        master.geometry("600x600")

        # 建立主窗口
        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # 保存路径
        ttk.Label(main_frame, text="保存路径:", anchor="center").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.path_entry = ttk.Entry(main_frame)
        self.path_entry.grid(row=0, column=1, columnspan=1,padx=5, pady=5, sticky="ew")
        ttk.Button(main_frame, text="选择", command=self.choose_path).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # 目录地址
        ttk.Label(main_frame, text="目录地址:", anchor="center").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.url_entry = ttk.Entry(main_frame)
        self.url_entry.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="目录规则:", anchor="center").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.list_rule_entry = ttk.Entry(main_frame)
        self.list_rule_entry.grid(row=2, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        self.download_button = ttk.Button(main_frame, text="目录规则测试", command=self.test_list_rule)
        self.download_button.grid(row=2, column=2, columnspan=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="书名规则:", anchor="center").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.book_name_rule_entry = ttk.Entry(main_frame)
        self.book_name_rule_entry.grid(row=3, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        self.book_name_test_button = ttk.Button(main_frame, text="书名规则测试", command=self.test_book_name_rule)
        self.book_name_test_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="章名规则:", anchor="center").grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.name_rule_entry = ttk.Entry(main_frame)
        self.name_rule_entry.grid(row=4, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        self.name_rule_button = ttk.Button(main_frame, text="章名规则测试", command=self.test_name_rule)
        self.name_rule_button.grid(row=4, column=2, columnspan=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="内容规则:", anchor="center").grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        self.content_rule_entry = ttk.Entry(main_frame)
        self.content_rule_entry.grid(row=5, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        self.content_rule_button = ttk.Button(main_frame, text="内容规则测试", command=self.test_content_rule)
        self.content_rule_button.grid(row=5, column=2, columnspan=1, padx=5, pady=5, sticky="ew")

        ttk.Label(main_frame, text="分页规则:", anchor="center").grid(row=6, column=0, padx=5, pady=5, sticky="ew")
        self.next_rule_entry = ttk.Entry(main_frame)
        self.next_rule_entry.grid(row=6, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

        self.next_rule_button = ttk.Button(main_frame, text="分页规则测试", command=self.test_next_rule)
        self.next_rule_button.grid(row=6, column=2, columnspan=1, padx=5, pady=5, sticky="ew")


        # 等待时间
        ttk.Label(main_frame, text="等待时间:", anchor="center").grid(row=7, column=0, padx=5, pady=5, sticky="ew")
        self.wait_entry = ttk.Entry(main_frame)
        self.wait_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        self.wait_entry.insert(0, "3")  # Default wait time
        ttk.Button(main_frame, text="秒").grid(row=7, column=2, padx=5, pady=5, sticky="ew")

        # 加载配置按钮
        self.download_button = ttk.Button(main_frame, text="加载配置", command=self.load_config)
        self.download_button.grid(row=8, column=0, columnspan=1, padx=5, pady=5, sticky="ew")

        # 保存配置按钮
        self.download_button = ttk.Button(main_frame, text="保存配置", command=self.save_config)
        self.download_button.grid(row=8, column=2, columnspan=1, padx=5, pady=5, sticky="ew")

        # 下载按钮
        self.download_button = ttk.Button(main_frame, text="开始下载", command=self.start_download)
        self.download_button.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # 暂停/恢复 按钮
        self.pause_resume_button = ttk.Button(main_frame, text="暂停", command=self.toggle_pause_resume,
                                              state=tk.DISABLED)
        self.pause_resume_button.grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # 停止按钮
        self.stop_button = ttk.Button(main_frame, text="终止下载", command=self.stop_download, state=tk.DISABLED)
        self.stop_button.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # 日志窗口
        self.log_text = tk.Text(main_frame, height=12, width=70)
        self.log_text.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=12, column=3, sticky="ns")
        self.log_text['yscrollcommand'] = scrollbar.set

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # 配置UI表权重
        # 配置每一列的权重
        main_frame.columnconfigure(0, weight=1)  # 第一列权重为1
        main_frame.columnconfigure(1, weight=6)  # 第二列权重为6
        main_frame.columnconfigure(2, weight=3)  # 第三列权重为3

        # 配置行的权重
        main_frame.rowconfigure(12, weight=1)



        # 下载控制参数
        self.is_downloading = False
        self.is_paused = False
        self.should_stop = False

    def load_config(self):
        # 弹出选择文件框
        file_path = filedialog.askopenfilename()
        if not file_path:
            self.log("未选择配置文件。")
            return

        try:
            with open(file_path, "r") as f:
                config_data = toml.load(f)

                # 检查配置文件是否包含所有必要的配置项
                required_keys = ["url", "list_rule", "name_rule", "content_rule"]
                if not all(key in config_data for key in required_keys):
                    self.log(f"配置文件 {file_path} 格式不正确，缺少必要的配置项。")
                    return

                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, config_data["path"])
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, config_data["url"])
                self.list_rule_entry.delete(0, tk.END)
                self.list_rule_entry.insert(0, config_data["list_rule"])
                self.book_name_rule_entry.delete(0, tk.END)
                self.book_name_rule_entry.insert(0, config_data["book_name_rule"])
                self.name_rule_entry.delete(0, tk.END)
                self.name_rule_entry.insert(0, config_data["name_rule"])
                self.content_rule_entry.delete(0, tk.END)
                self.content_rule_entry.insert(0, config_data["content_rule"])
                self.next_rule_entry.delete(0, tk.END)
                self.next_rule_entry.insert(0, config_data["next_rule"])
                self.wait_entry.delete(0, tk.END)
                self.wait_entry.insert(0, config_data["wait"])
        except FileNotFoundError:
            self.log(f"未找到配置文件 {file_path}，请先保存配置。")
        except toml.TomlDecodeError:
            self.log(f"配置文件 {file_path} 格式不正确，无法解析。")
        except Exception as e:
            self.log(f"加载配置文件时发生错误: {e}")

    def save_config(self):
        # 弹出保存文件位置框
        save_path = filedialog.askdirectory()
        # 弹出文件名称框
        save_name = filedialog.asksaveasfilename(defaultextension=".toml")

        # 验证用户输入
        if not save_path or not save_name:
            self.log("保存路径或文件名无效，请重新选择。")
            return

        # 拼接完整路径
        full_path = os.path.join(save_path, save_name)

        config_data = {
            "path": self.path_entry.get(),
            "url": self.url_entry.get(),
            "list_rule": self.list_rule_entry.get(),
            "book_name_rule": self.book_name_rule_entry.get(),
            "name_rule": self.name_rule_entry.get(),
            "content_rule": self.content_rule_entry.get(),
            "next_rule": self.next_rule_entry.get(),
            "wait": self.wait_entry.get()
        }

        try:
            with open(full_path, mode="w") as f:
                toml.dump(config_data, f)
        except FileNotFoundError:
            self.log("保存路径或文件名无效，请重新选择。")
        except PermissionError:
            self.log("没有权限写入文件，请检查文件路径和权限。")
        except OSError as e:
            self.log(f"发生错误：{e}")

    def test_list_rule(self):
        threading.Thread(target=self._test_list_rule).start()

    def _test_list_rule(self):
        try:
            list_rule = self.list_rule_entry.get()
            list_url = self.url_entry.get()
            browser = Chromium()
            test_tab = browser.new_tab(list_url)
            novel_lists = test_tab(list_rule).eles('tag:a')  # 获取章节地址元素
            self.log(f"共找到 {len(novel_lists)} 章节")
            novel_links = novel_lists.get.links()
            for novel_link in novel_links:
                self.log(f"获取到章节地址{novel_link}")
        except Exception as e:
            self.log(f"错误：{e}")
            return

    def test_book_name_rule(self):
        threading.Thread(target=self._test_book_name_rule).start()

    def _test_book_name_rule(self):
        try:
            list_url = self.url_entry.get()
            book_name_rule = self.book_name_rule_entry.get()
            browser = Chromium()
            test_tab = browser.new_tab(list_url)
            book_name_element = test_tab.ele(book_name_rule)
            book_name = book_name_element.text  # 获取小说名称
            self.log(f"获取到小说名称{book_name}")
        except Exception as e:
            self.log(f"错误：{e}")
            return

    def test_name_rule(self):
        threading.Thread(target=self._test_name_rule).start()

    def _test_name_rule(self):
        try:
            list_rule = self.list_rule_entry.get()
            name_rule = self.name_rule_entry.get()
            list_url = self.url_entry.get()
            browser = Chromium()
            test_tab = browser.new_tab(list_url)
            novel_lists = test_tab(list_rule).eles('tag:a')  # 获取章节地址元素
            novel_links = novel_lists.get.links()
            novel_link = novel_links[1]
            test_tab.get(novel_link)
            novel_name = test_tab.ele(name_rule).text  # 获取章节名称
            self.log(f"获取到章节名称{novel_name}")

        except Exception as e:
            self.log(f"错误：{e}")
            return

    def test_content_rule(self):
        threading.Thread(target=self._test_content_rule).start()

    def _test_content_rule(self):
        try:
            list_rule = self.list_rule_entry.get()
            content_rule = self.content_rule_entry.get()
            list_url = self.url_entry.get()
            browser = Chromium()
            test_tab = browser.new_tab(list_url)
            novel_lists = test_tab(list_rule).eles('tag:a')
            novel_links = novel_lists.get.links()  # 获取章节地址
            novel_link = novel_links[1]
            test_tab.get(novel_link)
            novel_content = test_tab.ele(content_rule).text  # 获取章节名称
            self.log(f"获取到章节内容：\n {novel_content}")

        except Exception as e:
            self.log(f"错误：{e}")
            return

    def test_next_rule(self):
        threading.Thread(target=self._test_next_rule).start()


    def _test_next_rule(self):
        try:
            list_rule = self.list_rule_entry.get()
            content_rule = self.content_rule_entry.get()
            list_url = self.url_entry.get()
            next_rule = self.next_rule_entry.get()
            browser = Chromium()
            test_tab = browser.new_tab(list_url)
            novel_lists = test_tab(list_rule).eles('tag:a')
            novel_links = novel_lists.get.links()  # 获取章节地址
            novel_link = novel_links[1]
            test_tab.get(novel_link)

            while True:
                # 获取当前页面的内容
                novel_content = test_tab.ele(content_rule).text
                self.log(f"获取到章节内容：\n {novel_content}")

                # 尝试找到下一页的元素
                next_page = test_tab.ele(next_rule)
                if not next_page:
                    break  # 如果没有找到下一页的元素，跳出循环

                # 点击下一页
                next_page.click()

        except Exception as e:
            self.log(f"错误：{e}")
            return




    def choose_path(self):
        folder_selected = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder_selected)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.master.update_idletasks()

    def start_download(self):
        save_path = self.path_entry.get()
        novel_list_url = self.url_entry.get()
        wait_time = float(self.wait_entry.get())

        if not save_path or not novel_list_url:
            self.log("请填写保存路径和目录地址")
            return

        self.download_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.is_downloading = True
        self.is_paused = False
        self.should_stop = False
        threading.Thread(target=self.download_novel, args=(save_path, wait_time), daemon=True).start()

    def toggle_pause_resume(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_resume_button.config(text="暂停")
            self.log("继续下载")
        else:
            self.is_paused = True
            self.pause_resume_button.config(text="继续")
            self.log("下载已暂停")

    def stop_download(self):
        self.should_stop = True
        self.log("正在终止下载...")

    def update_progress(self, current, total):
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.master.update_idletasks()

    def download_novel(self, save_path, wait_time):
        try:
            url = self.url_entry.get()
            list_rule = self.list_rule_entry.get()  # 从list_rule_entry中获取章节列表规则
            book_name_rule = self.book_name_rule_entry.get()  # 从book_name_rule_entry中获取小说名称规则
            name_rule = self.name_rule_entry.get()  # 从name_rule_entry中获取章节名称规则
            content_rule = self.content_rule_entry.get() # 从content_rule_entry中获取章节内容规则
            next_rule = self.next_rule_entry.get()  # 从next_rule_entry中获取下一页规则

            browser = Chromium()  # 创建一个Chromium对象
            tab = browser.get_tab()  # 获取一个新标签页
            tab.get(url)  # 进入小说目录地址
            book_name = tab.ele(book_name_rule).text   # 获取小说名称
            self.master.after(0, self.log, f'获取到小说名称：\n {book_name}')

            novel_list = tab(list_rule).eles('tag:a')  # 获取章节地址元素
            novel_list_len = len(novel_list)  # 获取章节数量
            novel_links = novel_list.get.links()  # 获取章节地址
            self.master.after(0, self.log, f'共{novel_list_len}章')

            for i in range(novel_list_len):
                if self.should_stop:
                    self.master.after(0, self.log, "下载已终止")
                    break

                while self.is_paused:
                    time.sleep(0.1)
                    if self.should_stop:
                        break

                novel_link =novel_links[i]  # 获取章节地址
                self.master.after(0, self.log, f'获取到章节地址：\n {novel_link}')
                tab.get(novel_link)  # 进入章节地址
                novel_title = tab.ele(name_rule).text  # 获取章节名称
                if next_rule:
                    while True:
                        novel_content = tab.ele(content_rule).text  # 获取当前页面的内容
                        with open(os.path.join(save_path, f"{book_name}.txt"), 'a', encoding='utf-8') as f:
                            f.write(novel_content + "\n\n")
                        next_page = tab.ele(next_rule)  # 尝试找到下一页的元素
                        if next_page:
                            tab.scroll.to_see(next_page)
                            time.sleep(wait_time)
                            next_page.click()  # 点击下一页
                        else:
                            break  # 如果没有找到下一页的元素，跳出循环

                else:
                    novel_content = tab.ele(content_rule).text  # 获取章节内容
                    with open(os.path.join(save_path, f"{book_name}.txt"), 'a', encoding='utf-8') as f:
                        f.write(novel_content + "\n\n")

                self.master.after(0, self.log, f' {novel_title} 下载完成')
                self.master.after(0, self.update_progress, i + 1, novel_list_len)
                time.sleep(wait_time)

            if not self.should_stop:
                self.master.after(0, self.log, "下载完成")
        except Exception as e:
            self.master.after(0, self.log, f"发生错误: {str(e)}")
        finally:
            self.is_downloading = False
            self.master.after(0, self.reset_ui)

    def reset_ui(self):
        self.download_button.config(state=tk.NORMAL)
        self.pause_resume_button.config(state=tk.DISABLED, text="暂停")
        self.stop_button.config(state=tk.DISABLED)
        self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = NovelDownloaderApp(root)
    root.mainloop()

