import cv2
import numpy as np

def align_images(im1, im2, max_features=500, good_match_percent=0.15):
    # Convert images to grayscale
    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(max_features)
    keypoints1, descriptors1 = orb.detectAndCompute(im1_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2_gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches = sorted(matches, key=lambda x: x.distance)

    # Remove not so good matches
    num_good_matches = int(len(matches) * good_match_percent)
    matches = matches[:num_good_matches]

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

    # Use homography
    height, width, channels = im1.shape
    im2_aligned = cv2.warpPerspective(im2, h, (width, height))

    return im2_aligned, h

if __name__ == "__main__":
    # Read reference image
    ref_filename = "./assets/tax_form_orig.png"
    print("Reading reference image : ", ref_filename)
    im1 = cv2.imread(ref_filename, cv2.IMREAD_COLOR)

    # Read image to be aligned
    im_filename = "./assets/tax_form_odd.png"
    print("Reading image to align : ", im_filename)
    im2 = cv2.imread(im_filename, cv2.IMREAD_COLOR)

    print("Aligning images ...")
    # Align images
    aligned_image, homography = align_images(im1, im2)

    # Write aligned image to disk.
    out_filename = "./assets/aligned.jpg"
    print("Saving aligned image : ", out_filename)
    cv2.imwrite(out_filename, aligned_image)

    print("Done.")
