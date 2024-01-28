import os
import fitz
import pdfrw
import time

output_directory = "output"


def removeTexts(file, replacement_array):
    doc = fitz.open(file)
    rect_coords = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        for array in replacement_array:
            for replacement_text in array:
                text_instances = page.search_for(replacement_text)

                for rect in text_instances:
                    page.add_redact_annot(rect)
                    page.apply_redactions()
                    rect_coords.append([(rect.x0, rect.y0, rect.x1, rect.y1, page_num)])

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Build the full path to the output file
    output_path = os.path.join(output_directory, "added_input.pdf")
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    return rect_coords


def add_text_field(field_name, template_pdf, page, x, y, width, height):
    if not template_pdf.pages[page].Annots or not isinstance(
        template_pdf.pages[page].Annots, pdfrw.PdfArray
    ):
        template_pdf.pages[page].Annots = []

    y = float(template_pdf.pages[page].MediaBox[3]) - float(y)
    template_pdf.pages[page].Annots.append(
        pdfrw.PdfDict(
            Subtype=pdfrw.PdfName.Widget,
            FT=pdfrw.PdfName.Tx,
            Rect=pdfrw.PdfArray([x, y - height, x + width, y]),
            V="",
            T=field_name,
            DA="(Helvetica) 12",
        )
    )


def replaceTexts(file, target_texts):
    replacement_rects = removeTexts(file, target_texts)
    input_path = os.path.join(output_directory, "added_input.pdf")
    output_path = os.path.join(output_directory, "added_input.pdf")
    for i, rect in enumerate(replacement_rects):
        for j, ect in enumerate(rect):
            template_pdf = pdfrw.PdfReader(input_path)
            add_text_field(
                f"text_field{ect[4]}_{i}_{j}",
                template_pdf,
                ect[4],
                ect[0],
                ect[1],
                150,
                18,
            )
            pdfrw.PdfWriter().write(output_path, template_pdf)
            time.sleep(1)
    # Write the modified PDF to a new file after all modifications
    pdfrw.PdfWriter().write(output_path, template_pdf)
    return output_path
