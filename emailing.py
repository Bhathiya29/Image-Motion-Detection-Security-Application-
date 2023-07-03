# Emailing.py will be responsible for the back-end part (emailing the detected photo from the webcam)
import smtplib  # The standard email sending library
from email.message import EmailMessage  # Since there is an attachment in the mail we need this library
import imghdr  # To get metadata about images

password = 'ngfsgwerwo123'
sender_email = 'youremailaccount@gmail.com'
receiver = 'youremailaccount@gmail.com'


def send_email(selected_image):
    email_message = EmailMessage()  # creating an object but this behaves like a dictionary
    email_message['Subject'] = 'New Image Detected'  # The subject of the mail
    email_message.set_content('Hey there was a new object that was detected')

    with open(selected_image, 'rb') as file:
        content = file.read()  # Reading the image file
    email_message.add_attachment(content, mainType='image',
                                 subType=imghdr.what(None, 'content'))  # Attaching the image file

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender_email, password)
    gmail.sendmail(sender_email, receiver, email_message.as_string())
    gmail.quit()
    

if __name__ == '__main__':
    send_email('Images/19.png')
