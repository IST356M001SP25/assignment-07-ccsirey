if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price: str) -> float:
    """Removes '$' and ',' and converts to float"""
    cleaned = price.replace("$", "").replace(",", "").strip()
    return float(cleaned)


def clean_scraped_text(scraped_text: str) -> list[str]:
    """Cleans scraped text by filtering out unwanted lines."""
    unwanted = {"NEW", "NEW!", "S", "V", "GS", "P"}
    lines = scraped_text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip() and line.strip() not in unwanted]
    return cleaned_lines


def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    """Creates a MenuItem object from title and scraped text."""
    cleaned = clean_scraped_text(scraped_text)

    name = cleaned[0]
    price = clean_price(cleaned[1])
    description = cleaned[2] if len(cleaned) > 2 else "No description available"

    return MenuItem(
        category=title,
        name=name,
        price=price,
        description=description
    )



if __name__=='__main__':
    pass
