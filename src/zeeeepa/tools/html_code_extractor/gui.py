#!/usr/bin/env python3
"""GUI for HTML Code Extractor."""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional

from zeeeepa.tools.html_code_extractor.extractor import (
    HTMLParsingError,
    FileCreationError,
    extract_code_from_html,
    preview_code_from_html,
)


class HTMLExtractorGUI:
    """GUI for HTML Code Extractor."""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI.

        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("HTML Code Extractor")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        # Set up the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # File selection
        self.file_frame = ttk.LabelFrame(self.main_frame, text="HTML File", padding="10")
        self.file_frame.pack(fill=tk.X, pady=5)

        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path, width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.browse_button = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.RIGHT)

        # Output directory
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Output Directory", padding="10")
        self.output_frame.pack(fill=tk.X, pady=5)

        self.output_dir = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "Desktop", "WEB-CODES")
        )
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_dir, width=50)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.browse_output_button = ttk.Button(
            self.output_frame, text="Browse", command=self.browse_output_dir
        )
        self.browse_output_button.pack(side=tk.RIGHT)

        # Advanced options
        self.advanced_frame = ttk.LabelFrame(self.main_frame, text="Advanced Options", padding="10")
        self.advanced_frame.pack(fill=tk.X, pady=5)

        # File path class
        ttk.Label(self.advanced_frame, text="File Path Class:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=2
        )
        self.file_path_class = tk.StringVar(value="text-sm text-zinc-400 mb-2 font-mono")
        ttk.Entry(self.advanced_frame, textvariable=self.file_path_class, width=40).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=2
        )

        # Code table class
        ttk.Label(self.advanced_frame, text="Code Table Class:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2
        )
        self.code_table_class = tk.StringVar(value="syntax-highlight")
        ttk.Entry(self.advanced_frame, textvariable=self.code_table_class, width=40).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=2
        )

        # Code line class
        ttk.Label(self.advanced_frame, text="Code Line Class:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=2
        )
        self.code_line_class = tk.StringVar(value="line added")
        ttk.Entry(self.advanced_frame, textvariable=self.code_line_class, width=40).grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=2
        )

        # Encoding
        ttk.Label(self.advanced_frame, text="Encoding:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=2
        )
        self.encoding = tk.StringVar(value="utf-8")
        ttk.Entry(self.advanced_frame, textvariable=self.encoding, width=40).grid(
            row=3, column=1, sticky=tk.W, padx=5, pady=2
        )

        # Status
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="10")
        self.status_frame.pack(fill=tk.X, pady=5)

        self.status_text = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_text)
        self.status_label.pack(fill=tk.X)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.preview_button = ttk.Button(
            self.button_frame, text="Preview", command=self.preview_files
        )
        self.preview_button.pack(side=tk.LEFT, padx=5)

        self.extract_button = ttk.Button(
            self.button_frame, text="Extract", command=self.extract_files
        )
        self.extract_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = ttk.Button(self.button_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=5)

        # Preview window
        self.preview_window: Optional[tk.Toplevel] = None
        self.preview_tree: Optional[ttk.Treeview] = None

    def browse_file(self) -> None:
        """Open a file dialog to select an HTML file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("HTML files", "*.html;*.htm"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)

    def browse_output_dir(self) -> None:
        """Open a directory dialog to select an output directory."""
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir.set(output_dir)

    def update_progress(self, value: float) -> None:
        """Update the progress bar.

        Args:
            value: Progress value (0-100)
        """
        self.progress_var.set(value)
        self.root.update_idletasks()

    def extract_files(self) -> None:
        """Extract code blocks from the HTML file."""
        # Disable buttons during extraction
        self.extract_button.config(state=tk.DISABLED)
        self.preview_button.config(state=tk.DISABLED)

        # Reset progress bar
        self.progress_var.set(0)

        # Get input values
        html_file_path = self.file_path.get()
        output_dir = self.output_dir.get()
        selectors = {
            "file_path_class": self.file_path_class.get(),
            "code_table_class": self.code_table_class.get(),
            "code_line_class": self.code_line_class.get(),
        }
        encoding = self.encoding.get()

        # Validate input
        if not html_file_path:
            messagebox.showerror("Error", "Please select an HTML file")
            self.extract_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)
            return

        if not os.path.exists(html_file_path):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file_path}")
            self.extract_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)
            return

        # Update status
        self.status_text.set("Extracting code...")

        # Run extraction in a separate thread
        threading.Thread(
            target=self._extract_files_thread,
            args=(html_file_path, output_dir, selectors, encoding),
            daemon=True,
        ).start()

    def _extract_files_thread(
        self, html_file_path: str, output_dir: str, selectors: Dict[str, str], encoding: str
    ) -> None:
        """Extract code blocks from the HTML file in a separate thread.

        Args:
            html_file_path: Path to the HTML file
            output_dir: Directory to save extracted files
            selectors: Dictionary of CSS selectors for finding elements
            encoding: File encoding
        """
        try:
            files_created = extract_code_from_html(
                html_file_path=html_file_path,
                output_dir=output_dir,
                selectors=selectors,
                encoding=encoding,
                progress_callback=self.update_progress,
            )

            # Update status
            if files_created:
                self.status_text.set(f"Successfully extracted {len(files_created)} files")
                messagebox.showinfo(
                    "Success",
                    f"Successfully extracted {len(files_created)} files to {output_dir}",
                )
            else:
                self.status_text.set("No files were created")
                messagebox.showwarning(
                    "Warning",
                    "No files were created. Check if the HTML structure matches the expected pattern.",
                )
        except (FileNotFoundError, HTMLParsingError, FileCreationError) as e:
            self.status_text.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_text.set(f"Unexpected error: {str(e)}")
            messagebox.showerror("Unexpected Error", str(e))
        finally:
            # Re-enable buttons
            self.extract_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)

    def preview_files(self) -> None:
        """Preview code blocks from the HTML file."""
        # Disable buttons during preview
        self.extract_button.config(state=tk.DISABLED)
        self.preview_button.config(state=tk.DISABLED)

        # Reset progress bar
        self.progress_var.set(0)

        # Get input values
        html_file_path = self.file_path.get()
        selectors = {
            "file_path_class": self.file_path_class.get(),
            "code_table_class": self.code_table_class.get(),
            "code_line_class": self.code_line_class.get(),
        }
        encoding = self.encoding.get()

        # Validate input
        if not html_file_path:
            messagebox.showerror("Error", "Please select an HTML file")
            self.extract_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)
            return

        if not os.path.exists(html_file_path):
            messagebox.showerror("Error", f"HTML file does not exist: {html_file_path}")
            self.extract_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)
            return

        # Update status
        self.status_text.set("Previewing code...")

        # Run preview in a separate thread
        threading.Thread(
            target=self._preview_files_thread,
            args=(html_file_path, selectors, encoding),
            daemon=True,
        ).start()

    def _preview_files_thread(
        self, html_file_path: str, selectors: Dict[str, str], encoding: str
    ) -> None:
        """Preview code blocks from the HTML file in a separate thread.

        Args:
            html_file_path: Path to the HTML file
            selectors: Dictionary of CSS selectors for finding elements
            encoding: File encoding
        """
        try:
            code_blocks = preview_code_from_html(
                html_file_path=html_file_path,
                selectors=selectors,
                encoding=encoding,
            )

            # Update status
            if code_blocks:
                self.status_text.set(f"Found {len(code_blocks)} files")
                self.root.after(0, lambda: self._show_preview_window(code_blocks))
            else:
                self.status_text.set("No files were found")
                messagebox.showwarning(
                    "Warning",
                    "No files were found. Check if the HTML structure matches the expected pattern.",
                )
        except (FileNotFoundError, HTMLParsingError) as e:
            self.status_text.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            self.status_text.set(f"Unexpected error: {str(e)}")
            messagebox.showerror("Unexpected Error", str(e))
        finally:
            # Re-enable buttons
            self.extract_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)

    def _show_preview_window(self, code_blocks: Dict[str, List[str]]) -> None:
        """Show a preview window with the extracted code blocks.

        Args:
            code_blocks: Dictionary of file paths and code lines
        """
        # Close existing preview window if it exists
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()

        # Create a new preview window
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Preview")
        self.preview_window.geometry("800x600")
        self.preview_window.minsize(600, 400)

        # Create a frame for the preview
        preview_frame = ttk.Frame(self.preview_window, padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)

        # Create a treeview for the file list
        file_frame = ttk.Frame(preview_frame)
        file_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

        ttk.Label(file_frame, text="Files:").pack(anchor=tk.W)

        self.preview_tree = ttk.Treeview(file_frame, show="tree")
        self.preview_tree.pack(fill=tk.BOTH, expand=True)

        # Create a text widget for the code preview
        code_frame = ttk.Frame(preview_frame)
        code_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(code_frame, text="Code:").pack(anchor=tk.W)

        code_text = tk.Text(code_frame, wrap=tk.NONE)
        code_text.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar for the code text
        code_scrollbar = ttk.Scrollbar(code_text, orient=tk.VERTICAL, command=code_text.yview)
        code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        code_text.config(yscrollcommand=code_scrollbar.set)

        # Add a horizontal scrollbar for the code text
        code_hscrollbar = ttk.Scrollbar(code_frame, orient=tk.HORIZONTAL, command=code_text.xview)
        code_hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        code_text.config(xscrollcommand=code_hscrollbar.set)

        # Populate the treeview with file paths
        for file_path in sorted(code_blocks.keys()):
            self.preview_tree.insert("", tk.END, text=file_path, values=(file_path,))

        # Add a callback for selecting a file
        def on_file_select(event: tk.Event) -> None:
            """Handle file selection event.

            Args:
                event: Tkinter event
            """
            selected_item = self.preview_tree.selection()
            if selected_item:
                file_path = self.preview_tree.item(selected_item[0], "text")
                code_lines = code_blocks.get(file_path, [])
                code_text.delete(1.0, tk.END)
                code_text.insert(tk.END, "\n".join(code_lines))

        self.preview_tree.bind("<<TreeviewSelect>>", on_file_select)

        # Select the first file by default
        if code_blocks:
            first_item = self.preview_tree.get_children()[0]
            self.preview_tree.selection_set(first_item)
            self.preview_tree.event_generate("<<TreeviewSelect>>")


def main() -> int:
    """Run the HTML Code Extractor GUI.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    root = tk.Tk()
    HTMLExtractorGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
