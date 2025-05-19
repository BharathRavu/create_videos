#!/usr/bin/env python3
"""
pptx_to_png.py - Convert PowerPoint presentations to PNG images on Ubuntu

This module provides functionality to convert PPTX files to PNG images
using LibreOffice for the initial conversion to PDF and pdf2image for 
generating the final PNG images.

Usage:
    python pptx_to_png.py <pptx_path> <output_folder>
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pdf2image import convert_from_path


def convert_pptx_to_pdf(pptx_path, output_dir):
    """
    Convert a PPTX file to PDF using LibreOffice in headless mode.
    
    Args:
        pptx_path (str): Path to the PPTX file
        output_dir (str): Directory to save the PDF
        
    Returns:
        str: Path to the generated PDF file
    """
    # Get the filename without extension
    base_name = os.path.splitext(os.path.basename(pptx_path))[0]
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert PPTX to PDF using LibreOffice
    cmd = [
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", output_dir, pptx_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not os.path.exists(pdf_path):
            raise Exception("PDF conversion failed")
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"Error during LibreOffice conversion: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


def convert_pdf_to_png(pdf_path, output_dir, dpi=300):
    """
    Convert a PDF file to PNG images.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the PNG images
        dpi (int): DPI resolution for the PNG images
        
    Returns:
        list: Paths to the generated PNG images
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)
        
        # Save images
        image_paths = []
        for i, image in enumerate(images):
            output_path = os.path.join(output_dir, f"slide_{i+1:03d}.png")
            image.save(output_path, "PNG")
            image_paths.append(output_path)
        
        return image_paths
    except Exception as e:
        print(f"Error converting PDF to PNG: {e}")
        raise


def pptx_to_png(pptx_path, output_dir, keep_pdf=False, dpi=300):
    """
    Convert a PPTX file to PNG images.
    
    Args:
        pptx_path (str): Path to the PPTX file
        output_dir (str): Directory to save the PNG images
        keep_pdf (bool): Whether to keep the intermediate PDF file
        dpi (int): DPI resolution for the PNG images
        
    Returns:
        list: Paths to the generated PNG images
    """
    # Create a temporary directory for the PDF if not keeping it
    if keep_pdf:
        pdf_dir = output_dir
    else:
        pdf_dir = tempfile.mkdtemp()
    
    try:
        # Convert PPTX to PDF
        pdf_path = convert_pptx_to_pdf(pptx_path, pdf_dir)
        
        # Convert PDF to PNG
        image_paths = convert_pdf_to_png(pdf_path, output_dir, dpi)
        
        return image_paths
    finally:
        # Clean up the temporary directory if we created one
        if not keep_pdf and pdf_dir != output_dir:
            shutil.rmtree(pdf_dir, ignore_errors=True)


def main():
    """Main function to handle command-line usage."""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <pptx_path> <output_folder>")
        sys.exit(1)
    
    pptx_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(pptx_path):
        print(f"Error: File not found: {pptx_path}")
        sys.exit(1)
    
    # Check if input file is a PPTX file
    if not pptx_path.lower().endswith('.pptx'):
        print(f"Error: Input file must be a .pptx file: {pptx_path}")
        sys.exit(1)
    
    try:
        image_paths = pptx_to_png(pptx_path, output_dir)
        print(f"Successfully converted presentation to {len(image_paths)} PNG images.")
        print(f"Images saved in: {output_dir}")
    except Exception as e:
        print(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
