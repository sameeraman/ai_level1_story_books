from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ----------------------------
# CONFIG
# ----------------------------
image_files = ["mermaid_story_1.png", "mermaid_story_2.png"]  # Replace with your actual image filenames
border_px = 5  # Adjust this to remove dividing borders (set to 0 if no borders)


pdf_title = "Marina the Mermaid"
output_pdf = "mermaid_Storybook.pdf"

# Each entry is a tuple of (line1, line2)
page_texts = [
    ("Marina the mermaid had a red fin.", "She sat on a big rock and sang a sad song."),
    ("“Hop, hop,” said a crab.", "“Why are you sad?”"),
    ("“I had a pet,” said Marina.", "“A fat cat. He ran far.”"),
    ("“Did he go in a van?”", "No,” said Marina. “He hid in a net.”"),
    ("The crab had a plan.", "“Let's get the cat!”"),
    ("Marina and the crab swam to the net.", "“Cat!” she said. “Get up!”"),
    ("The cat got up.", "He had mud on his leg."),
    ("Marina gave the cat a hug.", "“Now I am not sad,” she said.")
]


# ----------------------------
# SPLIT IMAGE INTO 4 PANELS
# ----------------------------
def split_image_into_4(img_path, border=0):
    img = Image.open(img_path)
    width, height = img.size
    w_half = width // 2
    h_half = height // 2

    panels = [
        img.crop((0 + border, 0 + border, w_half - border, h_half - border)),
        img.crop((w_half + border, 0 + border, width - border, h_half - border)),
        img.crop((0 + border, h_half + border, w_half - border, height - border)),
        img.crop((w_half + border, h_half + border, width - border, height - border))
    ]
    return panels

# Gather all 8 panels
panels = []
for file in image_files:
    panels.extend(split_image_into_4(file, border=border_px))

# register fonts
pdfmetrics.registerFont(TTFont('Andika-Bold', 'Andika-Bold.ttf'))


# ----------------------------
# CREATE PDF
# ----------------------------
c = canvas.Canvas(output_pdf, pagesize=A4)
page_width, page_height = A4

# --- Title Page ---
c.setFont("Andika-Bold", 34)
c.drawCentredString(page_width / 2, page_height / 2, pdf_title)
c.showPage()

# --- Story Pages ---
for idx, panel in enumerate(panels):
    img_reader = ImageReader(panel)

    # Resize image to fit top portion of page
    max_img_height = page_height * 0.35
    max_img_width = page_width * 0.55
    img_width, img_height = panel.size
    scale = min(max_img_width / img_width, max_img_height / img_height)
    disp_width = img_width * scale
    disp_height = img_height * scale

    img_x = (page_width - disp_width) / 2
    #img_y = page_height - disp_height - 50
    img_y = (page_height - disp_height) /2 
    
    c.drawImage(img_reader, img_x, img_y, width=disp_width, height=disp_height)

    # Add two lines of text below the image
    line1, line2 = page_texts[idx]
    text_y_start = img_y - 50
    c.setFont("Andika-Bold", 24)
    c.drawCentredString(page_width / 2, text_y_start, line1)
    c.drawCentredString(page_width / 2, text_y_start - 36, line2)

    c.showPage()

c.save()
print(f"PDF saved as {output_pdf}")
