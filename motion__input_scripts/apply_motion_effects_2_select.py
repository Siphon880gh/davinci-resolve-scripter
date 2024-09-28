import os

try:
  # _ADJUST the abs path to the app, due to limitation of free DaVinci - 1 of 3
  # For example the app is the folder path that contains app.clips.json, README.md, etc.
  APP_CLIPS_JSON_ABS_PATH = "/Users/wengffung/dev/web/davinci/"
  
  # _ADJUST the video track whose clips we are adding motion effects on - 2 of 3
  track = timeline.GetItemsInTrack('video', 1) # type: ignore


  fusion_path = ""
  hinted_fusion_path = os.path.join(APP_CLIPS_JSON_ABS_PATH, "04_motion__input_scripts/") 
  cleaned_fusion_path = os.path.join(APP_CLIPS_JSON_ABS_PATH, "motion__input_scripts/") 
  if os.path.isdir(hinted_fusion_path):
    fusion_path = hinted_fusion_path
  elif os.path.isdir(cleaned_fusion_path):
    fusion_path = cleaned_fusion_path
  else:
    raise Exception("Could not find the folder containing the Fusion comp files. Tried: " + hinted_fusion_path + " and " + cleaned_fusion_path)

  # _ADJUST which clip gets which motion effects - 3 of 3
  # Clips are indexed 1 to N from left to right on the video track
  positionalData = [
    {"index": 1, "fusion_path": fusion_path + "fusion_loads/10secs-24fps/zoom120.comp"},
    {"index": 2, "fusion_path": fusion_path + "fusion_loads/10secs-24fps/zoompan_left.comp"},
    {"index": 3, "fusion_path": fusion_path + "fusion_loads/10secs-24fps/zoom120to100.comp"},
    {"index": 4, "fusion_path": fusion_path + "fusion_loads/10secs-24fps/zoompan_top.comp"},
    {"index": 5, "fusion_path": fusion_path + "fusion_loads/10secs-24fps/zoompan_trc.comp"}
  ]

  addMotionsTo(track, positionalData) # type: ignore
except Exception as e:
  print("Did you paste in part 1 of the script into DaVinci Resolve's console? Error:", e)