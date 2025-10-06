#!/usr/bin/env python3
"""
PDF Splitter Script

This script splits a large PDF file into smaller chunks to avoid rate limiting issues
when uploading to LibreChat with Azure OpenAI embeddings.

Usage:
    python split_pdf.py input.pdf --pages-per-chunk 50 --output-dir split_pdfs
"""

import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_path, pages_per_chunk=50, output_dir="split_pdfs"):
    """
    Split a PDF into smaller chunks.
    
    Args:
        input_path (str): Path to the input PDF file
        pages_per_chunk (int): Number of pages per output PDF
        output_dir (str): Directory to save the output PDFs
    
    Returns:
        list: List of paths to the output PDF files
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get the base filename without extension
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    
    # Read the input PDF
    pdf = PdfReader(input_path)
    total_pages = len(pdf.pages)
    
    output_files = []
    
    # Split the PDF into chunks
    for i in range(0, total_pages, pages_per_chunk):
        output = PdfWriter()
        
        # Add pages to the output PDF
        end_page = min(i + pages_per_chunk, total_pages)
        for page_num in range(i, end_page):
            output.add_page(pdf.pages[page_num])
        
        # Save the output PDF
        output_path = os.path.join(output_dir, f"{base_filename}_part_{i//pages_per_chunk+1}.pdf")
        with open(output_path, "wb") as output_file:
            output.write(output_file)
        
        output_files.append(output_path)
        print(f"Created {output_path} with pages {i+1}-{end_page}")
    
    return output_files

def main():
    parser = argparse.ArgumentParser(description="Split a large PDF file into smaller chunks")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("--pages-per-chunk", type=int, default=50, 
                        help="Number of pages per output PDF (default: 50)")
    parser.add_argument("--output-dir", default="split_pdfs", 
                        help="Directory to save the output PDFs (default: 'split_pdfs')")
    
    args = parser.parse_args()
    
    output_files = split_pdf(args.input_pdf, args.pages_per_chunk, args.output_dir)
    
    print(f"\nSplit {args.input_pdf} into {len(output_files)} smaller PDFs in the '{args.output_dir}' directory.")
    print("You can now upload these smaller PDFs to LibreChat one at a time.")

if __name__ == "__main__":
    main()
