# USAGE
# With default parameters
#     python3 03_recognise.py
# OR specifying the encodings, screen resolution
#     python3 03_recognise.py -e encodings.pickle -r 240

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages

class Recognise:
    """Class for recognising faces for login feature including an intialization and run"""
    def __init__(self):  
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-e", "--encodings", default="./opencv/encodings.pickle",
            help="path to serialized db of facial encodings")
        ap.add_argument("-r", "--resolution", type=int, default=240,
            help="Resolution of the video feed")
        ap.add_argument("-d", "--detection-method", type=str, default="hog",
            help="face detection model to use: either `hog` or `cnn`")
        self.args = vars(ap.parse_args())

    def run(self, username):
        """Runs the facial recognition by loading saved images, starting the video stream and detecting if valid face for login"""
        # load the known faces and embeddings
        print("[INFO] loading encodings...")
        print(os.getcwd())
        data = pickle.loads(open(self.args["encodings"], "rb").read())

        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)

        # loop over frames from the video file stream
        while True:
            # grab the frame from the threaded video stream
            frame = vs.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = imutils.resize(frame, width = self.args["resolution"])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            boxes = face_recognition.face_locations(rgb, model = self.args["detection_method"])
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key = counts.get)

                # update the list of names
                names.append(name)

            # loop over the recognized faces
            for name in names:
                # print to console, identified person
                print("Person found: {}".format(name))
                if(name == username):
                    vs.stop()
                    return name
                elif(name == 'Unknown'):
                    vs.stop()
                    return False
                # Set a flag to sleep the cam for fixed time
                time.sleep(3.0)

##if __name__ == "__main__":
##    Recognise().run("S3661545")
