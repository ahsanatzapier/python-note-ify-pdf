# Usage

python3 note-ify-pdf.py <pdf_file>

# What is note-ify-pdf ?

note-ify-pdf is a Python application that takes in a PDF and samples the first pages to get the dimensions of the new PDF to be created. The app then iterates through every page in the pdf and applies scaling and transformations depending on if the page that's being iterated through is an odd or even page number. Error checking is also implemented where appropriate! The final result is a PDF with two slides on every page aligned vertically, with half the page dedicated to note-taking! To make the application easy to use, it takes the original file as an argument and outputs the new PDF as "original_pdf_file_Notes_Version.pdf."
