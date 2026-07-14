import re

text = "The Coffee Concept Rau द कॉफी कॉन्सेप्ट, राऊ 4.2 (1,829) · ₹200–400 · Dine-in · Takeout · Delivery · Coffee shop Overview Menu Reviews About"

category_candidate = ""
cat_match = re.search(r'([1-5]\.\d)\s*\([\d,]+\)\s*(?:·\s*[^·]+)?·\s*([^·\n]{2,30})', text)
if cat_match:
    category_candidate = cat_match.group(2).strip()
    print("Initial match:", category_candidate)
    if any(x in category_candidate for x in ["Dine-in", "Takeout", "Delivery"]):
        parts = text.split("·")
        for p in parts:
            p_clean = p.strip()
            # Clean up checkmarks/unicode
            p_clean = re.sub(r'[^\w\s-]', '', p_clean).strip()
            # Remove navigation words
            p_clean = re.sub(r'\b(Overview|Menu|Reviews|About|Directions|Save|Nearby|Share)\b', '', p_clean, flags=re.I).strip()
            if p_clean and not any(x in p_clean for x in ["Dine-in", "Takeout", "Delivery"]):
                # check if it contains rupees or dollars
                if not any(c in p_clean for c in ["₹", "$"]) and not re.search(r'\d', p_clean):
                    words = p_clean.split()
                    if len(words) <= 3 and len(p_clean) < 30:
                        category_candidate = p_clean
                        break

print("Cleaned Category:", category_candidate)
