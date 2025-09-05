# 🔐 PASSCHECKER

PASSCHECKER is a simple **Password Strength Assessment Tool** built in Python.<br>
It features:
- Random rotating ASCII banners with colorful text.
- Interactive password input (masked with asterisks ⭐).
- Strength analysis: **WEAK, MEDIUM, STRONG**.
- Actionable feedback on how to improve your password security.
- Repeat checks option (Y/N loop).


## Run the tool:

*python3 passchecker.py*


## Features

✅ Length check (minimum 8 characters).

✅ Uppercase, lowercase, digit, and special character detection.

✅ Password scoring (out of 5 criteria).

✅ Suggestions for stronger password creation.

## Example Output
WELCOME TO PASSCHECKER - A Simple Password Strength Tool

Enter the password to check: ********<br>
Password Strength Report
------------------------
Strength : MEDIUM<br>
Score    : 3/5 (60%)

Checks:
 - Length >= 8 : OK
 - Contains UPPERCASE letter  : YES
 - Contains lowercase letter  : YES
 - Contains digit             : NO
 - Contains special character : NO

Suggestions:
 * Add at least one digit (0-9).
 * Add at least one special character (e.g. !@#$%^&*).


## Requirements

 * Python 3.x

 * colorama

## Install dependencies:

*pip install colorama*


## Author

Ozichukwu Callistus Nonso<br>
Cybersecurity Analyst & Ethical Hacker<br>
*GitHub: Callistuschino*
