#!/usr/bin/env python3
import os
import re
import sys
import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from bs4 import BeautifulSoup
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_code_from_html(html_file_path, output_dir):
    """
    Extract code blocks from HTML file and create corresponding files.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_dir (str): Directory to save extracted files
    
    Returns:
        list: List of created file paths
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read HTML file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return []
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all code blocks
    code_blocks = {}
    current_file = None
    
    # Find all elements with class "text-sm text-zinc-400 mb-2 font-mono"
    # These contain the file paths
    file_headers = soup.find_all(class_=re.compile(r"text-sm text-zinc-400 mb-2 font-mono"))
    
    if not file_headers:
        logger.warning("No file headers found. Check if the HTML structure matches the expected pattern.")
    
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
        
        # Find the next table with class "syntax-highlight"
        table = header.find_next('table', class_='syntax-highlight')
        if table:
            # Find all rows with class "line added"
            added_lines = table.find_all('tr', class_='line added')
            
            for line in added_lines:
                # Extract code from the line
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)
    
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

class HTMLExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Code Extractor")
        self.root.geometry("600x400")
        
        # Set up the main frame
        main_frame = ttk.Frame(root, padding="10")
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
        
        # Get desktop path
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "WEB-CODES")
        self.output_path_var = tk.StringVar(value=self.desktop_path)
        
        ttk.Label(output_frame, text="Files will be extracted to:").pack(anchor=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=50, state="readonly").pack(fill=tk.X, padx=5, pady=5)
        
        # Create the action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Extract Code", command=self.extract_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Create the status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_file(self):
        """Open file dialog to select HTML file"""
        file_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html;*.htm"), ("HTM Files", "*.htm"), ("HTML Files", "*.html"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

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
        self.root.update()
        
        try:
            # Extract code
            files_created = extract_code_from_html(html_file, output_dir)
            
            if files_created:
                self.status_var.set(f"Completed: Created {len(files_created)} files")
                messagebox.showinfo("Success", f"Successfully extracted {len(files_created)} files to {output_dir}")
            else:
                self.status_var.set("No files created")
                messagebox.showwarning("Warning", "No files were created. Check if the HTML structure matches the expected pattern.")
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = HTMLExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
