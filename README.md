# DaVinci Resolve Scripter

![Last Commit](https://img.shields.io/github/last-commit/Siphon880gh/davinci-resolve-scripter/main)
<a target="_blank" href="https://github.com/Siphon880gh" rel="nofollow"><img src="https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub" alt="Github" data-canonical-src="https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub" style="max-width:8.5ch;"></a>
<a target="_blank" href="https://www.linkedin.com/in/weng-fung/" rel="nofollow"><img src="https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue" alt="Linked-In" data-canonical-src="https://img.shields.io/badge/LinkedIn-blue?style=flat&amp;logo=linkedin&amp;labelColor=blue" style="max-width:10ch;"></a>
<a target="_blank" href="https://www.youtube.com/@WayneTeachesCode/" rel="nofollow"><img src="https://img.shields.io/badge/Youtube-red?style=flat&logo=youtube&labelColor=red" alt="Youtube" data-canonical-src="https://img.shields.io/badge/Youtube-red?style=flat&amp;logo=youtube&amp;labelColor=red" style="max-width:10ch;"></a>

By Weng (Weng Fei Fung). Script that automates video editing by automatically importing media, creating time line, adding zoom and pan motion effects and adding transitions.

## Requirement

Although my scripts allows you to change the starting time code to 01:00:00:00 or 00:00:00:00, the fusion motion effects are based off frame numbers starting from 00:00:00:00, so your timelines must start at 00:00:00:00. You right click the timeline in the media pool -> Timelines -> Starting Timecode...

Unfortunately my code can set the starting timecode for the generated timeline but it only works on paid DaVinci Studio, so you may have to do it manually after generating a timeline with clips inside, before applying motion effects and timing and transitions.

## Usage

Various ways because DaVinci's API Python and Fusion Scripting is not matured. Will fill in usage later.