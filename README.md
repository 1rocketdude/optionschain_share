# optionschain_share
assemble a historical perspective on the options chain for a large number of equities

The goals of this project are rather simplistic; given the lack of free optionschain data, it is difficult to assemble a historical perspective on the options chain for a large number of equities. Available free sources of option chain data are limited (Yahoo Fianance, and maybe Google Fianance is still functional). The further limitation that this project seeks to address is the historical perspective. While possible to get historical end-of-day (EOD) open-close-high-low underlying data, optionchain data is only available for the current trading day.

This project hopes to provide a decentralized repository of historical options chain data that anyone could pull from to obtain historical perspective of options trading data. It depends on contributing users to pull the options chain data down routinely and storing it to a sharable cloud resource so that others can retrieve it at future dates.

This decentralized architecture is for personal, non-commercial activities meant to harness the power of the crowd to provide something not currently available. If used for commercial purposes, the project may have to be shut down.

See AAPL.pkl for the underlying and options chain for AAPL, downloaded from Yahoo finance at the end of the day 2018-11-30. Use python code such as the following to extract it:
    import pickle
    with open('AAPL.pkl','rb') as f:
        underlying = pickle.load(f)
        options_chain = pickle.load(f)

A portion of the options data and the underlying is shown in the file AAPL.json.

See the file discussion.docx for topics to consider. After a short period, I'll create a design.docx file describing how the archive will be organized and how the project will be managed.
