# Plot usage

Run with python3 plot.py <args>

## Command line arguments for plot.py
- `--id` followed by a 4-digit id specifies the market id to plot
- `--plot-type` specifices the plot type. If none is specified, the `yes` option is used by default
	-- `--plot-type yes` plots the yes prices for the market
	-- `--plot-type no` plots the no prices for the market
	-- `--plot-type risk` plots the risk for the market (scaled up to 100)
- `--marketdata` followed by a directory containing all marketdata. If none is specified, `marketdata/` is used by default
- `--tweetdata` followed by a path to a JSON file containing tweet data may be specified to plot tweets over the original plot.
- `epoch-range` followed by a unix-epoch time range (e.g. `1577034796-1577046736`) will limit plotted data to the given range (both tweets and marketdata)



Example usage:

```
python3 plot.py --id 5328 --plot-type yes --marketdata marketdata/ --tweetdata trump_tweets.json --epoch-range 1577034796-1577046736
```

