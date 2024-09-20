resolve = app.GetResolve()
if not resolve:
    sys.exit("Failed to initialize DaVinci Resolve")

# Access the project manager and current project
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
if not project:
    sys.exit("No project is currently open in DaVinci Resolve")

# Access the current timeline
timeline = project.GetCurrentTimeline()
if not timeline:
    sys.exit("No timeline is currently active in the current project")

def get_video_clips(timeline, track_index=1):
    """
    Retrieves all video clips from the specified video track.

    Parameters:
        timeline: The current timeline object.
        track_index: The video track number to retrieve clips from (default is 1).

    Returns:
        A dictionary of clip IDs and clip objects.
    """
    clips = timeline.GetItemsInTrack("video", track_index)
    return clips

def has_fusion_composition(clip):
    """
    Checks if a clip has an associated Fusion composition.

    Parameters:
        clip: The clip object.

    Returns:
        True if the clip has a Fusion composition, False otherwise.
    """
    fusion_comps = clip.GetFusionCompNameList()
    return len(fusion_comps) > 0

def assign_fusion_composition(timeline, original_clip, fusion_template_comp_name):
    """
    Assigns a Fusion composition to a clip by replacing it with a Fusion composition.

    Parameters:
        timeline: The current timeline object.
        original_clip: The original clip object.
        fusion_template_comp_name: The name of the Fusion composition template to use.

    Returns:
        True if successful, False otherwise.
    """
    # Retrieve the Fusion composition by name
    fusion_comps = timeline.GetFusionCompList()
    if fusion_template_comp_name not in fusion_comps:
        print(f"Fusion composition '{fusion_template_comp_name}' not found.")
        return False

    # Get the Fusion composition clip
    fusion_clip = timeline.ImportFusionComp("/Users/wengffung/dev/web/temp-vid/fusion_compiled/php.comp")
    if not fusion_clip:
        print(f"Failed to find Fusion composition '{fusion_template_comp_name}'.")
        return False

    # Get original clip's properties
    start_frame = original_clip.GetStart()
    duration = original_clip.GetDuration()

    # Duplicate the Fusion composition
    # Note: The API may not support duplication directly; this is a placeholder
    # You might need to manually create or have multiple Fusion comps ready
    # For demonstration, we'll assume the fusion_clip can be reused

    # Replace the original clip with the Fusion composition
    # Note: The ReplaceClip method might not exist; alternative approaches may be needed
    # This is a hypothetical implementation
    try:
        timeline.ReplaceClip(original_clip, fusion_clip)
        print(f"Assigned Fusion composition '{fusion_template_comp_name}' to clip '{original_clip.GetName()}'.")
        return True
    except Exception as e:
        print(f"Error assigning Fusion composition: {e}")
        return False

def ensure_all_clips_have_fusion(timeline, track_index=1, fusion_template_comp_name="DefaultFusionComp"):
    """
    Ensures all clips in the specified video track have a Fusion composition.

    Parameters:
        timeline: The current timeline object.
        track_index: The video track number to process (default is 1).
        fusion_template_comp_name: The name of the Fusion composition template to assign.
    """
    clips = get_video_clips(timeline, track_index)
    if not clips:
        print(f"No clips found in video track {track_index}.")
        return

    for clip_id, clip in clips.items():
        clip_name = clip.GetName()
        print(f"Processing clip: {clip_name}")

        if has_fusion_composition(clip):
            print(f"Clip '{clip_name}' already has a Fusion composition.")
            continue

        # Assign a Fusion composition to the clip
        success = assign_fusion_composition(timeline, clip, fusion_template_comp_name)
        if not success:
            print(f"Failed to assign Fusion composition to clip '{clip_name}'.")

# Execute the function
# Replace 'DefaultFusionComp' with the actual name of your Fusion composition template
ensure_all_clips_have_fusion(timeline, track_index=1, fusion_template_comp_name="DefaultFusionComp")
