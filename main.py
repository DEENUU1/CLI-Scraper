import typer
from scrapers import xkom_scraper
from rich.console import Console


app = typer.Typer(
    name="CLI-Scraper",
    help="Scraping products from online stores",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()


@app.command(help="Scrape products from xkom.pl")
def xkom():
    """
    Return all products and prices in xkom.pl
    """
    xkom_products = xkom_scraper.scrape_xkom()
    if xkom_products:
        console.print(xkom_products)


if __name__ == "__main__":
    app()
