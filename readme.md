##SECURITY ALERT APPLICATION

This is a Python Application where it will detect moving objects
and will alert the relevant person via email with a photo of the detected
object.

The algorithm here is we compare the very first frame with the frames after that (matrix comparison).
If any difference is detected we will use an algorithm to smooth that area, and we will draw some rectangles
and will find the rectangle around that object and will draw the rectangle on the current frame with the rectangle inside.

The algorithm is basically like classifying pixels based on a certain threshold

The moment the algorithm detects an object, an email will be sent with the captured image

There will be multiple images captured, and the best one will be emailed

This application also uses Threading.
