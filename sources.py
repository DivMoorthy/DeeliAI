
class RankSource:
    def select_most_credible_url(urls):
        """
        Takes a list of URLs and returns the one with the highest credibility
        based on a 3-tier ranking system.

        Returns:
            (best_url, credibility_level)
        """

    def get_credibility_level(url):
        url = url.lower()

        level_1_sources = [
            "sec.gov", "federalreserve.gov", ".gov", ".edu",
            "irs.gov", "whitehouse.gov", "nasa.gov", "data.gov",
            "nvidia.com", "intel.com", "microsoft.com"  # add official domains
        ]

        level_2_sources = [
            "yahoo.com", "bloomberg.com", "morningstar.com",
            "reuters.com", "marketwatch.com", "cnbc.com",
            "investopedia.com", "fool.com"
        ]

        level_3_keywords = [
            "wordpress", "medium", "substack", "quora", "reddit",
            "blogspot", "seekingalpha.com", "forum", "tumblr"
        ]

        for source in level_1_sources:
            if source in url:
                return 1

        for source in level_2_sources:
            if source in url:
                return 2

        for keyword in level_3_keywords:
            if keyword in url:
                return 3

        return 3  # default to lowest credibility if unknown

        # Rank all URLs
        ranked_urls = [(url, get_credibility_level(url)) for url in urls]

        # Sort by level (lowest number = highest credibility)
        ranked_urls.sort(key=lambda x: x[1])

        best_url, best_level = ranked_urls[0]
        return best_url, best_level
