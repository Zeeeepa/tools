#!/usr/bin/env python3
import os
import re
import sys
import json
import logging
import tkinter as tk
import threading
import configparser
import argparse
from tkinter import filedialog, ttk, messagebox, scrolledtext
from bs4 import BeautifulSoup
from pathlib import Path

# Set up logging
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

def extract_code_from_html(html_file_path, output_dir=None, preview_only=False):
    """
    Extract code blocks from HTML file and create corresponding files.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_dir (str, optional): Directory to save extracted files. Defaults to current directory.
        preview_only (bool, optional): If True, only generate preview data without creating files.
            
    Returns:
        list: List of created file paths or preview data
    """
    # Set default output directory if not provided
    if output_dir is None:
        output_dir = os.getcwd()
    
    # Create output directory if it doesn't exist and not in preview mode
    if not preview_only:
        os.makedirs(output_dir, exist_ok=True)
    
    # Read HTML file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # Try with different encoding if utf-8 fails
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
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all code blocks
    code_blocks = {}
    current_file = None
    
    # Find all elements with the file path class
    file_headers = soup.find_all(class_=re.compile("text-sm text-zinc-400 mb-2 font-mono"))
    
    if not file_headers:
        logger.warning(f"No file headers found with class 'text-sm text-zinc-400 mb-2 font-mono'. Check if the HTML structure matches the expected pattern.")
    
    for header in file_headers:
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
        
        # Find the next table with the code table class
        table = header.find_next('table', class_='syntax-highlight')
        if table:
            # Find all rows with the code line class
            added_lines = table.find_all('tr', class_='line added')
            
            for line in added_lines:
                # Extract code from the line
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)
    
    # If preview only, return the preview data
    if preview_only:
        return code_blocks
    
    # Create files with extracted code
    files_created = []
    for file_path, code_lines in code_blocks.items():
        if not code_lines:
            continue
        
        # Create full path
        full_path = os.path.join(output_dir, file_path)
        
        try:
            # Create directory structure
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write code to file
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(code_lines))
            
            files_created.append(file_path)
            logger.info(f"Created file: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
    
    return files_created

def preview_code_from_html(html_file_path, selectors, encoding="utf-8"):
    """
    Generate a preview of code blocks from HTML file.
    
    Args:
        html_file_path (str): Path to the HTML file
        selectors (dict): Dictionary of CSS selectors
        encoding (str, optional): File encoding. Defaults to "utf-8".
    
    Returns:
        dict: Preview data
    """
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

class CodeExtractor:
    def __init__(self):
        self.file_path_selector = r"text-sm text-zinc-400 mb-2 font-mono"
        self.code_table_selector = r"syntax-highlight"
        self.code_line_selector = r"line added"
        self.extracted_files = []
        self.preview_data = {}
        
    def extract_code_from_html(self, html_file_path, output_dir=None, preview_only=False):
        """
        Extract code blocks from HTML file and create corresponding files.
        
        Args:
            html_file_path (str): Path to the HTML file
            output_dir (str, optional): Directory to save extracted files. Defaults to current directory.
            preview_only (bool, optional): If True, only generate preview data without creating files.
            
        Returns:
            list: List of created file paths or preview data
        """
        # Set default output directory if not provided
        if output_dir is None:
            output_dir = os.getcwd()
        
        # Create output directory if it doesn't exist and not in preview mode
        if not preview_only:
            os.makedirs(output_dir, exist_ok=True)
        
        # Read HTML file
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            # Try with different encoding if utf-8 fails
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
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all code blocks
        code_blocks = {}
        current_file = None
        
        # Find all elements with the file path class
        file_headers = soup.find_all(class_=re.compile(self.file_path_selector))
        
        if not file_headers:
            logger.warning(f"No file headers found with class '{self.file_path_selector}'. Check if the HTML structure matches the expected pattern.")
        
        for header in file_headers:
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
            
            # Find the next table with the code table class
            table = header.find_next('table', class_=self.code_table_selector)
            if table:
                # Find all rows with the code line class
                added_lines = table.find_all('tr', class_=self.code_line_selector)
                
                for line in added_lines:
                    # Extract code from the line
                    code_text = line.get_text().strip()
                    code_blocks[current_file].append(code_text)
        
        # If preview only, return the preview data
        if preview_only:
            self.preview_data = code_blocks
            return code_blocks
        
        # Create files with extracted code
        files_created = []
        for file_path, code_lines in code_blocks.items():
            if not code_lines:
                continue
            
            # Create full path
            full_path = os.path.join(output_dir, file_path)
            
            try:
                # Create directory structure
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # Write code to file
                with open(full_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(code_lines))
                
                files_created.append(file_path)
                logger.info(f"Created file: {file_path}")
            except Exception as e:
                logger.error(f"Error creating file {file_path}: {e}")
        
        self.extracted_files = files_created
        return files_created

class HTMLCodeExtractorV2App:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Code Extractor v2")
        self.root.geometry("800x600")
        
        # Create the extractor
        self.extractor = CodeExtractor()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.extract_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.preview_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.extract_tab, text="Extract")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.preview_tab, text="Preview")
        
        # Set up the extract tab
        self.setup_extract_tab()
        
        # Set up the settings tab
        self.setup_settings_tab()
        
        # Set up the preview tab
        self.setup_preview_tab()
        
        # Create the status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize progress bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
    
    def setup_extract_tab(self):
        # Create the file selection section
        file_frame = ttk.LabelFrame(self.extract_tab, text="Select HTML File", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        # Create the output directory section
        output_frame = ttk.LabelFrame(self.extract_tab, text="Output Directory", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        # Get desktop path
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "WEB-CODES")
        self.output_path_var = tk.StringVar(value=self.desktop_path)
        
        ttk.Label(output_frame, text="Files will be extracted to:").pack(anchor=tk.W, pady=5)
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir).pack(side=tk.RIGHT, padx=5)
        
        # Create the encoding section
        encoding_frame = ttk.LabelFrame(self.extract_tab, text="File Encoding", padding="10")
        encoding_frame.pack(fill=tk.X, pady=10)
        
        self.encoding_var = tk.StringVar(value="utf-8")
        ttk.Radiobutton(encoding_frame, text="UTF-8", variable=self.encoding_var, value="utf-8").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(encoding_frame, text="Latin-1", variable=self.encoding_var, value="latin-1").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(encoding_frame, text="Auto-detect", variable=self.encoding_var, value="auto").pack(side=tk.LEFT, padx=20)
        
        # Create the action buttons
        button_frame = ttk.Frame(self.extract_tab)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Preview", command=self.preview_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Extract Code", command=self.extract_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def setup_settings_tab(self):
        # Create the settings form
        settings_frame = ttk.LabelFrame(self.settings_tab, text="HTML Selectors", padding="10")
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # File path selector
        ttk.Label(settings_frame, text="File Path Class:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path_selector_var = tk.StringVar(value=self.extractor.file_path_selector)
        ttk.Entry(settings_frame, textvariable=self.file_path_selector_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Code table selector
        ttk.Label(settings_frame, text="Code Table Class:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.code_table_selector_var = tk.StringVar(value=self.extractor.code_table_selector)
        ttk.Entry(settings_frame, textvariable=self.code_table_selector_var, width=50).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Code line selector
        ttk.Label(settings_frame, text="Code Line Class:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.code_line_selector_var = tk.StringVar(value=self.extractor.code_line_selector)
        ttk.Entry(settings_frame, textvariable=self.code_line_selector_var, width=50).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Save settings button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Configure grid
        settings_frame.columnconfigure(1, weight=1)
    
    def setup_preview_tab(self):
        # Create the preview area
        preview_frame = ttk.LabelFrame(self.preview_tab, text="Code Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a scrolled text widget for the preview
        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, width=80, height=20)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_text.config(state=tk.DISABLED)
    
    def browse_file(self):
        """Open file dialog to select HTML file"""
        file_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html;*.htm"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def browse_output_dir(self):
        """Open directory dialog to select output directory"""
        dir_path = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_path_var.get()
        )
        if dir_path:
            self.output_path_var.set(dir_path)
    
    def save_settings(self):
        """Save the current settings"""
        self.extractor.file_path_selector = self.file_path_selector_var.get()
        self.extractor.code_table_selector = self.code_table_selector_var.get()
        self.extractor.code_line_selector = self.code_line_selector_var.get()
        
        messagebox.showinfo("Settings Saved", "Your settings have been saved.")
    
    def preview_code(self):
        """Generate a preview of the code extraction"""
        html_file = self.file_path_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        # Update status
        self.status_var.set("Generating preview...")
        self.root.update()
        
        try:
            # Extract code in preview mode
            preview_data = self.extractor.extract_code_from_html(html_file, preview_only=True)
            
            # Update the preview text
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            
            if preview_data:
                for file_path, code_lines in preview_data.items():
                    if code_lines:
                        self.preview_text.insert(tk.END, f"File: {file_path}\n")
                        self.preview_text.insert(tk.END, "-" * 80 + "\n")
                        self.preview_text.insert(tk.END, "\n".join(code_lines) + "\n\n")
                
                self.status_var.set(f"Preview generated: {len(preview_data)} files found")
            else:
                self.preview_text.insert(tk.END, "No code blocks found in the HTML file.")
                self.status_var.set("No code blocks found")
            
            self.preview_text.config(state=tk.DISABLED)
            
            # Switch to the preview tab
            self.notebook.select(self.preview_tab)
            
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_code(self):
        """Extract code from the selected HTML file"""
        html_file = self.file_path_var.get()
        output_dir = self.output_path_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        # Update status
        self.status_var.set("Extracting code...")
        self.progress['value'] = 0
        self.root.update()
        
        # Run extraction in a separate thread to keep UI responsive
        def extraction_thread():
            try:
                # Extract code
                files_created = self.extractor.extract_code_from_html(html_file, output_dir)
                
                # Update UI from the main thread
                self.root.after(0, lambda: self.update_after_extraction(files_created, output_dir))
            except Exception as e:
                # Update UI from the main thread
                self.root.after(0, lambda: self.show_error(str(e)))
        
        threading.Thread(target=extraction_thread).start()
        
        # Show progress
        self.progress['value'] = 50
    
    def update_after_extraction(self, files_created, output_dir):
        """Update UI after extraction is complete"""
        self.progress['value'] = 100
        
        if files_created:
            message = f"Successfully extracted {len(files_created)} files to {output_dir}"
            self.status_var.set(message)
            
            # Ask if user wants to open the output directory
            if messagebox.askyesno("Extraction Complete", f"{message}\n\nDo you want to open the output directory?"):
                self.open_output_directory(output_dir)
        else:
            self.status_var.set("No files were created")
            messagebox.showinfo("Extraction Complete", "No files were created. Check if the HTML structure matches the expected pattern.")
    
    def show_error(self, error_message):
        """Show error message"""
        self.progress['value'] = 0
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", f"An error occurred: {error_message}")
    
    def open_output_directory(self, directory):
        """Open the output directory in file explorer"""
        try:
            if sys.platform == 'win32':
                os.startfile(directory)
            elif sys.platform == 'darwin':  # macOS
                import subprocess
                subprocess.Popen(['open', directory])
            else:  # Linux
                import subprocess
                subprocess.Popen(['xdg-open', directory])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory: {str(e)}")

def extract_code_from_html_cli(html_file_path, output_dir=None, file_path_selector=None, code_table_selector=None, code_line_selector=None):
    """
    Extract code blocks from HTML file and create corresponding files.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_dir (str, optional): Directory to save extracted files. Defaults to current directory.
        file_path_selector (str, optional): CSS selector for file paths. Defaults to "text-sm text-zinc-400 mb-2 font-mono".
        code_table_selector (str, optional): CSS selector for code tables. Defaults to "syntax-highlight".
        code_line_selector (str, optional): CSS selector for code lines. Defaults to "line added".
    
    Returns:
        list: List of created file paths
    """
    # Create an extractor instance
    extractor = CodeExtractor()
    
    # Set custom selectors if provided
    if file_path_selector:
        extractor.file_path_selector = file_path_selector
    if code_table_selector:
        extractor.code_table_selector = code_table_selector
    if code_line_selector:
        extractor.code_line_selector = code_line_selector
    
    # Extract code
    return extractor.extract_code_from_html(html_file_path, output_dir)

def main():
    # Check if running in CLI mode
    if len(sys.argv) > 1:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Extract code blocks from HTML files and create corresponding files.')
        parser.add_argument('html_file', help='Path to the HTML file')
        parser.add_argument('-o', '--output-dir', help='Directory to save extracted files. Defaults to current directory.')
        parser.add_argument('--file-path-selector', help='CSS selector for file paths. Defaults to "text-sm text-zinc-400 mb-2 font-mono".')
        parser.add_argument('--code-table-selector', help='CSS selector for code tables. Defaults to "syntax-highlight".')
        parser.add_argument('--code-line-selector', help='CSS selector for code lines. Defaults to "line added".')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
        parser.add_argument('--v2', action='store_true', help='Use the v2 interface')
        
        args = parser.parse_args()
        
        # Set logging level based on verbose flag
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Check if v2 interface is requested
        if args.v2:
            root = tk.Tk()
            app = HTMLCodeExtractorV2App(root)
            root.mainloop()
        else:
            # Extract code from HTML file
            files_created = extract_code_from_html_cli(
                args.html_file,
                args.output_dir,
                args.file_path_selector,
                args.code_table_selector,
                args.code_line_selector
            )
            
            # Print summary
            if files_created:
                print(f"Successfully extracted {len(files_created)} files.")
                if args.verbose:
                    print("Files created:")
                    for file_path in files_created:
                        print(f"  - {file_path}")
            else:
                print("No files were created. Check if the HTML structure matches the expected pattern.")
    else:
        # Run in GUI mode
        root = tk.Tk()
        app = HTMLExtractorApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()
