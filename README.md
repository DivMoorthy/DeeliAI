This is a tool that inputs in web-scraped + API fetched data (utilizing python playwright and google's Gemini) to get both qualitative and quantitative data regarding a 
company's financial statistics and then calculate an investment score (1 being poor and 10 being lucrative) based on a series of weighted metrics and rankings.

Some features include:
1. A 6-bucket metric system (individual functions) with 3 qualitative and 3 quantitative metrics. Each function currently evalautes one value (ex: size and valuation currently
   evaluates only TAM, however every function can be scaled to 3-4 submetrics each as planned in the linked metric spreadsheet below)
   Fully developed metrics plan: https://docs.google.com/spreadsheets/d/181XVMJgEUIjcpRgn1FoFlrMwOLjWbIkN/edit?usp=sharing&ouid=115915866111961084415&rtpof=true&sd=true
2. There is an error-handling function that has a default value autofill utilizing an API call to Gemini and previosuly evauluated companies that share similar data as a benchmark
3. When web-scraping for sources, there is a proximity based heirarchy for the credibility of a source: prioritizing direct data from financial documents such as 10k's and SEC filings,
   then evaluaiting analyst reports, and finally refering to 3rd party sources as a final resort before default-autofilling. Full plans for both he erorr-handling and source-ranking
   can be found here in a visual representation: https://www.figma.com/design/LiCbRnJEKJR7WNMhqg1VFc/Deeli-Market-Metric-Design?node-id=38-245&t=RnFuVy9OYBVTSkBE-1
   

Throughout the development of this tool there are some limiatations and considerations to keep in mind for suture usage in larger scaled projects:

Technical issues faced include:
1. fetching the documents after dowloading then and parsing throws an event loop closed error, and requirs a new call in order to function properly
2. python playwright can't identify the table structure linking within the SEC filings as it is not pure HTML and requires link keyword recognition rather than a table position
3. When fetchign the CIK, ensure that Gemini follows a specific format as written in to avoid potential naming issues with the pdf download later on

Other considerations:
1. SEC filings are updates quarterly at best so the information from this program is only as recent as the data allows for
2. In the event of a default alue autofill, the data is approximated and is not 100% accurate which may skew larger predictions
3. This program is only functional for companies that are actively filing taxes and are government compliant (meaning they have a CIK number)

