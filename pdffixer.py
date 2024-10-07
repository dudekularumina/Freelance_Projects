import asyncio
import os
import pdfplumber
from playwright.async_api import Page, Playwright, async_playwright
from harambe import SDK

async def scrape(sdk: SDK, current_url: str, context: dict, *args: Any, **kwargs: Any) -> None:
    # Playwright page
    page: Page = sdk.page
    
    # Wait for the PDF download button to appear
    await page.wait_for_selector("#pdfdoc")
    
    # Click on the download button
    download_button = await page.query_selector("button#pdfdoc")
    
    # Initiate the download
    pdf_download = await page.wait_for_event("download", lambda download: download.suggested_filename.endswith('.pdf'))
    await download_button.click()

    # Save the PDF to a local path
    download_path = os.path.join(os.getcwd(), "downloaded_pdf.pdf")
    await pdf_download.save_as(download_path)
    print(f"PDF downloaded to: {download_path}")
    
    # Extract text from the PDF using pdfplumber
    extract_text_from_pdf(download_path, context)

def extract_text_from_pdf(pdf_path: str, context: dict) -> None:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                full_text += f"\n\n--- Page {page_num + 1} ---\n{text}"
            
            # Save the extracted text
            save_extracted_text(full_text, context)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")

def save_extracted_text(text: str, context: dict) -> None:
    # Define output path and save the extracted text
    output_file = os.path.join(os.getcwd(), "extracted_text.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {context.get('title', 'No Title')}\n\n")
        f.write(text)
    print(f"Text extracted and saved to: {output_file}")

async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        
        sdk = SDK(page)  # Create SDK instance
        context = {"title": "Sample PDF Document"}
        
        await scrape(sdk, "https://indiankanoon.org/doc/1690805/", context)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
