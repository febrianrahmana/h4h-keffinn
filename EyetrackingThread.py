import numpy as np
import tkinter as tk
import pyautogui
import cv2

from PySide6.QtCore import Signal, Slot, Qt, QThread

from eyetracking.gaze_estimator import GazeEstimator
from eyetracking.calibration import run_9_point_calibration, fine_tune_kalman_filter

class EyetrackingThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.estimator = GazeEstimator()
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kalman.transitionMatrix = np.array(
            [[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
            np.float32,
        )
        self.kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 10
        self.kalman.measurementNoiseCov = np.eye(2, dtype=np.float32) * 1
        self.kalman.statePre = np.zeros((4, 1), np.float32)
        self.kalman.statePost = np.zeros((4, 1), np.float32)
        
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth() 
        self.screen_height = root.winfo_screenheight()
        root.destroy()
        
    def calibrate(self):
        run_9_point_calibration(self.estimator, 0)
        fine_tune_kalman_filter(self.estimator, self.kalman, 0)

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
                    
                    prediction = self.kalman.predict()
                    x_pred = int(prediction[0][0])
                    y_pred = int(prediction[1][0])
                    
                    # Clamp the predicted gaze point to the screen boundaries
                    x_pred = max(0, min(x_pred, self.screen_width - 1))
                    y_pred = max(0, min(y_pred, self.screen_height - 1))

                    measurement = np.array([[np.float32(x)], [np.float32(y)]])
                    if np.count_nonzero(self.kalman.statePre) == 0:
                        self.kalman.statePre[:2] = measurement
                        self.kalman.statePost[:2] = measurement
                    self.kalman.correct(measurement)
                else:
                    x_pred, y_pred = None, None
                    blink_detected = True
                
                if x_pred is not None and y_pred is not None:
                    pyautogui.moveTo(x_pred, y_pred)
                    
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
