from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
import sys
import cv2
from PySide6.QtCore import Signal, Slot, Qt, QThread
import numpy as np
from gaze_estimator import GazeEstimator
from calibration import run_9_point_calibration, fine_tune_kalman_filter
import tkinter as tk
import pyautogui
import os
from speech_processor import SpeechProcessor

# Reducing input lag
pyautogui.PAUSE = 0

# Disabling failsafe when eyetracking starts
pyautogui.FAILSAFE = False

class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self, gaze_estimator: GazeEstimator, kalman: cv2.KalmanFilter):
        super().__init__()
        self._run_flag = True
        self.estimator = gaze_estimator
        self.kalman = kalman
        
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth() 
        self.screen_height = root.winfo_screenheight()
        root.destroy() 

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                features, blink_detected = self.estimator.extract_features(cv_img)
                if features is not None and not blink_detected:
                    X = np.array([features])
                    gaze_point = self.estimator.predict(X)[0]
                    x, y = int(gaze_point[0]), int(gaze_point[1])
                    
                    prediction = kalman.predict()
                    x_pred = int(prediction[0][0])
                    y_pred = int(prediction[1][0])
                    
                    # Clamp the predicted gaze point to the screen boundaries
                    x_pred = max(0, min(x_pred, self.screen_width - 1))
                    y_pred = max(0, min(y_pred, self.screen_height - 1))

                    measurement = np.array([[np.float32(x)], [np.float32(y)]])
                    if np.count_nonzero(kalman.statePre) == 0:
                        kalman.statePre[:2] = measurement
                        kalman.statePost[:2] = measurement
                    kalman.correct(measurement)
                else:
                    x_pred, y_pred = None, None
                    blink_detected = True
                
                if x_pred is not None and y_pred is not None:
                    pyautogui.moveTo(x_pred, y_pred)
                    print(x_pred, y_pred)
                    
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class SpeechThread(QThread):
    def __init__(self, speech_processor: "SpeechProcessor"):
        super().__init__()
        self.speech_processor = speech_processor

    def run(self):
        self.speech_processor.listen()

    def stop(self):
        self.speech_processor.cleanup()
        self.wait()

class App(QWidget):
    def __init__(self, estimator: GazeEstimator, kalman: cv2.KalmanFilter):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the speech processing thread
        self.speech_processor = SpeechProcessor(model_type="google", input_mode="command")
        self.speech_thread = SpeechThread(self.speech_processor)
        self.speech_thread.start()

        # # create the video capture thread
        self.video_thread = VideoThread(estimator, kalman)
        # connect its signal to the update_image slot
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.video_thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @Slot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    gaze_estimator = GazeEstimator()
    run_9_point_calibration(gaze_estimator, 0)
    
    kalman = cv2.KalmanFilter(4, 2)
    kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kalman.transitionMatrix = np.array(
        [[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
        np.float32,
    )
    kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 10
    kalman.measurementNoiseCov = np.eye(2, dtype=np.float32) * 1
    kalman.statePre = np.zeros((4, 1), np.float32)
    kalman.statePost = np.zeros((4, 1), np.float32)

    fine_tune_kalman_filter(gaze_estimator, kalman, 0)
    
    cursor_alpha = 0.0
    cursor_alpha_step = 0.05
    
    app = QApplication(sys.argv)
    a = App(gaze_estimator, kalman)
    
    a.show()
    sys.exit(app.exec())