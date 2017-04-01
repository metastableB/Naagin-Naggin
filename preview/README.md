# Properly Converting Videos to GIFs

## Changing Video Playback Speed

    ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4

The filter works by changing the presentation timestamp (PTS) of each video frame. For example, if there are two successive frames shown at timestamps 1 and 2, and you want to speed up the video, those timestamps need to become 0.5 and 1, respectively. Thus, we have to multiply them by 0.5.


## Converting Video to GIF

    ffmpeg -t <duration> -ss <starting position in hh:mm:ss format> -i <input_video> out%04d.gif

For example:

    ffmpeg -t 30 -ss 00:00:7 -i output.mp4 out%04d.gif
    # or,
    ffmpg -ss 00:00:7 -i output.mp4 out%04d.gif

`-ss` togther with `-t` can be used to specify the end time.
`-vf scale=320:240` can be used to scale the output image. Make sure the flag is used immediately preceding the output file name specification.

## Details About Preview Examples

**01.gif**
Grid Size: 20x20
Cell Size: 30
Food Score: 50
Living Score: -1
Snake Agent: Reflex Agent
Food Agent: MaxManhattanFoodAgent
Score: 2021
Length: 67
Time Output:
```
    real    1m14.105s
    user    0m6.547s
    sys 0m0.980s
```

**02.gif**
Grid Size:20x20
Cell Size:30
Food Score:50
Living Score:-1
Snake Agent: MinMax Agent
Food Agent: MaxManhattanFoodAgent
Score:
Length:
Time Output:



Depth=6

**03.gif**
Grid Size:20x20
Cell Size:30
Food Score:50
Living Score:-1
Snake Agent: MinMax Agent
Food Agent: MaxManhattanFoodAgent
Score: 2277
SnakeLen: 82
Time Output:
```
    real    3m14.091s
    user    0m26.693s
    sys 0m2.413s
```
Depth: 1