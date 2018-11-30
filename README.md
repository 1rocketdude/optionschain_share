# optionschain_share
assemble a historical perspective on the options chain for a large number of equities

The goals of this project are rather simplistic; given the lack of free optionschain data, it is difficult to assemble a historical perspective on the options chain for a large number of equities. Available free sources of option chain data are limited (Yahoo Fianance, and maybe Google Fianance is still functional). The further limitation that this project seeks to address is the historical perspective. While possible to get historical end-of-day (EOD) open-close-high-low underlying data, optionchain data is only available for the current trading day.

This project hopes to provide a decentralized repository of historical options chain data that anyone could pull from to obtain historical perspective of options trading data. It depends on contributing users to pull the options chain data down routinely and storing it to a sharable cloud resource so that others can retrieve it at future dates.

This decentralized architecture is for personal, non-commercial activities meant to harness the power of the crowd to provide something not currently available. If used for commercial purposes, the project may have to be shut down.

Questions as to implementation:
	1. what format to store the optionchain data in to make retrieval simplistic, bandwidth efficient, and automatable? Some alternatives:
		a. one sqlite3 database for each symbol, which has an underlying table and a linked options table that can be parsed by any software that understands sqlite3 tables. An example table definition is contained in the next section. This has the advantage of simplifying storage (one directory of symbols, each containing the entire historical record in a way that makes querries simple. Software experience required.
		b. a python pickle'd binary file for each symbol, for each trading day. A lot of us use python, so getting the data out is trivial. Restrictive to users that don't use python. Also adds the complexity of a directory structure that is now two levels deep. This is perhaps not a big deal. The top level directory could be the symbol, followed by dates containing each trading days option chain.
		c. much as above, but using a JSON file. This is the format of the original data from Yahoo or Google. Perhaps to save bandwidth and storage, a directory of JSON files for each symbol is stored as a 7zip archive.

	2. cloud storage. Many providers give away 5-20 GB of online storage. There are interfaces to all of these that would allow a user to rsync (bandwidth efficiently) grab updates to a directory full of symbol option chains. A useful tool to use may be https://rclone.org/, which looks to be cloud agnostic. If Alice used Dropbox to store her 100 symbols, but Fred used Amazon's S3 to store his 125 symbols, then anyone could access these public shares in anyway they wished, but we would encourage a bandwidth efficient method such as rclone, in order to not get someone kicked off their free cloud storage.

	3. decentralized approach: most investors concern themselves with a few hundred different symbols. Downloading options chains data for a few hundred symbols on a nominal home broadband connection takes several minutes. Keeping and sharing these datasets with others allows a larger audience and a larger historical record to be shared. We should encourage other contributors to first scan other users directories for symbols before creating another archive of the same symbol. How many users have to download the options chain for GOOGL each day? The nominative answer, of course, is one.

Example sqlite3 database tables for underlying and options chain. Note that only a portion of the options chain information collected is ingested in these tables. This argues for using an alternative format that includes all the options chain data, such as a JSON file.

CREATE TABLE Underlying(
                             rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                             utc_timestamp INTEGER NOT NULL,
                             volume INTEGER NOT NULL,
                             AverageDailyVolume INTEGER NOT NULL,
                             bid REAL,
                             ask REAL,
                             last REAL NOT NULL,
                             Open REAL NOT NULL,
                             PreviousClose REAL NOT NULL,
                             PriceBook REAL,
                             PERatio REAL,
                             FiftydayMovingAverage REAL,
                             TwoHundreddayMovingAverage REAL,
                             YearHigh REAL,
                             YearLow REAL,
                             utc_datestr TEXT DEFAULT NULL,
                             earningsTimestamp INTEGER DEFAULT NULL,
                             averageDailyVolume10Day INTEGER DEFAULT NULL,
                             averageDailyVolume3Month INTEGER DEFAULT NULL,
                             epsForward REAL DEFAULT NULL,
                             epsTrailingTwelveMonths REAL DEFAULT NULL,
                             forwardPE REAL DEFAULT NULL,
                             trailingPE REAL DEFAULT NULL);

CREATE TABLE Option(
                              rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                              underlying_id INTEGER NOT NULL,
                              expiration_jday INTEGER NOT NULL,
                              strike_price REAL NOT NULL,
                              type TEXT NOT NULL,
                              volume INTEGER NOT NULL,
                              open_interest INTEGER NOT NULL,
                              last REAL NOT NULL,
                              bid REAL,
                              ask REAL,
                              expiration_datestr TEXT DEFAULT NULL,
                              impliedVolatility REAL NOT NULL DEFAULT 0.0,
                              FOREIGN KEY(underlying_id) REFERENCES Underlying(rowid) );

Example python code to download Yahoo optionschain data:
import requests
import demjson
url = 'https://query1.finance.yahoo.com/v7/finance/options/GOOGL'
r = requests.get(url, timeout=20)
opt = demjson.decode(r.text)
underlying = opt['optionChain']['result'][0]['quote']
chain = opt['optionChain']['result'][0]['options'][0]
expiration_seconds = opt['optionChain']['result'][0]['expirationDates']

then iterate over expiration_seconds for the optionschains for other expiry months.

