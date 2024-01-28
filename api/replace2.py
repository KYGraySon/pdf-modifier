import fitz
import pdfrw
import time


def replaceText(file, replacement_array):
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

    doc.save("output.pdf", garbage=4, deflate=True, clean=True)
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


if __name__ == "__main__":
    replacement_rects = replaceText(
        "input.pdf", [["[[Signature_1]]"], ["[[Signature_2]]"], ["[[Signature_3]]"]]
    )
print(replacement_rects)

for i, rect in enumerate(replacement_rects):
    for j, ect in enumerate(rect):
        template_pdf = pdfrw.PdfReader("output.pdf")
        add_text_field(
            f"text_field{ect[4]}_{i}_{j}",
            template_pdf,
            ect[4],
            ect[0],
            ect[1],
            150,
            18,
        )
        pdfrw.PdfWriter().write("output.pdf", template_pdf)
# Write the modified PDF to a new file after all modifications
pdfrw.PdfWriter().write("output.pdf", template_pdf)