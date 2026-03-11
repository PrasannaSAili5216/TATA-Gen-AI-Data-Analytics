
from pptx import Presentation

try:
    prs = Presentation(r'd:\Projects\Forage TATA Intern\TASK_DETAILS\TASK_4\Presentation_Template.pptx')
    print(f"Total Layouts: {len(prs.slide_layouts)}")
    for i, layout in enumerate(prs.slide_layouts):
        print(f"Layout {i}: {layout.name}")
        for shape in layout.placeholders:
            print(f"  - Polder idx {shape.placeholder_format.idx}, type {shape.placeholder_format.type}")
except Exception as e:
    print(f"Error: {e}")
