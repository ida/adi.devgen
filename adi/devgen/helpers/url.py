import urlparse


def getParamValsOfUrl(url, para_name):
    parsed_url = urlparse.urlparse(url)
    para_vals = urlparse.parse_qs(parsed_url.query)[para_name]
    return para_vals
