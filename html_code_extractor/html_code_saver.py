#!/usr/bin/env python3
import os
import re
import sys
import json
import shutil
import logging
import datetime
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from bs4 import BeautifulSoup
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HTMLCodeSaver:
    """
    A class for saving HTML files in a format optimized for later code extraction.
    This creates a self-contained archive with the HTML file and any necessary metadata.
    """
    
    def __init__(self, html_file_path=None, save_dir=None):
        """
        Initialize the HTML code saver.
        
        Args:
            html_file_path (str, optional): Path to the HTML file
            save_dir (str, optional): Directory to save the archive
        """
        self.html_file_path = html_file_path
        self.save_dir = save_dir or os.path.join(os.path.expanduser("~"), "Desktop", "HTML-ARCHIVES")
        
        # Create save directory if it doesn't exist
        os.makedirs(self.save_dir, exist_ok=True)
    
    def save_html_archive(self, html_file_path=None, archive_name=None):
        """
        Save the HTML file and metadata as an archive for later extraction.
        
        Args:
            html_file_path (str, optional): Path to the HTML file
            archive_name (str, optional): Name for the archive
            
        Returns:
            str: Path to the created archive
        """
        html_file_path = html_file_path or self.html_file_path
        
        if not html_file_path:
            logger.error("No HTML file specified")
            return None
        
        try:
            # Read HTML file
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
                return None
        except Exception as e:
            logger.error(f"Error reading HTML file: {e}")
            return None
        
        # Parse HTML to extract metadata
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title from HTML if available
        title = soup.title.string if soup.title else os.path.basename(html_file_path)
        
        # Create timestamp for the archive
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create archive name if not provided
        if not archive_name:
            base_name = os.path.splitext(os.path.basename(html_file_path))[0]
            archive_name = f"{base_name}_{timestamp}"
        
        # Create archive directory
        archive_dir = os.path.join(self.save_dir, archive_name)
        os.makedirs(archive_dir, exist_ok=True)
        
        # Copy HTML file to archive
        html_dest = os.path.join(archive_dir, os.path.basename(html_file_path))
        shutil.copy2(html_file_path, html_dest)
        
        # Create metadata file
        metadata = {
            "original_file": html_file_path,
            "title": title,
            "date_saved": timestamp,
            "file_size": os.path.getsize(html_file_path),
            "encoding": "utf-8",  # Default, may be overridden
            "selectors": {
                "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
                "code_table_class": "syntax-highlight",
                "code_line_class": "line added"
            }
        }
        
        # Save metadata
        metadata_path = os.path.join(archive_dir, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        # Create preview of code files that will be extracted
        preview = self._generate_preview(html_content)
        preview_path = os.path.join(archive_dir, "preview.txt")
        with open(preview_path, 'w', encoding='utf-8') as f:
            f.write(preview)
        
        logger.info(f"Created HTML archive at: {archive_dir}")
        return archive_dir
    
    def _generate_preview(self, html_content):
        """
        Generate a preview of the code files that will be extracted.
        
        Args:
            html_content (str): HTML content
            
        Returns:
            str: Preview text
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all file headers
        file_headers = soup.find_all(class_=re.compile(r"text-sm text-zinc-400 mb-2 font-mono"))
        
        if not file_headers:
            return "No code files found in HTML."
        
        preview_lines = ["Files that will be extracted:", ""]
        
        for header in file_headers:
            # Extract file path
            file_path = header.get_text().strip()
            if file_path.endswith(':'):
                file_path = file_path[:-1]
            
            # Find the next table with code
            table = header.find_next('table', class_='syntax-highlight')
            if table:
                # Count lines of code
                added_lines = table.find_all('tr', class_='line added')
                line_count = len(added_lines)
                preview_lines.append(f"{file_path} ({line_count} lines)")
            else:
                preview_lines.append(f"{file_path} (0 lines)")
        
        return "\n".join(preview_lines)

class HTMLCodeSaverApp:
    """GUI application for the HTML Code Saver."""
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("HTML Code Saver")
        self.root.geometry("700x500")
        
        # Create the HTML Code Saver
        self.saver = HTMLCodeSaver()
        
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
        output_frame = ttk.LabelFrame(main_frame, text="Archive Location", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        self.output_path_var = tk.StringVar(value=self.saver.save_dir)
        ttk.Label(output_frame, text="Archives will be saved to:").pack(anchor=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=50).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir).pack(anchor=tk.E, padx=5, pady=5)
        
        # Create the archive name section
        name_frame = ttk.LabelFrame(main_frame, text="Archive Name", padding="10")
        name_frame.pack(fill=tk.X, pady=10)
        
        self.archive_name_var = tk.StringVar()
        ttk.Label(name_frame, text="Archive name (optional):").pack(anchor=tk.W, pady=5)
        ttk.Entry(name_frame, textvariable=self.archive_name_var, width=50).pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(name_frame, text="If not specified, a name will be generated automatically.").pack(anchor=tk.W, pady=5)
        
        # Create the preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_text.insert(tk.END, "Select an HTML file to see a preview of extractable code files.")
        self.preview_text.config(state=tk.DISABLED)
        
        # Create the action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Generate Preview", command=self.generate_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Archive", command=self.save_archive).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Create the status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_file(self):
        """Open file dialog to select HTML file."""
        file_path = filedialog.askopenfilename(
            title="Select HTML File",
            filetypes=[("HTML Files", "*.html;*.htm"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.generate_preview()
    
    def browse_output_dir(self):
        """Open directory dialog to select output directory."""
        dir_path = filedialog.askdirectory(
            title="Select Archive Location"
        )
        if dir_path:
            self.output_path_var.set(dir_path)
            self.saver.save_dir = dir_path
    
    def generate_preview(self):
        """Generate a preview of the code files that will be extracted."""
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
            # Read HTML file
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except UnicodeDecodeError:
            # Try with different encoding if utf-8 fails
            try:
                with open(html_file, 'r', encoding='latin-1') as file:
                    html_content = file.read()
            except Exception as e:
                self.status_var.set("Error reading file")
                messagebox.showerror("Error", f"Error reading HTML file: {str(e)}")
                return
        except Exception as e:
            self.status_var.set("Error reading file")
            messagebox.showerror("Error", f"Error reading HTML file: {str(e)}")
            return
        
        # Generate preview
        preview = self.saver._generate_preview(html_content)
        
        # Update preview text
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        self.preview_text.config(state=tk.DISABLED)
        
        self.status_var.set("Preview generated")
    
    def save_archive(self):
        """Save the HTML file as an archive."""
        html_file = self.file_path_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file")
            return
        
        if not os.path.exists(html_file):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file}")
            return
        
        # Update status
        self.status_var.set("Saving archive...")
        self.root.update()
        
        # Update saver with current settings
        self.saver.save_dir = self.output_path_var.get()
        
        # Save archive
        try:
            archive_dir = self.saver.save_html_archive(
                html_file_path=html_file,
                archive_name=self.archive_name_var.get() or None
            )
            
            if archive_dir:
                self.status_var.set(f"Archive saved to: {archive_dir}")
                messagebox.showinfo("Success", f"HTML archive saved to:\n{archive_dir}")
            else:
                self.status_var.set("Failed to save archive")
                messagebox.showerror("Error", "Failed to save HTML archive")
        except Exception as e:
            self.status_var.set("Error saving archive")
            messagebox.showerror("Error", f"Error saving HTML archive: {str(e)}")

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = HTMLCodeSaverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
