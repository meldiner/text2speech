import cv2
import pytesseract
from gtts import gTTS
from io import BytesIO
import pygame
import time

# Set path to tesseract executable (if it's not in your system PATH)
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

def speak(text, lang='en'):
    # Create gTTS object and save as MP3 file
    tts = gTTS(text=text, lang=lang)

    # Create BytesIO object to hold the audio data in memory
    mp3_bytes = BytesIO()

    # Save the MP3 audio data to the BytesIO object
    tts.write_to_fp(mp3_bytes)

    # Reset the file pointer to the beginning of the buffer
    mp3_bytes.seek(0)

    # Play the MP3 audio data from the BytesIO object using Pygame
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_bytes)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue

def ocr(frame):
    # Convert the image to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply image thresholding to segment text from the background
    # _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours of text regions in the thresholded image
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Loop through each contour and extract the text
    # for contour in contours:
    #     # Get bounding box of contour
    #     x, y, w, h = cv2.boundingRect(contour)

    #     # Skip contours that are too small or too large
    #     if w < 10 or h < 10 or w > 1000 or h > 1000:
    #         continue
        
    #     # Extract the text from the bounding box using pytesseract
    #     text = pytesseract.image_to_string(gray[y:y+h, x:x+w])
        
    #     # Print the extracted text
    #     if text and len(text) > 3:
    #         print(text)
            
    #         # Speak the extracted text using text-to-speech
    #         speak(text)

    # Extract the text from the bounding box using pytesseract
    text = pytesseract.image_to_string(frame)

    return text


def main():
    # Set up video capture from default webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Set initial timestamp
    last_frame_time = time.time()

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Display the video frame
        cv2.imshow('Real-time Text-to-Speech', frame)

        # Calculate time since last frame was processed
        time_since_last_frame = time.time() - last_frame_time

        # Only process the frame if enough time has passed
        if time_since_last_frame >= 3:
            # Extract the text from the frame
            text = ocr(frame)
            
            # Print the extracted text
            if text and len(text) > 3:
                print(text)
                
                # Speak the extracted text using text-to-speech
                speak(text)

            # Update the timestamp
            last_frame_time = time.time()

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()