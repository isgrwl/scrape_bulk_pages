import getopt
import sys
import random
import time
import json
from multiprocessing import Queue, Pool, Process, Manager, TimeoutError

from run_instance import run_instance
from scrape_page import scrape_page, DataRule
from dispatcher import RuleDispatch
'''
    TODO
    - 
'''
class BulkScrape:
    def __init__(self, opts={}):
        self.manager = Manager()
        self.results = self.manager.dict()  # scraper results (shared)
        self.urls = Queue()  # urls to scrape (shared)
        self.instances = []  # scraper processes

        self.ruleDispatch = RuleDispatch()

        self.num_instances = getattr(opts, "num_instances", 3)

    def start(self):
        # spawn multiple scraper instances
        for i in range(self.num_instances):
            #initialize each instance with a copy of ruledispatcher
            instance = Process(
                target=run_instance,
                args=(urls, results, i+1,self.ruleDispatch) 
            )
            instance.start()
            self.instances.append(instance)
            print(f"Spawned instance {i}")

        # wait for all processes to complete
        for instance in instances:
            instance.join()
            print(f"Instance exited")


if __name__ == "__main__":
    main()

