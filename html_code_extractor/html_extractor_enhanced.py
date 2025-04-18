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

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default configuration
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
    """
    Load configuration from file or use defaults.
    
    Args:
        config_path (str, optional): Path to config file
        
    Returns:
        dict: Configuration dictionary
    """
    if not config_path:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    
    config = DEFAULT_CONFIG.copy()
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                
            # Update config with user settings
            for section, values in user_config.items():
                if section in config:
                    if isinstance(values, dict):
                        config[section].update(values)
                    else:
                        config[section] = values
                else:
                    config[section] = values
                    
            logger.info(f"Loaded configuration from {config_path}")
        else:
            logger.info("No configuration file found, using defaults")
            
            # Create default config file
            save_config(config, config_path)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
    
    return config

def save_config(config, config_path=None):
    """
    Save configuration to file.
    
    Args:
        config (dict): Configuration dictionary
        config_path (str, optional): Path to config file
    """
    if not config_path:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        logger.info(f"Saved configuration to {config_path}")
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")

def extract_code_from_html(html_file_path, output_dir, selectors=None, encoding='utf-8', 
                          callback=None, preview_only=False):
    """
    Extract code blocks from HTML file and create corresponding files.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_dir (str): Directory to save extracted files
        selectors (dict, optional): CSS selectors for finding elements
        encoding (str, optional): File encoding to use
        callback (function, optional): Callback function for progress updates
        preview_only (bool, optional): If True, don't create files, just return data
    
    Returns:
        dict: Dictionary with extraction results
    """
    # Set default selectors if not provided
    if selectors is None:
        selectors = DEFAULT_CONFIG["selectors"]
    
    # Create output directory if it doesn't exist and we're not in preview mode
    if not preview_only:
        os.makedirs(output_dir, exist_ok=True)
    
    # Read HTML file
    try:
        with open(html_file_path, 'r', encoding=encoding) as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # Try with different encodings if utf-8 fails
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for enc in encodings:
            try:
                with open(html_file_path, 'r', encoding=enc) as file:
                    html_content = file.read()
                encoding = enc  # Remember successful encoding
                logger.info(f"Successfully read file with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            logger.error("Failed to read HTML file with any encoding")
            return {"success": False, "error": "Failed to read HTML file with any encoding"}
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return {"success": False, "error": str(e)}
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all code blocks
    code_blocks = {}
    current_file = None
    
    # Find all elements with the specified class for file paths
    file_headers = soup.find_all(class_=re.compile(selectors["file_path_class"]))
    
    if not file_headers:
        logger.warning("No file headers found. Check if the HTML structure matches the expected pattern.")
        return {"success": False, "error": "No file headers found", "files": []}
    
    total_headers = len(file_headers)
    
    for i, header in enumerate(file_headers):
        # Update progress
        if callback:
            progress = (i / total_headers) * 100
            callback(progress, f"Processing file {i+1} of {total_headers}")
        
        # Extract file path from the header text
        file_path = header.get_text().strip()
        
        # Clean up the file path
        if file_path.endswith(':'):
            file_path = file_path[:-1]  # Remove trailing colon
        
        # Skip empty file paths
        if not file_path:
            continue
        
        current_file = file_path
        code_blocks[current_file] = []
        
        # Find the next table with the specified class
        table = header.find_next('table', class_=selectors["code_table_class"])
        if table:
            # Find all rows with the specified class
            added_lines = table.find_all('tr', class_=selectors["code_line_class"])
            
            for line in added_lines:
                # Extract code from the line
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)
    
    # Create files with extracted code
    files_created = []
    files_with_errors = []
    
    if preview_only:
        # Just return the code blocks without creating files
        return {
            "success": True, 
            "files": [{"path": path, "content": "\n".join(lines)} for path, lines in code_blocks.items() if lines],
            "encoding": encoding
        }
    
    total_files = len(code_blocks)
    for i, (file_path, code_lines) in enumerate(code_blocks.items()):
        # Update progress
        if callback:
            progress = ((total_headers + i) / (total_headers + total_files)) * 100
            callback(progress, f"Creating file {i+1} of {total_files}")
        
        if not code_lines:
            continue
        
        # Create full path
        full_path = os.path.join(output_dir, file_path)
        
        try:
            # Create directory structure
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write code to file
            with open(full_path, 'w', encoding=encoding) as file:
                file.write('\n'.join(code_lines))
            
            files_created.append(file_path)
            logger.info(f"Created file: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
            files_with_errors.append({"path": file_path, "error": str(e)})
    
    # Final progress update
    if callback:
        callback(100, "Extraction complete")
    
    return {
        "success": True,
        "files_created": files_created,
        "files_with_errors": files_with_errors,
        "encoding": encoding
    }

class HTMLExtractorApp:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        
        # Apply configuration
        window_size = self.config["ui"]["window_size"]
        self.root.title("HTML Code Extractor")
        self.root.geometry(window_size)
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Extract")
        
        # Create settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Create preview tab
        self.preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_tab, text="Preview")
        
        # Set up the main tab
        self.setup_main_tab()
        
        # Set up the settings tab
        self.setup_settings_tab()
        
        # Set up the preview tab
        self.setup_preview_tab()
        
        # Create the status bar
        self.status_frame = ttk.Frame(root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=2)
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=2)
    
    def setup_main_tab(self):
        """Set up the main extraction tab"""
        main_frame = ttk.Frame(self.main_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the file selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select HTML File", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        # Create the output directory section
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        # Get default output path from config
        self.output_path_var = tk.StringVar(value=self.config["output"]["default_dir"])
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=50)
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir).pack(side=tk.RIGHT, padx=5)
        
        # Create options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        # File encoding option
        ttk.Label(options_frame, text="File Encoding:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.encoding_var = tk.StringVar(value=self.config["output"]["encoding"])
        encoding_combo = ttk.Combobox(options_frame, textvariable=self.encoding_var, width=15)
        encoding_combo['values'] = ('utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16')
        encoding_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Create the action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Preview", command=self.preview_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Extract Code", command=self.extract_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def setup_settings_tab(self):
        """Set up the settings tab"""
        settings_frame = ttk.Frame(self.settings_tab, padding="10")
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the selectors section
        selectors_frame = ttk.LabelFrame(settings_frame, text="HTML Selectors", padding="10")
        selectors_frame.pack(fill=tk.X, pady=10)
        
        # File path class selector
        ttk.Label(selectors_frame, text="File Path Class:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_path_class_var = tk.StringVar(value=self.config["selectors"]["file_path_class"])
        ttk.Entry(selectors_frame, textvariable=self.file_path_class_var, width=40).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Code table class selector
        ttk.Label(selectors_frame, text="Code Table Class:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.code_table_class_var = tk.StringVar(value=self.config["selectors"]["code_table_class"])
        ttk.Entry(selectors_frame, textvariable=self.code_table_class_var, width=40).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Code line class selector
        ttk.Label(selectors_frame, text="Code Line Class:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.code_line_class_var = tk.StringVar(value=self.config["selectors"]["code_line_class"])
        ttk.Entry(selectors_frame, textvariable=self.code_line_class_var, width=40).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # UI settings
        ui_frame = ttk.LabelFrame(settings_frame, text="UI Settings", padding="10")
        ui_frame.pack(fill=tk.X, pady=10)
        
        # Window size
        ttk.Label(ui_frame, text="Window Size:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.window_size_var = tk.StringVar(value=self.config["ui"]["window_size"])
        ttk.Entry(ui_frame, textvariable=self.window_size_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Save button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5, pady=10)
        ttk.Button(settings_frame, text="Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=5, pady=10)
    
    def setup_preview_tab(self):
        """Set up the preview tab"""
        preview_frame = ttk.Frame(self.preview_tab, padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selector
        file_selector_frame = ttk.Frame(preview_frame)
        file_selector_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_selector_frame, text="Select File:").pack(side=tk.LEFT, padx=5)
        self.preview_file_var = tk.StringVar()
        self.preview_file_combo = ttk.Combobox(file_selector_frame, textvariable=self.preview_file_var, width=50, state="readonly")
        self.preview_file_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.preview_file_combo.bind("<<ComboboxSelected>>", self.update_preview_content)
        
        # Preview content
        preview_content_frame = ttk.LabelFrame(preview_frame, text="File Content")
        preview_content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_content_frame, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Preview stats
        self.preview_stats_var = tk.StringVar(value="No files previewed yet")
        ttk.Label(preview_frame, textvariable=self.preview_stats_var).pack(side=tk.BOTTOM, anchor=tk.W, padx=5, pady=5)
    
    def browse_file(self):
        """Open file dialog to select HTML file"""
        file_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html;*.htm"), ("HTM Files", "*.htm"), ("HTML Files", "*.html"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def browse_output_dir(self):
        """Open directory dialog to select output directory"""
        dir_path = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if dir_path:
            self.output_path_var.set(dir_path)
    
    def update_progress(self, progress, message):
        """Update progress bar and status message"""
        self.progress_var.set(progress)
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def extract_code(self):
        """Extract code from the selected HTML file"""
        html_file = self.file_path_var.get()
        output_dir = self.output_path_var.get()
        encoding = self.encoding_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        # Get current selectors from settings
        selectors = {
            "file_path_class": self.file_path_class_var.get(),
            "code_table_class": self.code_table_class_var.get(),
            "code_line_class": self.code_line_class_var.get()
        }
        
        # Update status
        self.status_var.set("Extracting code...")
        self.progress_var.set(0)
        self.root.update()
        
        # Run extraction in a separate thread to keep UI responsive
        def extraction_thread():
            try:
                result = extract_code_from_html(
                    html_file, 
                    output_dir, 
                    selectors=selectors,
                    encoding=encoding,
                    callback=self.update_progress
                )
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.extraction_complete(result))
            except Exception as e:
                # Handle exceptions in the main thread
                self.root.after(0, lambda: self.extraction_error(str(e)))
        
        threading.Thread(target=extraction_thread).start()
    
    def extraction_complete(self, result):
        """Handle extraction completion"""
        if result["success"]:
            files_created = result.get("files_created", [])
            files_with_errors = result.get("files_with_errors", [])
            
            if files_created:
                self.status_var.set(f"Completed: Created {len(files_created)} files")
                
                message = f"Successfully extracted {len(files_created)} files to {self.output_path_var.get()}"
                if files_with_errors:
                    message += f"\n\nWarning: {len(files_with_errors)} files had errors during creation."
                
                messagebox.showinfo("Success", message)
            else:
                self.status_var.set("No files created")
                messagebox.showwarning("Warning", "No files were created. Check if the HTML structure matches the expected pattern.")
        else:
            self.status_var.set("Extraction failed")
            messagebox.showerror("Error", f"Extraction failed: {result.get('error', 'Unknown error')}")
    
    def extraction_error(self, error_message):
        """Handle extraction error"""
        self.status_var.set("Error occurred")
        self.progress_var.set(0)
        messagebox.showerror("Error", f"An error occurred: {error_message}")
    
    def preview_code(self):
        """Preview code from the selected HTML file without creating files"""
        html_file = self.file_path_var.get()
        encoding = self.encoding_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        # Get current selectors from settings
        selectors = {
            "file_path_class": self.file_path_class_var.get(),
            "code_table_class": self.code_table_class_var.get(),
            "code_line_class": self.code_line_class_var.get()
        }
        
        # Update status
        self.status_var.set("Generating preview...")
        self.progress_var.set(0)
        self.root.update()
        
        # Run preview in a separate thread to keep UI responsive
        def preview_thread():
            try:
                result = extract_code_from_html(
                    html_file, 
                    "", 
                    selectors=selectors,
                    encoding=encoding,
                    callback=self.update_progress,
                    preview_only=True
                )
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.preview_complete(result))
            except Exception as e:
                # Handle exceptions in the main thread
                self.root.after(0, lambda: self.extraction_error(str(e)))
        
        threading.Thread(target=preview_thread).start()
    
    def preview_complete(self, result):
        """Handle preview completion"""
        if result["success"]:
            files = result.get("files", [])
            
            if files:
                self.status_var.set(f"Preview generated: {len(files)} files")
                
                # Switch to preview tab
                self.notebook.select(self.preview_tab)
                
                # Update file selector
                file_paths = [file["path"] for file in files]
                self.preview_file_combo['values'] = file_paths
                self.preview_file_combo.current(0)
                
                # Store preview data
                self.preview_data = {file["path"]: file["content"] for file in files}
                
                # Update preview content
                self.update_preview_content()
                
                # Update stats
                total_lines = sum(content.count('\n') + 1 for content in self.preview_data.values())
                self.preview_stats_var.set(f"Found {len(files)} files with {total_lines} lines of code")
            else:
                self.status_var.set("No files found")
                messagebox.showwarning("Warning", "No files were found. Check if the HTML structure matches the expected pattern.")
        else:
            self.status_var.set("Preview failed")
            messagebox.showerror("Error", f"Preview failed: {result.get('error', 'Unknown error')}")
    
    def update_preview_content(self, event=None):
        """Update preview content when a file is selected"""
        selected_file = self.preview_file_var.get()
        if selected_file and hasattr(self, 'preview_data'):
            content = self.preview_data.get(selected_file, "")
            
            # Clear and update text widget
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, content)
            
            # Update line count
            line_count = content.count('\n') + 1
            self.preview_stats_var.set(f"File: {selected_file} ({line_count} lines)")
    
    def save_settings(self):
        """Save current settings to config file"""
        # Update config with current values
        self.config["selectors"]["file_path_class"] = self.file_path_class_var.get()
        self.config["selectors"]["code_table_class"] = self.code_table_class_var.get()
        self.config["selectors"]["code_line_class"] = self.code_line_class_var.get()
        self.config["output"]["default_dir"] = self.output_path_var.get()
        self.config["output"]["encoding"] = self.encoding_var.get()
        self.config["ui"]["window_size"] = self.window_size_var.get()
        
        # Save to file
        save_config(self.config)
        
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.config = DEFAULT_CONFIG.copy()
            
            # Update UI with default values
            self.file_path_class_var.set(self.config["selectors"]["file_path_class"])
            self.code_table_class_var.set(self.config["selectors"]["code_table_class"])
            self.code_line_class_var.set(self.config["selectors"]["code_line_class"])
            self.output_path_var.set(self.config["output"]["default_dir"])
            self.encoding_var.set(self.config["output"]["encoding"])
            self.window_size_var.set(self.config["ui"]["window_size"])
            
            # Save to file
            save_config(self.config)
            
            messagebox.showinfo("Settings Reset", "Settings have been reset to defaults.")

def main():
    root = tk.Tk()
    app = HTMLExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
