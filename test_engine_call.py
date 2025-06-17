# test_engine_call.py
# Located at fastbackfilter-1.3.2/fastbackfilter/engines/test_harness/test_engine_call.py

import sys
import os
import time
import importlib # Added for importlib.import_module

# --- Path Configuration ---
# Get the absolute path of the current script's directory.
# This script is now at fastbackfilter-1.3.2/fastbackfilter/engines/test_harness
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the 'engines' directory (parent of test_harness)
engines_dir = os.path.dirname(current_script_dir)

# Navigate up one more level to the 'fastbackfilter' directory.
# This is the root of your package and needs to be in sys.path for relative imports to work.
package_root_dir = os.path.dirname(engines_dir)

# Add the 'fastbackfilter' directory to Python's system path.
# This tells Python that 'fastbackfilter' is a package it can import from.
if package_root_dir not in sys.path:
    sys.path.insert(0, package_root_dir) # Insert at the beginning to prioritize

# --- Diagnostic Check for __init__.py and core modules ---
# This is crucial for Python to recognize directories as packages and find dependencies.
print("\n--- Performing Package Structure and Core Dependency Check ---")
fastbackfilter_init = os.path.join(package_root_dir, '__init__.py')
engines_init = os.path.join(engines_dir, '__init__.py')

# CORRECTED PATHS for types.py and registry.py
# They should be directly under the 'fastbackfilter' package root directory
types_module_path = os.path.join(package_root_dir, 'types.py')
registry_module_path = os.path.join(package_root_dir, 'registry.py')


if not os.path.exists(fastbackfilter_init):
    print(f"WARNING: Missing '{fastbackfilter_init}'. The 'fastbackfilter' directory might not be recognized as a Python package.")
    print("ACTION: Please create an empty file named '__init__.py' inside the 'fastbackfilter' directory.")
else:
    print(f"'{fastbackfilter_init}' found.")

if not os.path.exists(engines_init):
    print(f"WARNING: Missing '{engines_init}'. The 'fastbackfilter.engines' directory might not be recognized as a Python subpackage.")
    print("ACTION: Please create an empty file named '__init__.py' inside the 'fastbackfilter/engines' directory.")
else:
    print(f"'{engines_init}' found.")

if not os.path.exists(types_module_path):
    print(f"WARNING: Missing core module '{types_module_path}'. Many engines rely on 'fastbackfilter.types'.")
    print("ACTION: Please ensure 'types.py' exists directly inside the 'fastbackfilter' directory.")
else:
    print(f"'{types_module_path}' found.")
    # Attempt to import types to catch syntax errors early
    try:
        importlib.import_module('fastbackfilter.types')
        print(f"Successfully imported 'fastbackfilter.types'.")
    except Exception as e:
        print(f"ERROR: Failed to import 'fastbackfilter.types': {e}. Please check for syntax errors in 'types.py'.")

if not os.path.exists(registry_module_path):
    print(f"WARNING: Missing core module '{registry_module_path}'. Some engines might rely on 'fastbackfilter.registry'.")
    print("ACTION: Please ensure 'registry.py' exists directly inside the 'fastbackfilter' directory.")
else:
    print(f"'{registry_module_path}' found.")
    # Attempt to import registry to catch syntax errors early
    try:
        importlib.import_module('fastbackfilter.registry')
        print(f"Successfully imported 'fastbackfilter.registry'.")
    except Exception as e:
        print(f"ERROR: Failed to import 'fastbackfilter.registry': {e}. Please check for syntax errors in 'registry.py'.")

print("--- End of Package Structure and Core Dependency Check ---\n")


# --- Engine Loading and Calling ---
# Define a list of engine module names to attempt to load and call.
# These are now treated as submodules of fastbackfilter.engines
engine_submodule_names = [
    "base", "bat", "csv", "exe", "fallback", "gzip", "html", "image",
    "json", "legacy_office", "mp3", "mp4", "pdf", "png", "sh", "tar",
    "text", "wav", "xml", "zip_office"
]

# A dictionary to store successfully loaded engine modules
loaded_engines = {}

print(f"Attempting to load engine modules from package 'fastbackfilter.engines'.")

for submodule_name in engine_submodule_names:
    # Construct the full package path for the module
    full_module_path = f"fastbackfilter.engines.{submodule_name}"
    try:
        # Use importlib.import_module for a cleaner and more reliable dynamic import
        # This will return the actual submodule object (e.g., fastbackfilter.engines.base)
        module = importlib.import_module(full_module_path)
        loaded_engines[submodule_name] = module # Store the module directly
        print(f"Successfully loaded engine module: {full_module_path}")
    except ImportError as e:
        print(f"ERROR: Could not load engine module '{full_module_path}': {e}.")
        print(f"  Check if '{submodule_name}.py' exists in '{engines_dir}', has no syntax errors,")
        print(f"  and verify all its internal imports (e.g., from ..types, from .base) are resolvable.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while loading '{full_module_path}': {e}")
        print(f"  This might indicate a runtime error or a deeper issue within {submodule_name}.py.")

# --- Test Data (replace with your actual test files) ---
# Create some mock content for demonstration purposes.
mock_file_path = "/tmp/mock_test_file.txt" # A placeholder path for process_file
mock_file_content = b"This is some general sample content for testing the file content detection engines."
mock_bat_content = b"@echo off\nrem This is a batch script example.\nECHO Hello World!"
mock_image_content = b"GIF89a\x01\x00\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;" # Very small GIF
mock_html_content = b"<!DOCTYPE html><html><body><h1>Test HTML</h1><p>This is some HTML content.</p></body></html>"
mock_json_content = b'{"name": "test", "value": 123}'
mock_csv_content = b"header1,header2,header3\nvalue1,value2,value3\nanother1,another2,another3"
mock_sh_content = b"#!/bin/bash\n# This is a shell script example\necho 'Hello from shell script!'"
mock_xml_content = b"<?xml version='1.0' encoding='UTF-8'?><root><item id='1'>data</item></root>"
mock_empty_content = b""

# A dictionary to map engine names to appropriate mock content for 'sniff' or 'process_content'
mock_content_map = {
    "base": mock_file_content,
    "bat": mock_bat_content,
    "csv": mock_csv_content,
    "exe": b"\x4D\x5A\x90\x00\x03\x00\x00\x00", # MZ header for exe
    "fallback": mock_file_content,
    "gzip": b"\x1f\x8b\x08\x00\x00\x00\x00\x00", # GZIP magic numbers
    "html": mock_html_content,
    "image": mock_image_content,
    "json": mock_json_content,
    "legacy_office": b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1", # OLE compound file header (start of DOC/XLS)
    "mp3": b"\xFF\xFB\x90\x00", # Common start of an MP3 frame
    "mp4": b"\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6F\x6D\x00\x00\x00\x00", # FTYP box for MP4
    "pdf": b"%PDF-1.4\n1 0 obj<<>>endobj", # Basic PDF header
    "png": b"\x89PNG\r\n\x1a\n", # PNG magic number
    "sh": mock_sh_content,
    "tar": b"ustar\x0000", # TAR magic string
    "text": mock_file_content,
    "wav": b"RIFF\x00\x00\x00\x00WAVEfmt ", # WAV header
    "xml": mock_xml_content,
    "zip_office": b"PK\x03\x04\x14\x00\x06\x00" # ZIP magic number (for .docx, .xlsx, etc.)
}


# --- Engine Calling Logic ---
print("\n--- Calling Loaded Engines ---")

# Ensure EngineBase is loaded to check subclasses
EngineBaseClass = None
if 'base' in loaded_engines:
    EngineBaseClass = getattr(loaded_engines['base'], 'EngineBase', None)
    if not EngineBaseClass:
        print("ERROR: 'base' module loaded but 'EngineBase' class not found within it. Cannot test other engines that subclass EngineBase.")
else:
    print("ERROR: 'base' module not loaded. Cannot test other engines that subclass EngineBase.")

if not loaded_engines:
    print("No engines were successfully loaded. Cannot proceed with calling.")
else:
    for name, engine_module in loaded_engines.items():
        print(f"\n--- Testing Engine: {name} ---")
        try:
            # Dynamically find the engine class within the module that subclasses EngineBase
            # This handles cases like bat.py having BATEngine(EngineBase)
            current_engine_class = None
            if EngineBaseClass:
                for attr_name in dir(engine_module):
                    attr = getattr(engine_module, attr_name)
                    # Check if it's a class, a subclass of EngineBase, and not EngineBase itself
                    if isinstance(attr, type) and issubclass(attr, EngineBaseClass) and attr is not EngineBaseClass:
                        current_engine_class = attr
                        break # Found the actual engine class (e.g., BATEngine, CSVEngine)

            if current_engine_class:
                start_time = time.time()
                engine_instance = current_engine_class()
                init_time = time.time() - start_time
                print(f"  {name} Engine instance ('{current_engine_class.__name__}') initialized in {init_time:.4f} seconds.")

                call_start_time = time.time()
                # Get specific mock content for the engine, or fallback to general text
                content_to_pass = mock_content_map.get(name, mock_file_content)
                if not content_to_pass: # Fallback if content map entry is empty
                    print(f"  Warning: No specific mock content for {name} found, using general text.")
                    content_to_pass = mock_file_content
                
                # Assume engines implementing EngineBase are callable and expect payload: bytes
                if callable(engine_instance):
                    result = engine_instance(content_to_pass) # Calls the __call__ method
                    call_elapsed_time = time.time() - call_start_time
                    print(f"  {name} Engine result: {result}")
                    print(f"  {name} Engine processing elapsed: {call_elapsed_time:.4f} seconds.")
                else:
                    print(f"  Warning: {name} Engine instance ('{current_engine_class.__name__}') is not callable. Check its inheritance from EngineBase and __call__ implementation.")
                    result = {"status": "skipped", "reason": "Engine instance not callable."}

            # If no suitable EngineBase subclass found, check for a standalone 'detect_content' function
            elif hasattr(engine_module, 'detect_content'):
                call_start_time = time.time()
                content_to_pass = mock_content_map.get(name, mock_file_content)
                if not content_to_pass:
                     content_to_pass = mock_file_content
                result = engine_module.detect_content(content_to_pass)
                call_elapsed_time = time.time() - call_start_time
                print(f"  {name} (detect_content) result: {result}")
                print(f"  {name} (detect_content) elapsed: {call_elapsed_time:.4f} seconds.")
            else:
                print(f"  {name} module has no suitable EngineBase subclass (inheriting from fastbackfilter.engines.base.EngineBase) nor a 'detect_content' function.")

        except Exception as e:
            print(f"  ERROR: Error calling engine '{name}': {e}")
            print(f"  ACTION: Please check the implementation of {name}.py and its expected API, and ensure it correctly inherits from fastbackfilter.engines.base.EngineBase.")

print("\nScript finished.")
