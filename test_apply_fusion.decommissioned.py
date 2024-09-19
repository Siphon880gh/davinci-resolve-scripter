# Decommissioned: Decommission fusion loading because free API does not support loading fusion settings, however DaVinci console supports it

import sys
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples')

from python_get_resolve import GetResolve
resolve = app.GetResolve()

# Function to add Fusion composition to a clip if it doesn't have one
def ensure_fusion_clip(clip):
    if clip.GetFusionCompCount() == 0:
        clip.AddFusionComp()
        print(f"Added Fusion composition to clip: {clip.GetName()}")
    else:
        print(f"Clip already has a Fusion composition: {clip.GetName()}")

def apply_fusion_script_to_clip(clip, fusion_comp, script_path):
    try:
        # Load the setting file into the Fusion composition
        # fusion_comp.ImportFusionComp(script_path)
        clip.ImportFusionComp(script_path)
        print(f"Successfully applied Fusion setting from {script_path}")
    except Exception as e:
        print(f"Error applying Fusion setting: {e}")

    # try:
    #     # Load the setting file into the Fusion composition
    #     fusion_comp.Load(script_path)
    #     print(f"Successfully applied Fusion setting from {script_path}")
    # except Exception as e:
    #     print(f"Error applying Fusion setting: {e}")

    # with open(script_path, 'r') as script_file:
    #     fusion_script = script_file.read()
    #     # print(fusion_script)
    # # This is where you can apply the script to the composition
    # fusion_comp.Execute(fusion_script)

project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

video_track = 1  # Assuming video track 1 contains the Fusion clips
clips = timeline.GetItemsInTrack('video', video_track)

script_path = "/Users/wengffung/dev/web/temp-vid/fusion_compiled/tlc.setting"  # Path to your Fusion script

for clip_id, clip in clips.items():
    # Check if the clip has a Fusion composition
    ensure_fusion_clip(clip)
    if clip.GetFusionCompCount() > 0: # Each clip has 0 or 1 fusion clip
        for comp_index in range(clip.GetFusionCompCount()):
            fusion_comp = clip.GetFusionCompByIndex(comp_index)
            # apply_fusion_script_to_clip(fusion_comp, script_path)
            # apply_fusion_script_to_clip(fusion_comp, "/Users/wengffung/dev/web/temp-vid/fusion_compiled/exported.comp")
            apply_fusion_script_to_clip(clip, fusion_comp, "/Users/wengffung/dev/web/temp-vid/fusion_compiled/exported.comp")
            # print(fusion_comp)
    

