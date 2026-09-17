import re
import tldextract
from urllib.parse import urlparse
import numpy as np

def extract_features(url):
    features = []
    
    # Length of URL
    features.append(len(url))
    
    # Count of special characters
    special_chars = ['-', '_', '@', '?', '%', '&', '=', '.']
    features.append(sum(url.count(char) for char in special_chars))

    # TLD length
    tld_info = tldextract.extract(url)
    features.append(len(tld_info.suffix))

    # Count of digits
    features.append(sum(c.isdigit() for c in url))

    # Presence of ‘https’
    features.append(1 if url.startswith("https") else 0)

    return np.array(features)