# pip install opentimelineio==0.17.0

import opentimelineio as otio

try:
    timeline = otio.adapters.read_from_file("generated_otio/generated.otio")
    print("OTIO file is valid.")
except Exception as e:
    print(f"Error validating OTIO file: {e}")

