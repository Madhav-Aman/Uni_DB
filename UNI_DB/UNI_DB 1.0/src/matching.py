import cv2
import io
import mysql.connector
import numpy as np
import cv2
import os
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from PIL import Image

def fingerprint_matching_score(uidai):
    # connect to the database
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
      database="uni_db"
    )

    # retrieve the fingerprint image from the database for the given UIDAI
    cursor = db.cursor()
    cursor.execute("SELECT fingerprint FROM registration WHERE UIDAI=%s", (uidai,))
    result = cursor.fetchone()

    if result is None:
        print(f"No fingerprint found for UIDAI {uidai}")
        return 0
    else:
        # read the blob image data into a NumPy array using OpenCV
        blob_image = result[0]
        nparr = np.frombuffer(blob_image, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # convert the image to JPG format using Pillow
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # save the converted image to the project directory
        output_path = f"{uidai}_fingerprint.jpg"
        pil_image.save(output_path, 'JPEG')
        print(f"Fingerprint image saved to {output_path}")

        # read the converted image from the local directory using OpenCV
        converted_image = cv2.imread(output_path)

        # pass the converted image to your function
        # your_function(converted_image)
        sample = cv2.imread(output_path)
        # sample = cv2.imread("3.jpg")
        # print(sample)

        ## Initialize fingerprint sensor
        try:
            f = PyFingerprint('COM5', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)


        ## Wait for 4 seconds to capture a good image
        time.sleep(2)
        ## Capture fingerprint image
        print('Place your finger on the sensor...')

        ## Wait for finger to be detected
        while ( f.readImage() == False ):
            pass

        ## Generate filename based on current date and time
        filename = time.strftime("%Y-%m-%d_%H-%M-%S") + ".bmp"

        ## Create directory if it doesn't exist
        directory = "e:/24-03-2023/DEMO1"
        if not os.path.exists(directory):
            os.makedirs(directory)

        ## Set destination path
        imageDestination = os.path.join(directory, filename)

        ## Download image to destination
        f.downloadImage(imageDestination)

        ## Read fingerprint image and process it using OpenCV
        fingerprint_image = cv2.imread(imageDestination)
        #Use SIFT algorithm to detect keypoints and descriptors in both images
        sift = cv2.SIFT_create()
        keypoints_1, descriptor_1 = sift.detectAndCompute(sample,None)
        keypoints_2, descriptor_2 = sift.detectAndCompute(fingerprint_image,None)

#Use FLANN-based matching to find matching keypoints between the two images
        matches = cv2.FlannBasedMatcher({'algorithm':1,'trees':40},{}).knnMatch(descriptor_1,descriptor_2,k=2)

#Filter out non-matching keypoints based on the distance ratio test
        match_points = []
        for p,q in matches:
            if p.distance < 0.8 *q.distance:
                match_points.append(p)

#Calculate the match score as the percentage of matched keypoints
                keypoints = 0
            if len(keypoints_1) < len(keypoints_2):
                keypoints = len(keypoints_1)
            else:
                keypoints = len(keypoints_2)

        score = len(match_points) / keypoints * 100
        print("Score: " + str(score))

#Remove temporary files
        os.remove(imageDestination)
        os.remove(output_path)

#Display the result image with matching keypoints
        result = cv2.drawMatches(sample, keypoints_1, fingerprint_image, keypoints_2, match_points, None)
        result = cv2.resize(result,None, fx=0.5, fy=0.5)
        cv2.imshow("Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#Return the match score
        return score


# if __name__ == "__main__":
    
#     a = input("enter the uidai number")
    
# print(fingerprint_matching_score(a))