import os
import fitz


def replaceText(file, target, replacement):
    doc = fitz.open(file)
    rect_coords = []
    output_directory = "output"

    for page_num in range(len(doc)):
        page = doc[page_num]

        text_instances = page.search_for(target)
        for rect in text_instances:
            if rect[0]:
                page.add_redact_annot(rect)
                page.apply_redactions()
                rect_coords.append((rect.x0, rect.y0, rect.x1, rect.y1, page_num))
                page.draw_rect(
                    fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1),
                    fill=(1, 1, 1),
                    width=0,
                )
                page.add_freetext_annot(
                    (rect.x0, rect.y0, rect.x1, rect.y1),
                    replacement,
                    fontname="helv",
                    fontsize=12,
                    text_color=(0, 0, 0),
                )
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Build the full path to the output file
    output_path = os.path.join(output_directory, "replace_name.pdf")

    doc.save(output_path, garbage=4, deflate=True, clean=True)
    return output_path


# if __name__ == "__main__":
#     replacement_rects = replaceText("input.pdf", "{{Full name}}", "Adam")
