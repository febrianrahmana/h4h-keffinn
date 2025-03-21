import cv2
import numpy as np
import tkinter as tk
import time
import argparse
import os
from gaze_estimator import GazeEstimator
from calibration import (
    run_9_point_calibration,
    fine_tune_kalman_filter,
)

def main():
    parser = argparse.ArgumentParser(
        description="Gaze Estimation with Kalman Filter or KDE"
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument(
        "--background", type=str, default=None, help="Path to background image"
    )
    args = parser.parse_args()

    filter_method = "kalman"
    camera_index = args.camera
    background_path = args.background

    gaze_estimator = GazeEstimator()

    # Run the chosen calibration method (default 9p)
    run_9_point_calibration(gaze_estimator, camera_index=camera_index)

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

    fine_tune_kalman_filter(gaze_estimator, kalman, camera_index=camera_index)

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    cam_width, cam_height = 320, 240

    if background_path and os.path.isfile(background_path):
        background = cv2.imread(background_path)
        background = cv2.resize(background, (screen_width, screen_height))
    else:
        background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        background[:] = (50, 50, 50)

    cv2.namedWindow("Gaze Estimation", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(
        "Gaze Estimation", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
    )

    cap = cv2.VideoCapture(camera_index)
    prev_time = time.time()

    # Variables for gaze cursor fade effect
    cursor_alpha = 0.0
    cursor_alpha_step = 0.05

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        features, blink_detected = gaze_estimator.extract_features(frame)
        if features is not None and not blink_detected:
            X = np.array([features])
            gaze_point = gaze_estimator.predict(X)[0]
            x, y = int(gaze_point[0]), int(gaze_point[1])

            if filter_method == "kalman":
                prediction = kalman.predict()
                x_pred = int(prediction[0][0])
                y_pred = int(prediction[1][0])

                # Clamp the predicted gaze point to the screen boundaries
                x_pred = max(0, min(x_pred, screen_width - 1))
                y_pred = max(0, min(y_pred, screen_height - 1))

                measurement = np.array([[np.float32(x)], [np.float32(y)]])
                if np.count_nonzero(kalman.statePre) == 0:
                    kalman.statePre[:2] = measurement
                    kalman.statePost[:2] = measurement
                kalman.correct(measurement)

            # Increase cursor alpha for fade-in effect
            elif filter_method == "none":
                x_pred, y_pred = x, y
                contours = []

            cursor_alpha = min(cursor_alpha + cursor_alpha_step, 1.0)
        else:
            x_pred, y_pred = None, None
            blink_detected = True
            contours = []

            # Decrease cursor alpha for fade-out effect
            cursor_alpha = max(cursor_alpha - cursor_alpha_step, 0.0)

        canvas = background.copy()

        # Draw the gaze cursor with fade effect
        if x_pred is not None and y_pred is not None and cursor_alpha > 0:
            overlay = canvas.copy()
            cv2.circle(overlay, (x_pred, y_pred), 30, (0, 0, 255), -1)
            cv2.circle(overlay, (x_pred, y_pred), 25, (255, 255, 255), -1)
            cv2.addWeighted(
                overlay, cursor_alpha * 0.6, canvas, 1 - cursor_alpha * 0.6, 0, canvas
            )

        # Draw the camera feed
        small_frame = cv2.resize(frame, (cam_width, cam_height))
        frame_border = cv2.copyMakeBorder(
            small_frame, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=(255, 255, 255)
        )
        x_offset = screen_width - cam_width - 20
        y_offset = screen_height - cam_height - 20
        canvas[
            y_offset : y_offset + cam_height + 4, x_offset : x_offset + cam_width + 4
        ] = frame_border

        # FPS and blink indicator
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        font_color = (255, 255, 255)
        font_thickness = 2

        cv2.putText(
            canvas,
            f"FPS: {int(fps)}",
            (50, 50),
            font,
            font_scale,
            font_color,
            font_thickness,
            lineType=cv2.LINE_AA,
        )

        blink_text = "Blinking" if blink_detected else "Not Blinking"
        blink_color = (0, 0, 255) if blink_detected else (0, 255, 0)
        cv2.putText(
            canvas,
            blink_text,
            (50, 100),
            font,
            font_scale,
            blink_color,
            font_thickness,
            lineType=cv2.LINE_AA,
        )

        cv2.imshow("Gaze Estimation", canvas)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
