import os
import re
import sys
import fitz  # PyMuPDF Library
from collections import defaultdict


def sanitize_pdf_dynamic(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        return

    # 1. Open the document with PyMuPDF
    doc = fitz.open(input_path)
    page_count = len(doc)
    print(f"Opening {page_count} pages for analysis and sanitization...")

    # =========================================================================
    # PHASE 1: DYNAMIC DETECTION BY VOLUME ANOMALY (INTELLIGENT)
    # =========================================================================
    print("Analyzing font structure looking for massive patterns...")
    family_counts = defaultdict(set)

    for page in doc:
        for font in page.get_fonts():
            basefont = font[3]
            name = font[4]

            for font_name in [basefont, name]:
                if font_name:
                    # Clean subset prefixes like 'ABCDEF+'
                    clean_name = font_name.split("+")[-1]
                    # Get the base family before the hyphen (e.g., 'Helvetica' from 'Helvetica-5389020523')
                    base_family = clean_name.split("-")[0]
                    family_counts[base_family].add(font_name)

    detected_font_family = None
    max_variants = 0

    for family, variants in family_counts.items():
        if len(variants) > max_variants and len(variants) > 5:
            max_variants = len(variants)
            detected_font_family = family

    if not detected_font_family:
        print(
            "⚠️ No massive anomaly detected. Using 'Helvetica' by default."
        )
        detected_font_family = "Helvetica"
    else:
        print(
            f"Success! Intruder family dynamically identified: '{detected_font_family}' ({max_variants} variants detected)"
        )

    # =========================================================================
    # PHASE 2: COLLECTING ALL VARIANTS OF THE FOUND FAMILY
    # =========================================================================
    tags_set = set()
    for page in doc:
        for font in page.get_fonts():
            basefont = font[3]
            name = font[4]

            if detected_font_family in basefont:
                tags_set.add(basefont)
            if detected_font_family in name:
                tags_set.add(name)

    internal_code_tags = sorted(list(tags_set))
    print(
        f"Internal code tags ready to remove: {len(internal_code_tags)}"
    )

    if not internal_code_tags:
        print(
            f"No internal code signatures found associated with '{detected_font_family}'."
        )
        doc.close()
        return

    # =========================================================================
    # PHASE 3: MASSIVE OPTIMIZATION AND SINGLE-PASS REMOVAL
    # =========================================================================
    tags_bytes = [t.encode("utf-8") for t in internal_code_tags]
    combined_tags = b"|".join(re.escape(t) for t in tags_bytes)

    massive_font_pattern = re.compile(
        b"/(?:" + combined_tags + b")\\s+[\\d\\.\\s-]+Tf"
    )

    print("Applying massive sanitization on internal page streams...")
    for page in