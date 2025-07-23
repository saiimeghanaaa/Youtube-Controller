import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

last_action_time = 0

# Gesture Logic Functions
def is_fist(landmarks):
    tips = [8, 12, 16, 20]
    return all(landmarks[tip].y > landmarks[tip - 2].y for tip in tips)

def detect_thumb_direction(landmarks):
    thumb_tip = landmarks[4].x
    wrist = landmarks[0].x
    if thumb_tip > wrist + 0.1:
        return "right"
    elif thumb_tip < wrist - 0.1:
        return "left"
    return "none"

def is_open_palm(landmarks):   
    tips = [8, 12, 16, 20]
    return all(landmarks[tip].y < landmarks[tip - 2].y for tip in tips)

def count_raised_fingers(landmarks):
    tips = [8, 12, 16, 20]
    return sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)

# Main Loop
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            landmarks = handLms.landmark

            current_time = time.time()
            if current_time - last_action_time > 1.5:

                if is_fist(landmarks):
                    print("✊ Fist → Play/Pause")
                    pyautogui.press("space")
                    last_action_time = current_time

                elif is_open_palm(landmarks):
                    print("✋ Open Palm → Mute/Unmute")
                    pyautogui.press("m")
                    last_action_time = current_timemml 

                else:
                    thumb_dir = detect_thumb_direction(landmarks)
                    if thumb_dir == "right":
                        print("👉 Thumb Right → Forward 10s")
                        pyautogui.press("l")  # Seek forward
                        last_action_time = current_time
                    elif thumb_dir == "left":
                        print("👈 Thumb Left → Rewind 10s")
                        pyautogui.press("j")  # Seek backward
                        last_action_time = current_time

                    finger_count = count_raised_fingers(landmarks)
                    if finger_count == 1:
                        print("☝️ One Finger → Volume Up")
                        pyautogui.press("volumeup")
                        last_action_time = current_time
                    elif finger_count == 2:
                        print("✌️ Two Fingers → Volume Down")
                        pyautogui.press("volumedown")
                        last_action_time = current_time

    cv2.imshow("Gesture Controlled YouTube", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
