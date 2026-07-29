from playwright.sync_api import sync_playwright
import sys
from bs4 import BeautifulSoup
from scanner.emulation_lab import get_wallet_emulation_script


def playwright_scrape_emulation(url):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()
        page.set_extra_http_headers({

            "User-Agent":
            "Mozilla/5.0"
            
        })

        requests_data = []

        responses_data =[]

        def capture_request(request):

            requests_data.append({

                "url": request.url,

                "method": request.method,

                "resource_type": request.resource_type
            })

        def capture_response(response):

            try:

                content_type = response.headers.get(
                    "content-type",
                    ""
                )

                if "application/json" in content_type:

                    body = response.text()

                    responses_data.append({

                        "url": response.url,

                        "status": response.status,

                        "content_type": content_type,

                        "body": body[:2000]

                    })

            except:

                pass

        page.on(

            "request",

            capture_request
        )   

        page.on(

            "response",

            capture_response
        ) 

        #Hook Interceptor

        page.add_init_script("""

        window.__wallet_requests__ = [];

        Object.defineProperty(window, 'ethereum', {

           set(value) {

            if(value && value.request){

                const originalRequest = value.request.bind(value);

                value.request = async function(args){

                    window.__wallet_requests__.push(args);
                    return originalRequest(args);

                }
                             
            }

             this.__ethereum = value;

    },

    get() {

        return this.__ethereum;

    }

});

""")    
        
        # START EMULATION LOGGING


        fake_log = open(

            "storage/fake_runtime_dump.txt",

            "w",

            encoding="utf-8"

        )

        original_stdout = sys.stdout

        sys.stdout = fake_log

        page.add_init_script(

            get_wallet_emulation_script()

        )                                 
                                                                       
        try:

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

        except Exception as e:

            print(
                f"Playwright failed: {url}"
            )

            print(e)

            return {
                "network_requests": [],
                "network_responses": [],
                "wallet_requests": []
            }

        page.wait_for_timeout(
            10000
        )

        ethereum_data = page.evaluate("""
        () => {

            if(window.ethereum){

                return {

                    detected: true,

                    keys: Object.keys(window.ethereum),

                    isMetaMask: window.ethereum.isMetaMask || false

                }

            }

            return {
                detected: false
            }

        }
        """)

        wallet_requests = page.evaluate("""

() => {

    return window.__wallet_requests__ || [];

}

    """)

        print(ethereum_data)

        print(wallet_requests)

        sys.stdout = original_stdout

        fake_log.close()       
                                                                    

        # FULL RENDERED HTML
        html = page.content()

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # TITLE
        title = soup.title.string if soup.title else "No Title"

        # TEXT
        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # LINKS
        links = []

        for link in soup.find_all("a"):

            href = link.get("href")

            if href:
                links.append(href)

        # SCRIPTS
        scripts = []

        for script in soup.find_all("script"):

            src = script.get("src")

            if src:
                scripts.append(src)

        # IMAGES
        images = []

        for img in soup.find_all("img"):

            src = img.get("src")

            if src:
                images.append(src)

        browser.close()

        return {

            "title": title,

            "text_sample": text[:2000],

            "links": links[:20],

            "scripts": scripts[:20],

            "images": images[:20],

            "network_requests": requests_data[:100],

            "ethereum_runtime": ethereum_data,

            "network_responses": responses_data[:50],

            "wallet_requests": wallet_requests

        }
    