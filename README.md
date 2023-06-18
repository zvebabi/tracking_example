## Tracking example
Example of Multi-Object Tracking using [FairMOT project](https://github.com/ifzhang/FairMOT) on [Hallway Corridor dataset](http://www.santhoshsunderrajan.com/datasets.html)

### Run demo
This repo has a prebuilt docker image `zvebabi/tracking_example`, so you can pull and run app
```
mkdir -p demos # create directory to save video with result
docker run --rm --runtime=nvidia -v $PWD/demos:/demos zvebabi/tracking_example
```
here `$PWD/demos` is a folder on host PC to save video with result
- It is possible to change the length of tracking history, for example:
```
docker run --rm --runtime=nvidia -v $PWD/demos:/demos zvebabi/tracking_example /app/runApp.sh N
```
where `N` is a length of the object paths in pixels on original image, default 100

### Build container
- Clone this repo, let's call repo dir as ${REPO_ROOT}
- Download weights to folder `${REPO_ROOT}/weights`. Link to baseline weights: [fairmot_dla34.pth](https://drive.google.com/open?id=1iqRQjsG9BawIl8SlFomMg5iwkb6nqSpi&authuser=0)
- Run container build from ${REPO_ROOT}
```
docker build -t tracking_example -f Dockerfile .
```
- After build is done, you can run application with default parameters:
```
docker run --rm --runtime=nvidia -v $PWD/../demos:/demos tracking_example
```
Here `$PWD/../demos` is a folder on host PC to save video with result, on one level up from ${REPO_ROOT}

### Known issues:
- Homography for topview is hardcoded only for video `001.avi`