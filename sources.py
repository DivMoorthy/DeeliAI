
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


"""
Hello Kevin, apologies for the late update, I was traveling this week and wasn't able to finish by Wed. night:

In terms of progress that I made this week:
- I succefully converted the github repo to provate, deleted the old one, and hid the API key in the gitignore file
- I debugged the playwright API to search within the SEC database, filter for 10k's based on unique company CIK numbers, and download the pdfs
-there is a new function called "scraper" that then scrapes the data from the downloaded pdf based on a keyword metric gien (called in main)
- finally I implemented the autfofill and source-ranking desings approved last time
-I have continues to learn about ADK, RAG and tool-calling, and thing we can move forawrd with them if needed
-Note: playwright can be buggy with downloading the files so there are many error-breaks within the code, sometimes it does not work but I am working towards fixing that issue

For you reference, here is the link to the Github repo: https://github.com/DivMoorthy/DeeliAI.git

Best, Divya



I just need to verify that each component works properly and do necessary adjustments, such as the case for 
the dox class to retrieve the PDF: It seems that it fails to locate the 10-K form due to the class data-testid="filing-row" not found.
Have a working minimal end-to-end pipeline by our meeting this week.
 We can keep the scope small and just focus on one sub-metric for each of the 6 metrics.


"""