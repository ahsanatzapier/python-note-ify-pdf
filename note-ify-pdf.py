import sys
try:
    from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
except:
    print("PyPDF2 package missing!")
    import sys
    import subprocess
    answer = input("Would you like to install it now? [Accepts: y or yes]: ")
    if answer.lower() in ["y", "yes"]:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "PyPDF2"])
            from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
        except:
            print("Something went wrong trying to install PyPDF2!")
            exit(1)
    else:
        exit(1)


def get_pdf(pdf):
    return PdfReader(pdf)


def get_filename_without_extension(filename):
    return filename.split(sep=".")[0]


def get_sample(pdf):
    return pdf.pages[0]


def get_sample_width_height(sample):
    sample_width = round(sample.mediabox.upperRight[0])
    sample_height = round(sample.mediabox.upperRight[1])
    return (sample_width, sample_height)


def get_number_of_pages(pdf_file):
    return len(pdf_file.pages)


def get_number_of_pages_needed_in_final_document(number_of_pages):
    return ((number_of_pages//2) + (number_of_pages % 2 > 0))


def get_even_or_odd(number_of_pages):
    return (number_of_pages % 2 == 0)


def get_odd_even_transformations(sample_height):
    odd_page_transformation = Transformation().scale(
        sx=0.5, sy=0.5).translate(tx=0, ty=sample_height/2)
    even_page_transformation = Transformation().scale(
        sx=0.5, sy=0.5).translate(tx=0, ty=0)
    return (odd_page_transformation, even_page_transformation)


def create_new_pdf(
    number_of_pages,
    number_of_pages_needed,
    pdf_file,
    document_is_even,
    width,
    height,
    odd_page_transformation,
    even_page_transformation,
    filename_without_extension
):
    pdf_writer = PdfWriter()
    page_number = 0

    for i in range(number_of_pages):

        if i == number_of_pages_needed:
            break

        blank_page = PageObject.createBlankPage(None, width, height)
        odd_page = pdf_file.pages[page_number+i]
        odd_page.add_transformation(odd_page_transformation)
        blank_page.merge_page(odd_page)

        if (i == (number_of_pages_needed - 1)) and not document_is_even:
            even_page = PageObject.createBlankPage(None, width, height)
        else:
            even_page = pdf_file.pages[page_number+i+1]
        even_page.add_transformation(even_page_transformation)
        blank_page.merge_page(even_page)
        pdf_writer.add_page(blank_page)
        page_number += 1

    with open(filename_without_extension+"_Notes_Version.pdf", "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)


def main():

    try:
        filename = sys.argv[1]
    except:
        print("You may have forgotten to add the filename! Run the program like this: note-ify-pdf.py <pdf_file>")
        sys.exit(1)

    try:

        filename_without_extension = get_filename_without_extension(filename)
        pdf_file = get_pdf(filename)

        number_of_pages = get_number_of_pages(pdf_file)

        number_of_pages_needed = get_number_of_pages_needed_in_final_document(
            number_of_pages)

        document_is_even = get_even_or_odd(number_of_pages)

        sample = get_sample(pdf_file)

        (width, height) = get_sample_width_height(sample)

        (odd_page_transformation,
         even_page_transformation
         ) = get_odd_even_transformations(height)

        create_new_pdf(
            number_of_pages,
            number_of_pages_needed,
            pdf_file,
            document_is_even,
            width,
            height,
            odd_page_transformation,
            even_page_transformation,
            filename_without_extension
        )

        print(filename, "has been note-ified successfully! - Your new PDF file is called:",
              filename_without_extension+"_Notes_Version.pdf")

    except:
        print("Something went wrong with the application!")
        exit(1)


main()
