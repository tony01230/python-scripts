# python-scripts
just a random collection of python scripts - check the readme

# Img2PDF Script (pdfv5.1.py)
A script that automates the queuing and production of PDFs from a numbered list of images.
I.e. I have images named, 1-250.jpg, I can place this script into the directory and it will automatically find the number of files that fit into a predetermined file size.

__Situation 1__
After running the script, it produced a single PDF named after the directory. It houses my images 1-250.

__Situation 2__
During the production of the files, it incounters multiple memory errors. It decreases my predetermined filesize by 5MB. I receive 2 PDFs named after the directory and with a " - 1" appended onto the end.

__Situation 3__
During the production of the files, it incounters over 25 memory errors. The script closes without warning. Running the script in CMD states that it has reached the limit of errors.

[Download the latest release!](scripts/pdfv5.1.py)

# BruteForce Password PHP (bruteforcepass.py)
A script that takes advantage of a sequential password sequence. I.e. a date?! Uses a bruteforce technique to guess the password and bombard a php server with 365 * # of years of requests.

[Download the latest release!](scripts/bruteforcepass.py)

# ContentStealer
A script that reuploads content stolen from other youtube channels.

[Read the README.md for more information.](scripts/contentstealer)
