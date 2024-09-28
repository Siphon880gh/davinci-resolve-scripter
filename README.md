# DaVinci Resolve Scripter

![Last Commit](https://img.shields.io/github/last-commit/Siphon880gh/davinci-resolve-scripter/main)
<a target="_blank" href="https://github.com/Siphon880gh" rel="nofollow"><img src="https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub" style="max-width:8.5ch;"></a>
<a target="_blank" href="https://www.linkedin.com/in/weng-fung/" rel="nofollow"><img src="https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue" alt="Linked-In" data-canonical-src="https://img.shields.io/badge/LinkedIn-blue?style=flat&amp;logo=linkedin&amp;labelColor=blue" style="max-width:10ch;"></a>
<a target="_blank" href="https://www.youtube.com/@WayneTeachesCode/" rel="nofollow"><img src="https://img.shields.io/badge/Youtube-red?style=flat&logo=youtube&labelColor=red" alt="Youtube" data-canonical-src="https://img.shields.io/badge/Youtube-red?style=flat&amp;logo=youtube&amp;labelColor=red" style="max-width:10ch;"></a>

By Weng (Weng Fei Fung). Script that automates video editing in DaVinci Resolve by automatically importing media, creating time line, adding zoom and pan motion effects, adding transitions, and automatic subtitling (on Free DaVinci Resolve).

## Requirement

### Start timecode at 00:00:00:00 if using my fusion scripts

Although my scripts allows you to change the starting time code to 01:00:00:00 or 00:00:00:00, you should keep it at 00:00:00:00. The fusion motion effects are based off frame numbers starting from 00:00:00:00, which cannot change on the FREE DaVinci Resolve's API, so your timelines must start at 00:00:00:00. So before applying fusion effects script, you should right click the timeline in the media pool -> Timelines -> Starting Timecode... The only exception to this requirement is if you don't use my fusion scripts, then you're free to adjust the timestart variable in my code.

### Some manual mouse work required
I cannot have a single script that runs to create a project because of how DaVinci made certain API's unavailable on the free version DaVinci Resolve v19.0.1 build 6 20024. I would like my API available to all DaVinci versions. Here is a breakdown of how DaVinci created this limit:

- My script can import media then place them as clips into a timeline video track, however the script cannot adjust the duration of each clip to your liking. 
- The workaround is to import a timeline and there are various formats, from the most plain EDL format (which supports cut and dissolve transitions) and the more complicated format OTIO (that supports cut, dissolve, AND wipes from different edges). While importing can bring in specified durations AND transitions, as of the current version, Fusion clips will have large negative frames, breaking fusion effects, and the free DaVinci API does not allow changing start frames.
- If you apply your own fusion or the fusion presets my repo provides, it will fail because of the negative frames. You can right click the timeline imported clips -> New Fusion Clip, BUT that removes all the imported transitions! 
- But not to worry, I have a fix that involves manually moving the transitions from the imported timeline to a cloned timeline (though you have to manually match their clip durations). We'd have those two timelines as tracks in one timeline, to simplify things. This will be the workaround until DaVinci fixes the negative frames bug.

In addition, free DaVinci doesnt allow you to run scripts outside of the editor. You have to run the script either by pasting it into the DaVinci console (Workspace -> Console), or dropping a file into the console.

Keep in mind certain APIs cannot run as a drop-in script, but they can run in the console, which is another limitation placed on free versions. AddFusionComp that makes sure your timeline item will have a fusion for you to programatically add nodes or to load a fusion comp file, that will fail as a drop-in script but yet the console accepts and executes if it were inputted in.

Summary of limitations (not comprehensive):
- SetCurrentTimecode not available on free API
- SetSetting, SetProperty, and similar are not available
- SetStart, SetEnd, SetDuration disabled so you can’t programmatically adjust clip durations
- ImportFusionComp fails to work as a drop into the DaVinci console script, but you can input directly into the DaVinci console and it works
- ImportFusionComp and AddFusionComp sometimes fails if you’re not on the Fusion screen. Last two limitations are discussed https://www.steakunderwater.com/wesuckless/viewtopic.php?t=4317&start=15


## Usage

**Prep the media:**

1. First have your images and video clips and audio ready. We will automate creating a DaVinci project with timeline of your clips. There will be zoom/pan effects and transitions automated into the timeline.

2. Make sure your images are the same dimensions or reasonably similar dimensions so there won't be visually unappealing black bars. Since you probably want the zoom and pan effects that my scripts offer, you wouldn't want black bars and instead would prefer blurred background padding (the same picture at where the black bars would be to keep a similar tone of the picture, however is blurred and zoomed so is an appropriate background). 

If that applies to you, adjust this NodeJS script then run it to find the max dimensions among the picture, then apply blurred background padding to smaller dimension pictures: `cd letterbox && node convert.js`

3. Adjust `unassemble__drop_scripts/import_media_and_assemble_timeline.py` to your clips and desired settings (all caps variables).

Then drag and drop `unassemble__drop_scripts/import_media_and_assemble_timeline.py` into DaVinci Console (Workspace -> Console). This will import into the media pool and assemble each image as a clip into the timeline. It will do so without automatically assembling an image sequence from filenames with 01, 02, etc suffixes.

**Transitions:**

4. Adjust `generate_otio/generate.py` to make sure the same filenames and consider the settings (all caps variables). Run the python script in your computer's terminal (`cd generate_otio && python generate.py`). This will generate and replace if necessary `generate_otio/generated_otio/generated.otio` (exported.otio is for when I exported otio from DaVinci to test things).

Import the timeline `generate_otio/generated_otio/generated.otio` going to File -> Import -> Timeline. Best to have the timecode at 00:00:00:00 at the import dialog. This imports in transitions.

This will import the clips, their durations, and their transitions.

Explanation: Why not skip running `import_media_assemble_timeline.py` because importing the timeline file also imports media and assembles clips into the timeline. This is because if you've skipped that step which imports images as individual clips, then importing the timeline file will automatically create image sequences from images sufficed with 01, 02, 03. For example, image01.jpg and image02.jpg would've become a image[01-02] image sequence and give you less control over them. By having ran the python script, it makes sure the media are individually imported unassembled as image01.jpg, image02.jpg etc, then when you import the timeline, then DaVinci can refer to your current media pool and know you don't want automatic assembly.

**Motion Effects:**

5. You now have created two timelines. On the python generated timeline, copy all the clips of the track to your clipboard. Then on the imported timeline, create a new video track and paste the clips there.

- Tip: You may want to isolate the new video track in order to select that video track to paste into (Option click the Audio Track Selector if on Mac). I suggest you are pasting into a Video Track 2.
- Tip: You may want to click Magnet icon to turn on snap mode.

6. Adjust the durations of V2 clips to match the imported clips. Then drag and drop the transitions from the V1 clips to the V2 clips. Then you may delete the imported timeline so the new adjusted python timeline remains. You will notice that the V2 track gets turned into a V1 track by name, important because the next step of applying the code lets you select the video track, and we'll keep it as video track 1.

- Tip: You can adjust the durations of all clips on the track simultaneously by selecting all thoes clips, then turning on Trim mode (T), and then changing one of the clip's duration (Either right click -> Change Clip Duration, or CMD+D on Mac)

Explanation: As of DaVinci 19.0.1 build 6, there is still a bug where all imported timelines will have fusion set to a negative frame (go look into Fusion page), which will make your motion effects fail. Until DaVinci fixed this bug (which started in 2021 as far as I know), this workaround of manipulating two tracks is required.

7. Now we apply the code for motion effects which will be done through Fusion's engine. Adjust `motion__input_scripts/apply_motion_effects_2_select.py` firstly which video track - and we'll keep it video track 1 - and then which clip you want to have which motion effects. Look into fusion_compiled for the .comp files that our API will load. First clip would be index 1, second clip would be index 2, etc. For each clip index, there needs to be a path to the effects .comp file. These fusion composition files are generated from `motion__input_scripts/index.html`based off as few templates as possible at fusion_templates/.

If using `motion__input_scripts/index.html` to generate specific fusion effect .comp files by fps and clip duration, make sure to input those settings and click "Refresh Below" button before saving the generated .comp files from the index.html dashboard. The fusion comps are zoom effects, as well as zoom pans to corners and sides. Btw, you have to open that index.html with a php server (Eg. MAMP)

I recommend matching motion effects to what images make sense (for example if the focus should be at the top right of a picture, then you zoom-pan to the top right corner - fusion_compiled/10secs-24fps/zoompan_trc.comp). The motion effects needs to match the duration and fps of your clip, which you can see in the filepath (eg. "fusion_compiled/10secs-24fps/..")

8. Copying and pasting into console the contents of `unassemble__drop_scripts/apply_motion_effects_1.py`. Then next, copying and pasting into console the script you adjusted from `unassemble__drop_scripts/apply_motion_effects_2_select.py`

Explanation: Free Davinci Resolve nerfed their APIs in various ways. Many Fusion composition related API does not work in a python file, but can be directly inputted into the DaVinco console even though it is using the python language.

9. If a fusion motion effect fails to apply (The console outputted `Difficult applying motion effect because this clip has no Fusion comp? Skipping this clip...`), you can drag and drop from fusion_drops/ directly into the Fusion screen, then manually make sure the MediaIn and MediaOut nodes are connected to it.

10. That's it. You can now render your video. 

- I recommend templatizing what you have: Bear in mind the named files. Your next project you can have the same filenames. If in the next project you delete the media pool files then upload your new media with the same filenames, you can conform the timeline clips to relink to the current assets! You'd have to right click the timeline clips -> Untick "Conform Lock Enabled". Then you can right click the current timeline asset in the media pool -> Timelines -> Reconform From Bins. You could simplify things even further by using this same project but having different bins, which are just folders you create under "Master" to the left of the media pool. This works very well if you have the same types of videos you make (eg. shorts video with 5 second images that zoom/pan as you speak on top of it).


**Automatic Subtitle Track OR Text+ Subtitle Clips:**
You can from your audio track which is usually AI generated (text-to-speech) or an actual voice recording generate a subtitle SRT file.

With this SRT file, you can have subtitle text at the bottom of your video and it will change as necessary because it syncs with your audio as long as your audio recording and the subtitle aligns to the start of the timeline (aka traditional subtitle track). Or, you can run an additional script that generates Text+ clips into an empty video track and this allows finer control of text visuals, great for IG-styled centered of the video text.

To create that subtitle file, you adjust then run `subtitle_from_audio/generate.py`.

Then decide what you want to do with the SRT file.

To have the traditional subtitle track, drag and drop the SRT file into DaVinci's media pool before creating and filling the subtitle track.

To generate Text+ clips on an empty video track, you adjust and drop the script `subtitle_from_audio/drop_textp*.py` into the DaVinci console. There is more than one `drop_textp` script corresponding to different Text+ effects - choose one that you like, and then stick to adjusting and dropping only that script.

The above are brief instructions. For in-depth instructions, refer to [README_transcribe_audio.md](subtitle_from_audio/README_transcribe_audio.md).

## Hint Mode

Running `make hint` will rename folders and files by prefixing a number which hints to you the sequence you should run the scripts in order to create a video in DaVinci. For example: 01_letterbox, 02_unassemble...

Run `make clean` to restore the filenames.

## Ancillary folder?

These are scripts I developed while trying to automate creating video from images with transition and motion effects. However, the scripts ended up being useless for this purpose, but they may be useful for other purposes, so I kept the scripts in this folder.

## Explanations

### Explanation of OTIO Timeline (generate_otio/generate.py)
Code currently works for EDL and OTIO timeline. EDL does not support wipes but supports cuts and dissolves (aka crossfades). Even fcp xml 1.11 does not support it (tested by exporting then reimporting into an empty project). EDL and AAF fails saying unrecognized transitions when transitioning out timeline with wipes

But I found OTIO format works! You can’t easily create OTIO format because it’s very wordy. But there’s a python package opentimelineio that’s developed for the purpose of generating OTIO timeline (if you’re not exporting the timeline as OTIO from DaVinci). There is no such nodejs equivalent as of late 2024.

Why we generate the OTIO timeline file? It would be too difficult for the user to markup the timeline file themselves because of its high verbosity and transition frames are fussy. Even if you had chosen the more simple EDL (if you’re not doing wipe transitions), you wouldn’t want to figure out the exact time codes for transition to work.