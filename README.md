# Saving market and tweet data to Pandas DataFrame

`save_marketdata.py` has functionality for saving marketdata and tweet data
to a csv file (to be read as a Pandas DataFrame)
Run with python3 `save_marketdata.py <args>`

<!-- ## Command line arguments for plot.py
- `--id` followed by a 4-digit id specifies the market id to plot
- `--plot-type` specifices the plot type. If none is specified, the `yes` option is used by default
	-- `--plot-type yes` plots the yes prices for the market
	-- `--plot-type no` plots the no prices for the market
	-- `--plot-type risk` plots the risk for the market (scaled up to 100)
- `--marketdata` followed by a directory containing all marketdata. If none is specified, `marketdata/` is used by default
- `--tweetdata` followed by a path to a JSON file containing tweet data may be specified to plot tweets over the original plot.
- `epoch-range` followed by a unix-epoch time range (e.g. `1577034796-1577046736`) will limit plotted data to the given range (both tweets and marketdata) -->

## Command line arguments for save_marketdata.py
- `--id` (required) specifies the market id to plot
- `--marketdata` gives the path to the marketdata directory (default is `marketdata/`)
- `--tweetdata` gives the path to the twitterdata in json format
<!-- - `--tweet-interval` -->
- `--epoch-range` gives range in unix time to be considered (e.g.  `1577034796-1577046736`)
- `--filename` gives the filename to save data to

## Format of Pandas DataFrame
- index is the unix time stamps by default;
- one column for each market outcome, with the YES prices at that time-stamp
- `tweets` column which contains number of tweets during the specified interval
(intervals are one minute long)
- additional columns called `unix` and `date` which have unix timestamps and
convenient date-times respectively

Example usage:

```
python3 save_marketdata.py --id 6422 --marketdata marketdata/ --tweetdata tweets.json --epoch-range 1577034796-1577046736
```

# Plotting Data

`plot_both.py` plots both market and tweet data
