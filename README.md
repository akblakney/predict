# Plot usage

Run with python3 plot.py <args>

## Command line arguments for plot.py
- `--id` followed by a 4-digit id specifies the market id to plot
- `--plot-type` specifices the plot type
	-- `--plot-type yes` plots the yes prices for the market
	-- `--plot-type no` plots the no prices for the market
	-- `--plot-type risk` plots the risk for the market (scaled up to 100)
- `--tweets` followed by a path to a JSON file containing tweet data may be specified to plot tweets over the original plot

Example usage:

```
python3 plot.py --id 5328 --plot-type yes -- tweets trump_tweets.json
```

