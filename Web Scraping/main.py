import Webnovel as wb
import royalroad as rr

def scrape_links():
    wb.scrap_novels(500)
    rr.scrap_novels(500)

def add_details():
    wb.update_details()
    rr.update_details()

add_details()
