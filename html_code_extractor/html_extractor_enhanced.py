#!/usr/bin/env python3
import os
import re
import sys
import json
import logging
import tkinter as tk
import threading
import configparser
from tkinter import filedialog, ttk, messagebox, scrolledtext
from bs4 import BeautifulSoup
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "selectors": {
        "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
        "code_table_class": "syntax-highlight",
        "code_line_class": "line added"
    },
    "output": {
        "default_dir": os.path.join(os.path.expanduser("~"), "Desktop", "WEB-CODES"),
        "encoding": "utf-8"
    },
    "ui": {
        "theme": "default",
        "window_size": "800x600"
    }
}

def load_config(config_path=None):
    if not config_path:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded configuration from {config_path}")
                return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    logger.info("No configuration file found, using defaults")
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        logger.info(f"Saved configuration to {config_path}")
    except Exception as e:
        logger.error(f"Error saving default configuration: {e}")
    
    return DEFAULT_CONFIG

def save_config(config, config_path=None):
    if not config_path:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info(f"Saved configuration to {config_path}")
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")

def extract_code_from_html(html_file_path, output_dir, selectors, encoding="utf-8", progress_callback=None):
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(html_file_path, 'r', encoding=encoding) as file:
            html_content = file.read()
    except UnicodeDecodeError:
        try:
            with open(html_file_path, 'r', encoding='latin-1') as file:
                html_content = file.read()
            logger.warning(f"Fallback to latin-1 encoding for {html_file_path}")
        except Exception as e:
            logger.error(f"Error reading HTML file: {e}")
            return []
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    code_blocks = {}
    current_file = None
    
    file_path_class = selectors["file_path_class"]
    code_table_class = selectors["code_table_class"]
    code_line_class = selectors["code_line_class"]
    
    file_headers = soup.find_all(class_=re.compile(file_path_class))
    
    if not file_headers:
        logger.warning("No file headers found. Check if the HTML structure matches the expected pattern.")
    
    total_headers = len(file_headers)
    
    for i, header in enumerate(file_headers):
        if progress_callback:
            progress_callback(i / total_headers * 100)
        
        file_path = header.get_text().strip()
        
        if file_path.endswith(':'):
            file_path = file_path[:-1]  
        
        if not file_path:
            continue
        
        current_file = file_path
        code_blocks[current_file] = []
        
        table = header.find_next('table', class_=code_table_class)
        if table:
            added_lines = table.find_all('tr', class_=code_line_class)
            
            for line in added_lines:
                # Extract code from the line, removing line numbers
                code_spans = line.find_all('span')
                if code_spans:
                    # Skip the first span which contains the line number
                    code_text = ''.join(span.get_text() for span in code_spans[1:])
                else:
                    # Fallback to get all text if no spans found
                    code_text = line.get_text().strip()
                    # Try to remove line numbers using regex
                    code_text = re.sub(r'^\d+\s*', '', code_text)
                
                code_blocks[current_file].append(code_text)
    
    files_created = []
    for file_path, code_lines in code_blocks.items():
        if not code_lines:
            continue
        
        full_path = os.path.join(output_dir, file_path)
        
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding=encoding) as file:
                file.write('\n'.join(code_lines))
            
            files_created.append(file_path)
            logger.info(f"Created file: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
    
    if progress_callback:
        progress_callback(100)
    
    return files_created

def preview_code_from_html(html_file_path, selectors, encoding="utf-8"):
    try:
        with open(html_file_path, 'r', encoding=encoding) as file:
            html_content = file.read()
    except UnicodeDecodeError:
        try:
            with open(html_file_path, 'r', encoding='latin-1') as file:
                html_content = file.read()
            logger.warning(f"Fallback to latin-1 encoding for {html_file_path}")
        except Exception as e:
            logger.error(f"Error reading HTML file: {e}")
            return {}
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return {}
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    code_blocks = {}
    current_file = None
    
    file_path_class = selectors["file_path_class"]
    code_table_class = selectors["code_table_class"]
    code_line_class = selectors["code_line_class"]
    
    file_headers = soup.find_all(class_=re.compile(file_path_class))
    
    if not file_headers:
        logger.warning("No file headers found. Check if the HTML structure matches the expected pattern.")
    
    for header in file_headers:
        file_path = header.get_text().strip()
        
        if file_path.endswith(':'):
            file_path = file_path[:-1]  
        
        if not file_path:
            continue
        
        current_file = file_path
        code_blocks[current_file] = []
        
        table = header.find_next('table', class_=code_table_class)
        if table:
            added_lines = table.find_all('tr', class_=code_line_class)
            
            for line in added_lines:
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)
    
    return code_blocks

class HTMLExtractorApp:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        
        window_size = self.config["ui"]["window_size"]
        self.root.title("HTML Code Extractor")
        self.root.geometry(window_size)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Extract")
        
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        self.preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_tab, text="Preview")
        
        self.setup_main_tab()
        
        self.setup_settings_tab()
        
        self.setup_preview_tab()
        
        self.status_frame = ttk.Frame(root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, length=100, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=5)
    
    def setup_main_tab(self):
        main_frame = ttk.Frame(self.main_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        file_frame = ttk.LabelFrame(main_frame, text="Select HTML File", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        self.output_path_var = tk.StringVar(value=self.config["output"]["default_dir"])
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=50)
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir).pack(side=tk.RIGHT, padx=5)
        
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(options_frame, text="File Encoding:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.encoding_var = tk.StringVar(value=self.config["output"]["encoding"])
        encoding_combo = ttk.Combobox(options_frame, textvariable=self.encoding_var, width=15)
        encoding_combo['values'] = ('utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16')
        encoding_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Preview", command=self.preview_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Extract Code", command=self.extract_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def setup_settings_tab(self):
        settings_frame = ttk.Frame(self.settings_tab, padding="10")
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        selectors_frame = ttk.LabelFrame(settings_frame, text="HTML Selectors", padding="10")
        selectors_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(selectors_frame, text="File Path Class:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_path_class_var = tk.StringVar(value=self.config["selectors"]["file_path_class"])
        ttk.Entry(selectors_frame, textvariable=self.file_path_class_var, width=40).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(selectors_frame, text="Code Table Class:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.code_table_class_var = tk.StringVar(value=self.config["selectors"]["code_table_class"])
        ttk.Entry(selectors_frame, textvariable=self.code_table_class_var, width=40).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(selectors_frame, text="Code Line Class:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.code_line_class_var = tk.StringVar(value=self.config["selectors"]["code_line_class"])
        ttk.Entry(selectors_frame, textvariable=self.code_line_class_var, width=40).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ui_frame = ttk.LabelFrame(settings_frame, text="UI Settings", padding="10")
        ui_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(ui_frame, text="Window Size:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.window_size_var = tk.StringVar(value=self.config["ui"]["window_size"])
        ttk.Entry(ui_frame, textvariable=self.window_size_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
    
    def setup_preview_tab(self):
        preview_frame = ttk.Frame(self.preview_tab, padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        file_list_frame = ttk.LabelFrame(preview_frame, text="Files", padding="10")
        file_list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        self.file_listbox = tk.Listbox(file_list_frame, width=30)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        file_scrollbar = ttk.Scrollbar(file_list_frame, orient="vertical", command=self.file_listbox.yview)
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=file_scrollbar.set)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        code_frame = ttk.LabelFrame(preview_frame, text="Code Preview", padding="10")
        code_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.code_text = scrolledtext.ScrolledText(code_frame, wrap=tk.WORD, width=50, height=20)
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        self.preview_data = {}
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html;*.htm"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if dir_path:
            self.output_path_var.set(dir_path)
    
    def save_settings(self):
        self.config["selectors"]["file_path_class"] = self.file_path_class_var.get()
        self.config["selectors"]["code_table_class"] = self.code_table_class_var.get()
        self.config["selectors"]["code_line_class"] = self.code_line_class_var.get()
        self.config["ui"]["window_size"] = self.window_size_var.get()
        self.config["output"]["encoding"] = self.encoding_var.get()
        
        save_config(self.config)
        
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
    
    def reset_settings(self):
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.config = DEFAULT_CONFIG
            
            self.file_path_class_var.set(self.config["selectors"]["file_path_class"])
            self.code_table_class_var.set(self.config["selectors"]["code_table_class"])
            self.code_line_class_var.set(self.config["selectors"]["code_line_class"])
            self.window_size_var.set(self.config["ui"]["window_size"])
            self.encoding_var.set(self.config["output"]["encoding"])
            self.output_path_var.set(self.config["output"]["default_dir"])
            
            save_config(self.config)
            
            messagebox.showinfo("Settings Reset", "Settings have been reset to defaults.")
    
    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def extract_code(self):
        html_file = self.file_path_var.get()
        output_dir = self.output_path_var.get()
        encoding = self.encoding_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        selectors = {
            "file_path_class": self.config["selectors"]["file_path_class"],
            "code_table_class": self.config["selectors"]["code_table_class"],
            "code_line_class": self.config["selectors"]["code_line_class"]
        }
        
        self.status_var.set("Extracting code...")
        self.root.update_idletasks()
        
        def extraction_thread():
            try:
                files_created = extract_code_from_html(
                    html_file, 
                    output_dir, 
                    selectors, 
                    encoding=encoding,
                    progress_callback=self.update_progress
                )
                
                self.root.after(0, lambda: self.extraction_complete(files_created, output_dir))
            except Exception as e:
                self.root.after(0, lambda: self.extraction_error(str(e)))
        
        threading.Thread(target=extraction_thread).start()
    
    def extraction_complete(self, files_created, output_dir):
        if files_created:
            self.status_var.set(f"Completed: Created {len(files_created)} files")
            messagebox.showinfo("Success", f"Successfully extracted {len(files_created)} files to {output_dir}")
        else:
            self.status_var.set("No files created")
            messagebox.showwarning("Warning", "No files were created. Check if the HTML structure matches the expected pattern.")
    
    def extraction_error(self, error_message):
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", f"An error occurred: {error_message}")
    
    def preview_code(self):
        html_file = self.file_path_var.get()
        encoding = self.encoding_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        selectors = {
            "file_path_class": self.config["selectors"]["file_path_class"],
            "code_table_class": self.config["selectors"]["code_table_class"],
            "code_line_class": self.config["selectors"]["code_line_class"]
        }
        
        self.status_var.set("Previewing code...")
        self.root.update_idletasks()
        
        def preview_thread():
            try:
                preview_data = preview_code_from_html(
                    html_file, 
                    selectors, 
                    encoding=encoding
                )
                
                self.root.after(0, lambda: self.preview_complete(preview_data))
            except Exception as e:
                self.root.after(0, lambda: self.preview_error(str(e)))
        
        threading.Thread(target=preview_thread).start()
    
    def preview_complete(self, preview_data):
        self.preview_data = preview_data
        
        self.notebook.select(self.preview_tab)
        
        self.file_listbox.delete(0, tk.END)
        
        for file_path in preview_data.keys():
            self.file_listbox.insert(tk.END, file_path)
        
        if preview_data:
            self.status_var.set(f"Preview ready: {len(preview_data)} files found")
        else:
            self.status_var.set("No files found for preview")
            messagebox.showwarning("Warning", "No files were found. Check if the HTML structure matches the expected pattern.")
    
    def preview_error(self, error_message):
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", f"An error occurred: {error_message}")
    
    def on_file_select(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.file_listbox.get(index)
            
            code_lines = self.preview_data.get(file_path, [])
            
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, '\n'.join(code_lines))

def main():
    root = tk.Tk()
    app = HTMLExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
