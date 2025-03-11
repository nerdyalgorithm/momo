import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import cv2
import mediapipe as mp
import threading

# Initialize Tkinter before loading GIFs
root = tk.Tk()
root.title("Mochi AI")
root.geometry("400x400")

# Load GIFs and preprocess frames
def load_gif_frames(file_path):
    """Load GIF frames after Tkinter root is initialized."""
    gif = Image.open(file_path)
    return [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

# Dictionary of preloaded frames (AFTER root is created)
gifs = {
    "happy": load_gif_frames("happy.gif"),
    "smile": load_gif_frames("smile.gif"),
    "resting": load_gif_frames("resting.gif"),
    "idle": load_gif_frames("idle.gif"),
    "leaving": load_gif_frames("leaving.gif"),
}

# Label to show GIF
gif_label = tk.Label(root)
gif_label.pack()

# Animation control variables
current_mood = "idle"
frame_index = 0

def animate():
    """Loop through frames of the current GIF."""
    global frame_index
    frame_index = (frame_index + 1) % len(gifs[current_mood])
    gif_label.config(image=gifs[current_mood][frame_index])
    root.after(100, animate)  # Adjust speed if needed

# Function to update GIF (only if mood changes)
def update_gif(mood):
    global current_mood, frame_index
    if mood != current_mood:
        current_mood = mood
        frame_index = 0  # Reset animation frame

# Start animation
animate()

# ---------------- FACE DETECTION SETUP ---------------- #
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

def detect_face():
    global current_mood
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        # Change mood only if it's different
        if results.detections:
            update_gif("happy")  # Face detected → happy GIF
        else:
            update_gif("idle")  # No face → idle GIF

        # Show face detection window
        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run face detection in a background thread
threading.Thread(target=detect_face, daemon=True).start()

root.mainloop()

    
    #The code above is a simple example of a virtual assistant that changes its mood based on whether a face is detected or not. The assistant can display different GIFs depending on the user's interaction. 
    #The program uses the  mediapipe  library for face detection and the  OpenCV  library for capturing video frames. The assistant displays different GIFs based on the presence of a face in the video stream. 
    #The program creates a simple GUI using the  tkinter  library to display the GIFs. It loads the GIFs as a list of frames and uses a label to display the frames in a loop. 
    ##The program also uses threading to run the face detection process in the background, allowing the GUI to update the GIFs based on the face detection results. 
    #To run the program, you need to have the required libraries installed. You can install them using the following commands: 
    #pip install mediapipe