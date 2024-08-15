import requests


class SecEdgar:

    def __init__(self, fileurl):
        self.fileurl = fileurl
        self.headers = {'user-agent': 'Aymericknoah97@gmail.com'}

        # Load the company ticker data
        r = requests.get(self.fileurl, headers=self.headers)
        self.data = r.json()
        self.namedict = {}
        self.tickerdict = {}

    def get_filings(self, cik):
        """
        Retrieves the most recent filings for a given CIK number.
        """
        url = f'https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json'
        r = requests.get(url, headers=self.headers)

        if r.status_code == 200:
            filings = r.json()
            return filings['filings']['recent']
        else:
            print(f"Error: {r.status_code}")
            return None

    def annual_filing(self, cik, year):
        """
        Retrieves the 10-K filing for a given CIK and year.
        """
        filings = self.get_filings(cik)
        if filings:
            for i, filing_date in enumerate(filings['filingDate']):
                if year in filing_date and filings['form'][i] == '10-K':
                    accession_number = filings['accessionNumber'][i].replace("-", "")
                    primary_document = filings['primaryDocument'][i]
                    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"
                    return url
        return None

    def quarterly_filing(self, cik, year, quarter):
        """
        Retrieves the 10-Q filing for a given CIK, year, and quarter.
        """
        filings = self.get_filings(cik)
        if filings:
            for i, filing_date in enumerate(filings['filingDate']):
                if year in filing_date and filings['form'][i] == '10-Q':
                    accession_number = filings['accessionNumber'][i].replace("-", "")
                    primary_document = filings['primaryDocument'][i]
                    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{primary_document}"
                    return url
        return None


# Example usage:
se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

# Replace '320193' with a valid CIK number, and the year and quarter you want to retrieve.
annual_url = se.annual_filing('320193', '2023')
print(f"10-K Filing URL: {annual_url}")

quarterly_url = se.quarterly_filing('320193', '2023', '2')
print(f"10-Q Filing URL: {quarterly_url}")
