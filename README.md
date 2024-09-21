# DaVinci Resolve Scripter

![Last Commit](https://img.shields.io/github/last-commit/Siphon880gh/davinci-resolve-scripter/main)
<a target="_blank" href="https://github.com/Siphon880gh" rel="nofollow"><img src="https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub" style="max-width:8.5ch;"></a>
<a target="_blank" href="https://www.linkedin.com/in/weng-fung/" rel="nofollow"><img src="https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue" alt="Linked-In" data-canonical-src="https://img.shields.io/badge/LinkedIn-blue?style=flat&amp;logo=linkedin&amp;labelColor=blue" style="max-width:10ch;"></a>
<a target="_blank" href="https://www.youtube.com/@WayneTeachesCode/" rel="nofollow"><img src="https://img.shields.io/badge/Youtube-red?style=flat&logo=youtube&labelColor=red" alt="Youtube" data-canonical-src="https://img.shields.io/badge/Youtube-red?style=flat&amp;logo=youtube&amp;labelColor=red" style="max-width:10ch;"></a>

By Weng (Weng Fei Fung). Script that automates video editing by automatically importing media, creating time line, adding zoom and pan motion effects and adding transitions.

## Requirement

### Start timecode at 00:00:00:00 if using my fusion scripts

Although my scripts allows you to change the starting time code to 01:00:00:00 or 00:00:00:00, you should keep it at 00:00:00:00. The fusion motion effects are based off frame numbers starting from 00:00:00:00, which cannot change on the FREE DaVinci Resolve's API, so your timelines must start at 00:00:00:00. So before applying fusion effects script, you should right click the timeline in the media pool -> Timelines -> Starting Timecode... The only exception to this requirement is if you don't use my fusion scripts, then you're free to adjust the timestart variable in my code.

### Some manual mouse work required
I cannot have a single script that runs to create a project because of how DaVinci made certain API's unavailable on the free version DaVinci Resolve v19.0.1 build 6 20024. I would like my API available to all DaVinci versions. Here is a breakdown of how DaVinci created this limit:

- My script can import media then place them as clips into a timeline video track, however the script cannot adjust the duration of each clip to your liking. 
- The workaround is to import a timeline and there are various formats, from the most plain EDL format (which supports cut and dissolve transitions) and the more complicated format OTIO (that supports cut, dissolve, AND wipes from different edges). While importing can bring in specified durations AND transitions, as of the current version, Fusion clips will have large negative frames, breaking fusion effects.
- If you apply your own fusion or the fusion presets my repo provides, it will fail because of the negative frames. You can right click the timeline imported clips -> New Fusion Clip, BUT that removes all the imported transitions! 

In addition, free DaVinci doesnt allow you to run scripts outside of the editor. You have to run the script either by pasting it into the DaVinci console (Workspace -> Console), or dropping a file into the console.

Keep in mind certain APIs cannot run as a drop-in script, but they can run in the console, which is another limitation placed on free versions. AddFusionComp that makes sure your timeline item will have a fusion for you to programatically add nodes or to load a fusion comp file, that will fail as a drop-in script but yet the console accepts and executes if it were inputted in.

Summary of limitations:
- SetCurrentTimecode not available on free API
- SetSetting not available
- SetEnd disabled so you can’t programmatically adjust clip durations
- ImportFusionComp fails to work as a drop into the DaVinci console script, but you can input directly into the DaVinci console and it works
- ImportFusionComp and AddFusionComp sometimes fails if you’re not on the Fusion screen. Last two limitations are discussed https://www.steakunderwater.com/wesuckless/viewtopic.php?t=4317&start=15


## Usage

**Media imports and timeline assembly (without auto assembling image01.jpg, image02.jpg into a video clip image[01-02]):**

1. First have your images and video clips and audio ready. We will automate creating a DaVinci project with timeline of your clips. There will be zoom/pan effects and transitions automated into the timeline.

2. Adjust import_media_and_assemble_timeline.py to your clips and desired settings (all caps variables).

3. Drag and drop import_media_and_assemble_timeline.py into DaVinci Console (Workspace -> Console). This will import into the media pool and assemble each image as a clip into the timeline.

**Transition Effects:**
4. Adjust generate-otio.py to make sure the same filenames and consider the settings (all caps variables). Run the python script in your computer's terminal (`python generate-itio.py`). This will generate and replace if necessary `generated_otio/generated.otio` (exported.otio is for when I exported otio from DaVinci to test things).

5. Import the timeline `generated_otio/generated.otio` going to File -> Import -> Timeline. Best to have the timecode at 00:00:00:00 at the import dialog. This imports in transitions.

Explanation: Why not skip running import_media_assemble_timeline.py because importing the timeline file also imports media and assembles clips into the timeline. This is because if you've skipped that step which imports images as individual clips, then importing the timeline file will automatically create clips from images sufficed with 01, 02, 03. For example, image01.jpg and image02.jpg would've become a image[01-02] video clip and give you less control over them.

**Motion Effects:**
5. Make sure snap is on in the timeline (Magnet icon). Create a new video track above the current video track. Look on the left sidebar Effects for "Adjustment Clip" and drag that to the first clip position of the new track.

6. Copy and paste the adjustment clip to the other imported clip start positions. Then adjust so that the adjustment clips each cover the duration of each imported clip.

Explanation: As of DaVinci 19.0.1 build 6, there is still a bug where all imported timelines will have fusion set to a negative frame (go look into Fusion page), which will make your motion effects fail. Adjustment clips will reset each potential fusion clip to start at 0. Until DaVinci fixed this bug (which started in 2021 as far as know), steps 5 and 6 of adding adjustment clips is necessary

7. Now we apply the code for motion effects which will be done through Fusion. Adjust `apply_motion_effects_2_select` which clip you want to have motion effects. First clip would be index 1. For each clip index, there's a path to the effects .comp file. These fusion composition files are generated from index.html (Make sure to match the fps and clip duration). The fusion comps are zooming and zoom pans to corners and sides. I recommend selecting what makes sense for an image (for example if the focus should be at the top right of a picture, then you zoom and pan there.)

8. Copying and pasting into console: `apply_motion_effects_1.py`. Then next, copying and pasting into console the script you adjusted: `apply_motion_effects_2_select.py`

Explanation: Free Davinci Resolve nerfed their APIs in various ways. Many Fusion composition related API does not work in a python file, but can be directly inputted into the DaVinco console even though it is using the python language.

## Hint Mode

Running `make hint` will rename folders and files by prefixing a number which hints to you the sequence you should run the scripts in order to create a video in DaVinci.

Run `make clean` to restore the filenames.

## Explanations

### Explanation of OTIO Timeline (generate-otio.py)
Code currently works for edl. EDL does not support wipes but supports cuts and dissolves (aka crossfades). Even fcp xml 1.11 does not support it (tested by exporting then reimporting over an undone timeline). EDL and AAF fails saying unrecognized transitions when transitioning out timeline with wipes

But I found otio format works! You can’t easily create OTIO format because it’s very wordy. But there’s a python package opentimelineio that’s developed for the purpose of generating OTIO timeline (if you’re not exporting the timeline as OTIO from DaVinci). There is no such nodejs equivalent as of late 2024