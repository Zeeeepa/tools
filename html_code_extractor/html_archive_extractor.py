#!/usr/bin/env python3
import os
import re
import sys
import json
import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from bs4 import BeautifulSoup
from pathlib import Path

# Import the HTML extractor functionality
from html_extractor import extract_code_from_html

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HTMLArchiveExtractor:
    """
    A class for extracting code from HTML archives created by the HTML Code Saver.
    """
    
    def __init__(self, archive_dir=None, output_dir=None):
        """
        Initialize the HTML archive extractor.
        
        Args:
            archive_dir (str, optional): Path to the HTML archive directory
            output_dir (str, optional): Directory to save extracted files
        """
        self.archive_dir = archive_dir
        self.output_dir = output_dir or os.path.join(os.path.expanduser("~"), "Desktop", "WEB-CODES")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def extract_from_archive(self, archive_dir=None):
        """
        Extract code from an HTML archive.
        
        Args:
            archive_dir (str, optional): Path to the HTML archive directory
            
        Returns:
            list: List of created file paths
        """
        archive_dir = archive_dir or self.archive_dir
        
        if not archive_dir:
            logger.error("No archive directory specified")
            return []
        
        if not os.path.isdir(archive_dir):
            logger.error(f"Archive directory does not exist: {archive_dir}")
            return []
        
        # Load metadata
        metadata_path = os.path.join(archive_dir, "metadata.json")
        if not os.path.exists(metadata_path):
            logger.error(f"Metadata file not found in archive: {metadata_path}")
            return []
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception as e:
            logger.error(f"Error reading metadata file: {e}")
            return []
        
        # Find HTML file in archive
        html_files = [f for f in os.listdir(archive_dir) if f.endswith(('.html', '.htm'))]
        if not html_files:
            logger.error(f"No HTML files found in archive: {archive_dir}")
            return []
        
        html_file_path = os.path.join(archive_dir, html_files[0])
        
        # Extract code from HTML file
        return extract_code_from_html(html_file_path, self.output_dir)
    
    def list_archives(self, archives_dir=None):
        """
        List all available HTML archives.
        
        Args:
            archives_dir (str, optional): Directory containing HTML archives
            
        Returns:
            list: List of archive directories
        """
        archives_dir = archives_dir or os.path.join(os.path.expanduser("~"), "Desktop", "HTML-ARCHIVES")
        
        if not os.path.isdir(archives_dir):
            logger.warning(f"Archives directory does not exist: {archives_dir}")
            return []
        
        # Find all subdirectories that contain metadata.json
        archives = []
        for item in os.listdir(archives_dir):
            item_path = os.path.join(archives_dir, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "metadata.json")):
                archives.append(item_path)
        
        return archives
    
    def get_archive_info(self, archive_dir):
        """
        Get information about an HTML archive.
        
        Args:
            archive_dir (str): Path to the HTML archive directory
            
        Returns:
            dict: Archive information
        """
        if not os.path.isdir(archive_dir):
            logger.error(f"Archive directory does not exist: {archive_dir}")
            return None
        
        # Load metadata
        metadata_path = os.path.join(archive_dir, "metadata.json")
        if not os.path.exists(metadata_path):
            logger.error(f"Metadata file not found in archive: {metadata_path}")
            return None
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception as e:
            logger.error(f"Error reading metadata file: {e}")
            return None
        
        # Load preview
        preview_path = os.path.join(archive_dir, "preview.txt")
        preview = ""
        if os.path.exists(preview_path):
            try:
                with open(preview_path, 'r', encoding='utf-8') as f:
                    preview = f.read()
            except Exception as e:
                logger.warning(f"Error reading preview file: {e}")
        
        # Find HTML file in archive
        html_files = [f for f in os.listdir(archive_dir) if f.endswith(('.html', '.htm'))]
        html_file = html_files[0] if html_files else None
        
        return {
            "name": os.path.basename(archive_dir),
            "path": archive_dir,
            "metadata": metadata,
            "preview": preview,
            "html_file": html_file
        }

class HTMLArchiveExtractorApp:
    """GUI application for the HTML Archive Extractor."""
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("HTML Archive Extractor")
        self.root.geometry("800x600")
        
        # Create the HTML Archive Extractor
        self.extractor = HTMLArchiveExtractor()
        
        # Set up the main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the archives section
        archives_frame = ttk.LabelFrame(main_frame, text="Available Archives", padding="10")
        archives_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a frame for the archive list and buttons
        list_frame = ttk.Frame(archives_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable listbox for archives
        self.archives_listbox = tk.Listbox(list_frame, height=10)
        self.archives_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.archives_listbox.bind('<<ListboxSelect>>', self.on_archive_select)
        
        # Add scrollbar to listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.archives_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.archives_listbox.config(yscrollcommand=scrollbar.set)
        
        # Create buttons for archive actions
        button_frame = ttk.Frame(archives_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Refresh Archives", command=self.refresh_archives).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Browse Archive", command=self.browse_archive).pack(side=tk.LEFT, padx=5)
        
        # Create the archive info section
        info_frame = ttk.LabelFrame(main_frame, text="Archive Information", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create text widget for archive info
        self.info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, height=10)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.info_text.insert(tk.END, "Select an archive to view information.")
        self.info_text.config(state=tk.DISABLED)
        
        # Create the output directory section
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        self.output_path_var = tk.StringVar(value=self.extractor.output_dir)
        ttk.Label(output_frame, text="Files will be extracted to:").pack(anchor=tk.W, pady=5)
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=50).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir).pack(anchor=tk.E, padx=5, pady=5)
        
        # Create the action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Extract Code", command=self.extract_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Create the status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize archive list
        self.archives = []
        self.selected_archive = None
        self.refresh_archives()
    
    def refresh_archives(self):
        """Refresh the list of available archives."""
        self.archives = self.extractor.list_archives()
        
        # Clear listbox
        self.archives_listbox.delete(0, tk.END)
        
        # Add archives to listbox
        for archive in self.archives:
            self.archives_listbox.insert(tk.END, os.path.basename(archive))
        
        self.status_var.set(f"Found {len(self.archives)} archives")
    
    def browse_archive(self):
        """Browse for an HTML archive directory."""
        dir_path = filedialog.askdirectory(
            title="Select HTML Archive Directory",
            initialdir=os.path.join(os.path.expanduser("~"), "Desktop", "HTML-ARCHIVES")
        )
        if dir_path:
            # Check if it's a valid archive
            if os.path.exists(os.path.join(dir_path, "metadata.json")):
                self.archives.append(dir_path)
                self.archives_listbox.insert(tk.END, os.path.basename(dir_path))
                self.archives_listbox.selection_clear(0, tk.END)
                self.archives_listbox.selection_set(tk.END)
                self.archives_listbox.see(tk.END)
                self.on_archive_select(None)
            else:
                messagebox.showerror("Error", f"Not a valid HTML archive: {dir_path}")
    
    def browse_output_dir(self):
        """Browse for an output directory."""
        dir_path = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.extractor.output_dir
        )
        if dir_path:
            self.output_path_var.set(dir_path)
            self.extractor.output_dir = dir_path
    
    def on_archive_select(self, event):
        """Handle archive selection event."""
        selection = self.archives_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < 0 or index >= len(self.archives):
            return
        
        self.selected_archive = self.archives[index]
        self.update_archive_info()
    
    def update_archive_info(self):
        """Update the archive information display."""
        if not self.selected_archive:
            return
        
        archive_info = self.extractor.get_archive_info(self.selected_archive)
        if not archive_info:
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error loading archive information: {self.selected_archive}")
            self.info_text.config(state=tk.DISABLED)
            return
        
        # Format archive info
        info_lines = [
            f"Archive: {archive_info['name']}",
            f"Path: {archive_info['path']}",
            f"HTML File: {archive_info['html_file']}",
            f"Date Saved: {archive_info['metadata'].get('date_saved', 'Unknown')}",
            f"Title: {archive_info['metadata'].get('title', 'Unknown')}",
            f"Original File: {archive_info['metadata'].get('original_file', 'Unknown')}",
            f"File Size: {archive_info['metadata'].get('file_size', 'Unknown')} bytes",
            "",
            "Preview:",
            archive_info['preview'] or "No preview available."
        ]
        
        # Update info text
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "\n".join(info_lines))
        self.info_text.config(state=tk.DISABLED)
    
    def extract_code(self):
        """Extract code from the selected archive."""
        if not self.selected_archive:
            messagebox.showerror("Error", "Please select an archive")
            return
        
        # Update output directory
        self.extractor.output_dir = self.output_path_var.get()
        
        # Update status
        self.status_var.set("Extracting code...")
        self.root.update()
        
        # Extract code
        try:
            files_created = self.extractor.extract_from_archive(self.selected_archive)
            
            if files_created:
                self.status_var.set(f"Extracted {len(files_created)} files")
                messagebox.showinfo("Success", f"Successfully extracted {len(files_created)} files to {self.extractor.output_dir}")
            else:
                self.status_var.set("No files extracted")
                messagebox.showwarning("Warning", "No files were extracted. Check the archive contents.")
        except Exception as e:
            self.status_var.set("Error extracting code")
            messagebox.showerror("Error", f"Error extracting code: {str(e)}")

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = HTMLArchiveExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
