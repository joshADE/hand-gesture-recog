# Hand Gesture Recog using MediaPipe
> A python project for detecting hand gestures using MediaPipe, Scikit-learn, and OpenCV

# Dependencies used
* [Python](https://www.python.org/)
* [MediaPipe](https://developers.google.com/edge/mediapipe/solutions/guide)
* [Scikit-learn](https://scikit-learn.org/stable/getting_started.html)
* [OpenCV](https://docs.opencv.org/5.0/index.html)
* [Pandas](https://pandas.pydata.org/)
* [NumPy](https://numpy.org/)

# Requirements

* Pip (Download python to install pip)
* GIT (Download [here](https://git-scm.com/))
* A webcam
* The MediaPipe hand landmarker model file, `hand_landmarker.task`

# Getting Started

## Clone Repository

Clone the repository to your computer.


```
git clone https://github.com/joshADE/hand-gesture-recog.git
```

## Setup the python environment, activate it, then install the dependencies
1. cd to the project directory.
2. Inside the project folder, create a virtual environment
3. Then activate the environment

On Windows with powershell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
or

On macOS / Linux with bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Download the Hand Landmarker pre-trained model

If the file `hand_landmarker.task` is not already in root of the project, download it from this link and place it in the root:

```text
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```
The `collect_data.py` and `live_predict.py` need to be placed in the root along with the `hand_landmarker.task` file.

## Install the dependencies


1. The dependencies can be found in `required_packages.txt`:
   - MediaPipe
   - OpenCV
   - NumPy
   - pandas
   - scikit-learn
   - joblib
2. To install it, run:

On Windows with powershell:

```powershell
python -m pip install --upgrade pip
python -m pip install -r required_packages.txt
```

or

On macOS / Linux with bash:

```bash
python -m pip install --upgrade pip
python -m pip install -r required_packages.txt
```


## Commands to start project

In the project directory, you can run the app by typing:

To collect the data run:
```bash
python collect_data.py 
```

__If propted to give Python permission to access  webcam, click Okay or Yes, as this is needed to collect the data__

Once `collect_data.py` runs, the webcam will turn on with a window showing the webcam's view.

This phase requires you show one of your hands to the webcam.

Press any one of the gesture keys below while your hand is visible and making the associated gesture to record an example. These examples are needed to train the model. The examples will be appended to the file `gesture_dataset_1.csv`. This file does not need to be created before hand.


| Key | Gesture Label |
| --- | ------------- |
| '1' | 'Thumbs_Up'   |
| '2' | 'Fist'        |
| '3' | 'Peace'       |
| 'q' |  Quit         |



Then to train the classifier, run (currently unavailable, use existing model file):
```bash
python train_model.py
```

When you run the above command, the script will read `gesture_dataset_1.csv` with all the training data, create a trained classifier from the data, and save the classifier to the file `gesture_model.pkl`. Running the command again will overwrite the file.

To test the model that was trained on live data, run:
```bash
python live_predict.py
```

The window with the webcam in view will be shown again similar to the `collect_data.py` script. Try making the same gestures again and the live predictor will use the model in the `gesture_model.pkl` file to predict the type of gesture performed. The result will be displayed inside the window as an overlay.



## Files and purpose

- `collect_data.py` : Captures and records hand landmark coordinates (x, y, and z as well as label) from the webcam into a file using the pre-trained hand landmarker model
- `train_model.py` : Trains the hand gesture classifier and saves the model to a file
- `live_predict.py` : Predicts live hand gestures using the webcam and saved classifier
- `required_packages.txt` : Lists the required packages/dependencies
- `hand_landmarker.task` : MediaPipe's hand landmarker model file
- `gesture_dataset_1.csv` : Stores the dataset created from the collection script
- `gesture_model.pkl` : Trained classifier stored as a file
