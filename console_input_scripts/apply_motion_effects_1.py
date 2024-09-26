# Init Resolve
# ------------------------------------------------
import importlib.util
resolve = None

import sys
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
sys.path.append(r'/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Examples')

if resolve == None:
    resolve = None
    if importlib.util.find_spec("DaVinciResolveScript") is not None:
        import DaVinciResolveScript as dvr_script
        test_init = dvr_script.scriptapp("Resolve")
        if(test_init is not None):
            resolve = test_init
        else:
            if app is not None:
                resolve = app.GetResolve()
    else:
        # app is available during runtime with DaVinci Resolve's console
        if app is not None:
            resolve = app.GetResolve()
    globals()['resolve'] = resolve


if resolve is None:
	print("Failed to connect to DaVinci Resolve.")
	exit()
else:
    print("Connected to DaVinci Resolve API...")

# _OTHER IMPORTS
# ------------------------------------------------

# Common Objects
# ------------------------------------------------
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()

# Remove timeline block if not applicable
try: 
    timeline = project.GetCurrentTimeline()
except Exception as e: # Comment/Uncomment as needed
    # print("ERROR - No timeline is currently open.")
    # print(e)
    # exit()
    media_pool.CreateEmptyTimeline("Timeline 1")
    timeline = project.GetCurrentTimeline()
    pass

# Remove this video track 1 block if not applicable
try: 
    track = timeline.GetItemsInTrack('video', 1)
except Exception as e:
    print("ERROR - No video track is available in opened timeline. Does your script work with an existing track? If not, you don't need this object - go ahead and remove this block.")
    print(e)
    exit()

# _SCRIPT:
# ------------------------------------------------

def addMotionsTo(track, positionalData):
    print("Timeline is: ", timeline.GetName())
    for datum in positionalData:
        index = datum["index"]
        fusion_path = datum["fusion_path"]
        print("Creating nodes and connecting to media in and out: " + str(index) + ":" + fusion_path)
    
        clip = track[index]
        print("Clip: ", clip)

        try:
            clip.ImportFusionComp(fusion_path)
            print("Imported Fusion comp:", fusion_path)
        except Exception as e:
            print("Error importing Fusion comp:", e)

        # A clip could have multiple fusion clips
        fusion_comp_name_list = clip.GetFusionCompNameList()
        print("Fusion comp name list:", fusion_comp_name_list)
        print("")

        fusion_comp = None
        if len(fusion_comp_name_list) == 0:
            clip.AddFusionComp()  
            fusion_comp_name_list = clip.GetFusionCompNameList()
        
        # Retrieve the Fusion composition from the clip (it's the top recent fusion clip that's active)
        # fusion_comp = clip.GetFusionCompByName(fusion_comp_name_list[-1]) # Get most top of the stack fusion
        fusion_comp = clip.GetFusionCompByName("Composition 1") # Get most top of the stack fusion

        #     if index > len(track)-1:
        #         continue
        #     else:
        #         clip = track[index+1]

        print("Converted clip to fusion clip:", fusion_comp)

        if(fusion_comp is None):
            print("Difficult applying motion effect because this clip has no Fusion comp? Skipping this clip...")
            continue
            # fusion_comp.AddFusionComp()

        # Find the MediaIn1 and MediaOut1 nodes
        media_in_node = fusion_comp.FindTool("MediaIn1")
        media_out_node = fusion_comp.FindTool("MediaOut1")

        print(media_in_node)
        print(media_out_node)

        # Assuming no user manipulation on MediaIn1 and MediaOut1
        if media_in_node and media_out_node: #
            # Skip because inconsistently crash: Disconnect MediaIn1 from MediaOut1
            # print("Disconnected MediaIn1 from MediaOut1")
            # media_out_node.Inputs["Input"].Disconnect() # No need
            print("MediaIn1 and MediaOut1 nodes found.")
        else:
            # Add MediaIn1 if it's missing
            if not media_in_node:
                print("Added MediaIn1 node")
                media_in_node = fusion_comp.AddTool("MediaIn", -32768, 0)  # Adds MediaIn1 node

        # Add MediaOut1 if it's missing
            if not media_out_node:
                print("Added MediaOut1 node")
                media_out_node = fusion_comp.AddTool("MediaOut", 32768, 0)  # Adds MediaOut1 node

        # These nodes are named from Weng's Motion Effects Library
        into_comp = fusion_comp.FindTool("INPUT_MED_IN")
        exit_comp = fusion_comp.FindTool("OUTPUT_MED_OUT")

        # Assuming into_comp and exit_comp are valid nodes in the Fusion composition
        if into_comp:
            print(f"into_comp Inputs: {into_comp.Inputs}")
            print(f"into_comp Outputs: {into_comp.Outputs}")
        else:
            print("into_comp is None")

        if exit_comp:
            print(f"exit_comp Inputs: {exit_comp.Inputs}")
            print(f"exit_comp Outputs: {exit_comp.Outputs}")
        else:
            print("exit_comp is None")

        # Assuming into_comp and exit_comp are valid nodes in the Fusion composition
        # Connect MediaIn1's Output to into_comp's Input
        if media_in_node and into_comp:
            into_comp.ConnectInput("Background", media_in_node, "Output")
            print("Connected MediaIn1 to into_comp")

        # Connect exit_comp's Output to MediaOut1's Input
        if exit_comp and media_out_node:
            media_out_node.ConnectInput("Input", exit_comp, "Output")
            print("Connected exit_comp to MediaOut1")