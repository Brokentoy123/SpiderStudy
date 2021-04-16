import cv2

bkg = cv2.imread('slide_bkg.png')

bkg = cv2.cvtColor(bkg, cv2.COLOR_BGR2GRAY)
cv2.imshow("img", bkg)

cv2.waitKey(0)
cv2.destroyAllWindows()
