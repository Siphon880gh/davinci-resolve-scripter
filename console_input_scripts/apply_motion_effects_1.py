import traceback

resolve = app.GetResolve()
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()
track = timeline.GetItemsInTrack('video', 1)

def addMotionsTo(track, positionalData):
    try:
        for datum in positionalData:
            index = datum["index"]
            fusion_path = datum["fusion_path"]
            print("Creating nodes and connecting to media in and out: " + str(index) + ":" + fusion_path)
        
            clip = track[index]

            # Retrieve the Fusion composition from the clip
            fusion_comp_name_list = clip.GetFusionCompNameList()
            if len(fusion_comp_name_list) == 0:
                # clip.AddFusionComp()  
                if index > len(track)-1:
                    continue
                else:
                    clip = track[index+1]

            clip.ImportFusionComp(fusion_path)
            fusion_comp = clip.GetFusionCompByName(fusion_comp_name_list[-1])  # Get most top of the stack fusion

            print("Converted clip to fusion clip:", fusion_comp)

            # Find the MediaIn1 and MediaOut1 nodes
            media_in_node = fusion_comp.FindTool("MediaIn1")
            media_out_node = fusion_comp.FindTool("MediaOut1")

            print(media_in_node)
            print(media_out_node)

            # Disconnect MediaIn1 from MediaOut1 (disconnect inputs/outputs)
            if media_in_node and media_out_node: # Assuming no user manipulation on MediaIn1 and MediaOut1
                # Disconnect MediaIn1 from MediaOut1
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

    except Exception as e:
        # Print the entire traceback
        traceback.print_exc()

