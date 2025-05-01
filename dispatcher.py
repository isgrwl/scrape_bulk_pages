import re


class RuleDispatch:
    def __init__(self):
        # absorb match table
        self.urlMatcher = MatchTable()
        self.addRule = self.urlMatcher.addRule
        self.matchUrl = self.urlMatcher.matchUrl

        # initialize rules to execute
        self.selectors = {}

    def addSelector(self, label, field, qstr, single=True, postprocess=(lambda s: s)):
        selectors[label] = dict(
            field=field,
            qstr=qstr,
            single=single,
            postprocess=postprocess
        )


# TODO: support multiple patterns map to one label

# sample regex  \/.+amazon\.ca.+/gm\


class MatchTable:
    def __init__(self):
        self.matchRules = []

    def addRule(self, label, pattern):
        regex = re.compile(pattern)

        self.matches.append([label, regex])

    def matchUrl(url):
        scs = []
        for label, regex in self.matchRules:
            if regex.match(url):
                scs.append(label)
        return scs
