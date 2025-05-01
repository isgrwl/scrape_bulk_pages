from seleniumbase import SB

# initialize scraper and begin processing URLs with getData callback
def run_instance(urls, results, instance_num, getData=None,):
    with SB(
        uc=True,
        xvfb=False,
        headed=True,
        ad_block=True,
        page_load_strategy="eager",
        skip_js_waits=True,
        # block_images=True,
        # disable_js=True,
    ) as sb:
        sb.activate_cdp_mode()
        while True:
            try:
                url = urls.get(True, 3)  # get url from queue
                page = sb.cdp.get(url)  # navigate to url
                # run callback with browser context
                data = getData(sb, rules)
                results[url] = data  # store result

            except Exception as error:
                # no urls left, close instance
                print(error)
                print(f"Nothing left to scrape in instance {instance_num}")
                return

