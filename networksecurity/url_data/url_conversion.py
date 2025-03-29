import re
import socket
import requests
import whois
import tldextract
from googlesearch import search
from urllib.parse import urlparse
import os,sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import my_logger


class DomainInfo:
    def __init__(self):
        try :
            pass
        except Exception as e:
            my_logger.error(f"An error occurred: {str(e)}")
            raise NetworkSecurityException(e,sys)





    def check_ip_in_url(self,url):
    # """Check if URL contains an IP address."""
       ip_pattern = re.compile(r'^(?:http[s]?://)?(\d{1,3}\.){3}\d{1,3}')
       return 1 if ip_pattern.search(url) else -1

    def get_url_length(self,url):
       """Check if URL length is suspicious (>75 characters)."""
       return 1 if len(url) < 75 else -1

    def check_shortening_service(self,url):
        """Check if URL uses a shortening service (bit.ly, tinyurl, etc.)."""
        shortening_services = ["bit.ly", "goo.gl", "tinyurl", "t.co", "ow.ly"]
        return -1 if any(service in url for service in shortening_services) else 1

    def check_at_symbol(self,url):
        """Check if '@' symbol is present in the URL."""
        return -1 if "@" in url else 1

    def check_double_slash_redirecting(self,url):
        """Check for double slashes in the URL path."""
        return -1 if url.count("//") > 1 else 1

    def check_prefix_suffix(self,url):
        """Check if domain name has '-' (e.g., phishing-site.com)."""
        domain = urlparse(url).netloc
        return -1 if '-' in domain else 1

    def check_subdomain(self,url):
        """Count subdomains in URL."""
        ext = tldextract.extract(url)
        if ext.subdomain == "":
            return 1  # No subdomain
        elif ext.subdomain.count('.') == 1:
            return 0  # 1 subdomain
        else:
            return -1  # More than 1 subdomain

    def check_ssl_final_state(self,url):
        """Check if URL uses HTTPS."""
        return 1 if url.startswith("https://") else -1

    def get_domain_registration_length(self,url):
        """Check domain registration length (less than 1 year is risky)."""
        try:
            domain = urlparse(url).netloc
            whois_info = whois.whois(domain)
            expiry_date = whois_info.expiration_date
            if isinstance(expiry_date, list):
                expiry_date = expiry_date[0]
            registration_length = (expiry_date - whois_info.creation_date).days
            return 1 if registration_length > 365 else -1
        except:
            return -1  # Unable to fetch WHOIS

    def check_google_index(self,url):
        """Check if URL is indexed by Google."""
        try:
            query = f"site:{url}"
            for _ in search(query, num=1, stop=1):
                return 1
            return -1
        except:
            return -1

    def extract_features(self,url):
        """Extract all features from a given URL."""
        return [
            self.check_ip_in_url(url),
            self.get_url_length(url),
            self.check_shortening_service(url),
            self.check_at_symbol(url),
            self.check_double_slash_redirecting(url),
            self.check_prefix_suffix(url),
            self.check_subdomain(url),
            self.check_ssl_final_state(url),
            self.get_domain_registration_length(url),
            1,  # Placeholder for favicon (hard to check dynamically)
            1,  # Placeholder for port (hard to check dynamically)
            1,  # Placeholder for HTTPS_token
            1,  # Placeholder for Request_URL
            1,  # Placeholder for URL_of_Anchor
            1,  # Placeholder for Links_in_tags
            1,  # Placeholder for SFH
            1,  # Placeholder for Submitting_to_email
            1,  # Placeholder for Abnormal_URL
            1,  # Placeholder for Redirect
            1,  # Placeholder for on_mouseover
            1,  # Placeholder for RightClick
            1,  # Placeholder for popUpWindow
            1,  # Placeholder for Iframe
            1,  # Placeholder for age_of_domain
            1,  # Placeholder for DNSRecord
            1,  # Placeholder for web_traffic
            1,  # Placeholder for Page_Rank
            self.check_google_index(url),
            1,  # Placeholder for Links_pointing_to_page
            1,  # Placeholder for Statistical_report
    ]

# Example usage
# url = "https://example.com"
# obj = DomainInfo()
# features = obj.extract_features(url)
# print(features)
# print(f"shape of the feature vector: {len(features)}")
