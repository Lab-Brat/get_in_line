# get_in_line
### About
A program I wrote for myself to automate checking the status of an online application.  
Stack: Python, Selenium, OpenCV, PyTesseract, 2captcha.  
<br/>
In a nutshell, `Selenium` opens Firefox browser, fills out required fields in a form, 
solves captcha either locally with OCR (<30% accuracy), 
or using 2captcha online captcha solver(99% accuracy), 
clicks `Enter` and gets the resut.