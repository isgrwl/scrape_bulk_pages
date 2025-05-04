import re

class RuleDispatcher:
    def __init__(self):
        # string patterns which map to a label, eg "amazon.com/*/gm/* -> amazon_product"
        self.urlPatterns = []
        self.extractRules = defaultdict(list)  # rules to execute on each label

    # get selectors to run, from url
    def getSelectorsForUrl(self, url):
        selectors = []
        labels = matchUrlPattern(url)
        for label in labels:
            selectors.append(self.extractRules[label])
        return selectors

    # add patterns which map to a label
    def addUrlPattern(self, pattern, label):
        regex = re.compile(pattern)

        self.matches.append([label, regex])

    # get matching labels from a url
    def matchUrlPattern(self, url):
        labels = {}
        for label, regex in self.matchRules:
            if regex.match(url):
                labels.append(label)
        return labels

    # label data with css selector
    def addExtractRule(self, label, field, selector, single=True, postprocess=(lambda s: s)):
        self.extractRules[label].extend(dict(
            field=field,
            selector=selector,
            single=single,
            postprocess=postprocess
        ))
