
track = timeline.GetItemsInTrack('video', 1)
positionalData = [
  {"index": 1, "fusion_path": "/Users/wengffung/dev/web/davinci/fusion_loads/10secs-24fps/zoom120.comp"},
  {"index": 2, "fusion_path": "/Users/wengffung/dev/web/davinci/fusion_loads/10secs-24fps/zoompan_left.comp"},
  {"index": 3, "fusion_path": "/Users/wengffung/dev/web/davinci/fusion_loads/10secs-24fps/zoom120to100.comp"},
  {"index": 4, "fusion_path": "/Users/wengffung/dev/web/davinci/fusion_loads/10secs-24fps/zoompan_top.comp"},
  {"index": 5, "fusion_path": "/Users/wengffung/dev/web/davinci/fusion_loads/10secs-24fps/zoompan_trc.comp"}
]

addMotionsTo(track, positionalData)
