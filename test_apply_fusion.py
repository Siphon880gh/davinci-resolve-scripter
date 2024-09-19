from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fusionscript import Resolve  # ...and/or other types you want
    

import sys
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples')

from python_get_resolve import GetResolve
resolve = app.GetResolve()

def apply_fusion_script_to_clip(fusion_comp, script_path):
    with open(script_path, 'r') as script_file:
        fusion_script = script_file.read()
    # This is where you can apply the script to the composition
    fusion_comp.Execute(fusion_script)

project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

video_track = 1  # Assuming video track 1 contains the Fusion clips
clips = timeline.GetItemsInTrack('video', video_track)

script_path = "/Users/wengffung/dev/web/temp-vid/fusion_compiled/tlc.setting"  # Path to your Fusion script

for clip_id, clip in clips.items():
    # Check if the clip has a Fusion composition
    if clip.GetFusionCompCount() > 0: # Each clip has 0 or 1 fusion clip
        for comp_index in range(clip.GetFusionCompCount()):
            fusion_comp = clip.GetFusionCompByIndex(comp_index)
            apply_fusion_script_to_clip(fusion_comp, script_path)
            # print(fusion_comp)
    

