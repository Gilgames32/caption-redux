# Caption Redux
(lite)

a gif captioner in the ifunny caption style, popular on discord and r/whenthe

**heavly inspired by and features many snippets from [kubinka0505's iFunny-Captions](https://github.com/kubinka0505/iFunny-Captions)** (public archive)


caption redux is still missing extra functionalities which the above mentioned generator had, some of these will be added in the near future

this project focuses on an easier to use and easier to maintain version of the now archived repo

## installation
```bash
git clone https://github.com/Gilgames32/caption-redux.git
cd caption-redux
pip install -r requirements. txt
```
have the following packages installed and added to the path
- [ffmpeg](https://ffmpeg.org/download.html)
- [gifsicle](https://www.lcdf.org/gifsicle/)

## usage
\>open `caption-redux.py`
\>???
\>profit

optionally you can run it with positional arguments
`python3 caption-redux.py -i "<image link>" -t "<caption text>"`
- `<image link>` path or direct url to the image
- `<caption text>` the caption, supports emojis, and discord emotes in `<:floraSmug:1112288234488201307>` format
 

## roadmap:
- png optimization
- video caption
- video optimization
- font, color, and emoji host configuration
- gui
- cache system
- wider range of supported gif hosting sites
- option to resize the gif to match the caption width and not the other way around
- try to use memory instead of much priceous ssd (stupit)
- show output file size
- make it retain the original gif speed
- emoji styles
- force empty emoji cache
- foce gif output
- gif optimization options
- fancy readme :3
- idk, whatever comes to my mind really


## contribution
the project is still in developement and open to contributions

