from PyPDF2 import PdfReader, PdfWriter, Transformation, PdfFileWriter
import os


def get_pdf(pdf):
    return PdfReader(pdf)


def get_sample(pdf):
    return pdf.pages[0]


def get_sample_width_height(sample):
    sample_width = round(sample.mediabox.upperRight[0])
    sample_height = round(sample.mediabox.upperRight[1])
    return (sample_width, sample_height)


def get_number_of_original_pages(pdf):
    return len(pdf.pages)


def get_number_of_pages_needed_in_final_document(number_of_original_pages):
    return ((number_of_original_pages//2) + (number_of_original_pages % 2 > 0))


def get_odd_even_transformations(sample_height):
    odd_page_transformation = Transformation().scale(
        sx=0.5, sy=0.5).translate(tx=0, ty=sample_height/2)
    even_page_transformation = Transformation().scale(
        sx=0.5, sy=0.5).translate(tx=0, ty=0)
    return (odd_page_transformation, even_page_transformation)


def create_empty_pages_for_final_document(number_of_pages_needed, sample_width, sample_height):
    pdf = PdfFileWriter()
    file = open("temp_blank_pages.pdf", "wb")
    for i in range(number_of_pages_needed):
        pdf.addBlankPage(sample_width, sample_height)
    pdf.write(file)
    file.close()


def create_new_pdf(number_of_original_pages, number_of_pages_needed, blank_pdf,
                   odd_page_transformation, even_page_transformation, writer,
                   page_number, original_file_name):

    if (number_of_original_pages % 2) == 0:
        print("Document has even pages")
    else:
        print("Document has odd pages")

    for i in range(number_of_original_pages):

        if i == number_of_pages_needed:
            break

        print("============= i =", i, "loop started")

        blank_page = blank_pdf.pages[i]
        print("A")
        odd_page = original_pdf.pages[page_number+i]
        print("B")

        ###################################################
        # LINE THAT HAS ISSUE ON ODD NUMBER OF PDF PAGE
        even_page = original_pdf.pages[page_number+i+1]
        ###################################################

        print("C")

        odd_page.add_transformation(odd_page_transformation)
        print("D")
        even_page.add_transformation(even_page_transformation)
        print("E")

        blank_page.merge_page(odd_page)
        print("odd page", page_number+i, "added")
        blank_page.merge_page(even_page)
        print("even page", page_number+i+1, "added")

        writer.add_page(blank_page)
        page_number += 1
        print("--- i = ", i, "loop ended")

    with open(original_file_name+"_Notes_Version.pdf", "wb") as fp:
        writer.write(fp)


# filename = "CS50-36×27-Even.pdf"
filename = "CS106-25x19-Odd.pdf"
# filename = "PPG-27×21-Odd.pdf"


filename_without_extension = filename.split(sep=".")[0]
print(filename_without_extension)
original_pdf = get_pdf(filename)
writer = PdfWriter()
page_number = 0

# getting the required information
number_of_original_pages = get_number_of_original_pages(original_pdf)
number_of_pages_needed = get_number_of_pages_needed_in_final_document(
    number_of_original_pages)
sample = get_sample(original_pdf)
(width, height) = get_sample_width_height(sample)
(odd_page_transformation, even_page_transformation) = get_odd_even_transformations(height)

# creating empty pages that all other pages will merge into
create_empty_pages_for_final_document(
    number_of_pages_needed, width, height)

blank_pdf = get_pdf("temp_blank_pages.pdf")

create_new_pdf(number_of_original_pages, number_of_pages_needed, blank_pdf,
               odd_page_transformation, even_page_transformation, writer, page_number, filename_without_extension)

os.remove("temp_blank_pages.pdf")
