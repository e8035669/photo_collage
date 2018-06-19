# photo_collage

You can collage a photo by many small picture.

## require

- python 2.7
- opencv-python
- numpy (opencv needed)

## usage

```sh
python MakePics.py -i video.mp4 -o pics/
python MakeYCrCbTable.py -i pics/
python MakeCollage.py -i myphoto.jpg -d pics/ -o output.jpg
```

## for more options

```sh
python MakePics.py --help
python MakeYCrCbTable.py --help
python MakeCollage.py --help
```
