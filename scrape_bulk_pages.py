'''


    TODO
    - cmdline options
    - test.py with amazon
'''

import getopt
import sys
import random
import time
import json
from multiprocessing import Queue, Pool, Process, Manager, TimeoutError
from seleniumbase import SB
from dispatcher import RuleDispatcher


class BulkScraper:
    def __init__(self, opts={}):
        self.manager = Manager()
        self.results = self.manager.dict()  # scraper results (shared)
        self.urls = Queue()  # urls to scrape (shared)

        self.instances = []  # scraper processes
        self.ruleDispatch = RuleDispatcher()

        self.num_instances = getattr(opts, "num_instances", 3)

    def start(self):
        # spawn multiple scraper instances
        for i in range(self.num_instances):
            # initialize each instance with a copy of ruledispatcher
            instance = Process(
                target=self.run_instance,
                args=(i+1)
            )
            instance.start()
            self.instances.append(instance)
            print(f"Spawned instance {i}")

        # wait for all processes to complete
        for instance in instances:
            instance.join()
            print(f"Instance exited")

    # initialize scraper and begin processing URLs with getData callback
    def run_instance(self, instance_id):
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
                    url = self.urls.get(True, 3)  # get url from queue
                    page = sb.cdp.get(url)  # navigate to url
                    # run callback with browser context
                    data = self.get_data(sb,url) #scrape results
                    self.results[url] = data  # store result

                except Exception as error:
                    # no urls left, close instance
                    print(error)
                    print(f"Nothing left to scrape in instance {instance_num}")
                    return

    def get_data(self, sb,url):
        selectors = self.ruleDispatch.getSelectorsForUrl(url)
        data = dict()
        for sel in selectors:
            try:
                # select first
                if rule.single:
                    tag = sb.cdp.select(rule.qstr)
                # select all
                else:
                    tag = sb.cdp.select_all(rule.qstr)

                # insert tag after postprocessing
                data[rule.field] = rule.postprocess(tag.text)

            except Exception as error:
                print(f"Couldn't get data for: {rule.field}")
                pass

        return data


if __name__ == "__main__":
    main()
