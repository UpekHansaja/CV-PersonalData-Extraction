#!/usr/bin/env python3
"""
Example usage script for CV Extractor
Shows different ways to use the CV extraction system
"""

from cv_extractor import CVExtractor
import os
from pathlib import Path

def example_1_interactive():
    """Example 1: Interactive mode - prompts for input"""
    print("\n" + "="*60)
    print("Example 1: Interactive Mode")
    print("="*60)
    
    cv_folder = input("Enter CV folder path: ").strip()
    output_file = input("Enter output CSV path (default: ./data.csv): ").strip() or "./data.csv"
    
    extractor = CVExtractor()
    results = extractor.process_cv_folder(cv_folder)
    
    if results:
        extractor.save_to_csv(output_file)
        print(f"\n✓ Extracted {len(results)} CVs")
        print(f"✓ Saved to {output_file}")


def example_2_programmatic():
    """Example 2: Programmatic usage with custom processing"""
    print("\n" + "="*60)
    print("Example 2: Programmatic Mode")
    print("="*60)
    
    # Initialize extractor
    extractor = CVExtractor()
    
    # Process a specific folder
    cv_folder = "./sample_cvs"  # Adjust this path
    
    if not Path(cv_folder).exists():
        print(f"Sample folder '{cv_folder}' not found. Skipping this example.")
        return
    
    results = extractor.process_cv_folder(cv_folder)
    
    # Print sample results
    if results:
        print(f"\nExtracted {len(results)} CVs:")
        for i, result in enumerate(results[:3], 1):  # Show first 3
            print(f"\n{i}. {result.get('filename', 'Unknown')}")
            print(f"   Name: {result.get('name', 'N/A')}")
            print(f"   Email: {result.get('email', 'N/A')}")
            print(f"   Phone: {result.get('phone', 'N/A')}")
            print(f"   Company: {result.get('current_company', 'N/A')}")
        
        # Save all results
        extractor.save_to_csv("./results.csv")
        print(f"\n✓ All results saved to results.csv")


def example_3_with_env():
    """Example 3: Using environment variables"""
    print("\n" + "="*60)
    print("Example 3: Environment Variable Mode")
    print("="*60)
    
    # Check if environment variables are set
    cv_folder = os.getenv('CV_FOLDER_PATH')
    output_csv = os.getenv('OUTPUT_CSV_PATH', './extracted_data.csv')
    
    if not cv_folder:
        print("CV_FOLDER_PATH environment variable not set")
        print("Set it with: export CV_FOLDER_PATH=/path/to/cvs")
        return
    
    extractor = CVExtractor()
    results = extractor.process_cv_folder(cv_folder)
    
    if results:
        extractor.save_to_csv(output_csv)
        print(f"\n✓ Extracted {len(results)} CVs from {cv_folder}")
        print(f"✓ Saved to {output_csv}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CV Personal Data Extraction - Usage Examples")
    print("="*60)
    
    print("\nChoose an example to run:")
    print("1. Interactive mode (prompt for folder path)")
    print("2. Programmatic mode (process sample folder)")
    print("3. Environment variable mode")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-3): ").strip()
    
    try:
        if choice == "1":
            example_1_interactive()
        elif choice == "2":
            example_2_programmatic()
        elif choice == "3":
            example_3_with_env()
        elif choice == "0":
            print("Exiting...")
        else:
            print("Invalid choice")
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
