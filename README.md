# Website Diff

This script prints the difference between websites on successive runs.

Requires Python 3.

The script is very basic, it just outputs a list of lines that have changed. Text passages are not abbreviated and there is no "inline diff", since the purpose was to simply notify myself of changes via the Telegram Bot API (the official Telegram clients do not support proper `diff` syntax highlighting). Due to this behaviour, messages of text with long sentences might end up quite long.

The list of websites is defined in [differ.py](differ.py) with `title`, `url` and `selector`. The `selector` is a CSS selector for the BeautifulSoup library, which is used to extract data of interest.

```
{
	"title": "Stadt Münster - Impfung in Münster",
	"url": "https://www.muenster.de/corona_impfung.html",
	"selector": "div#inhalts-spalte > main"
}
```

Example output:

>Update for 'Example diff' - https://www.example.com  
>\- Old line of text that was removed or changed.  
>\+ New line of text that has taken its place.  
>\+ Another added line of text.

## Setup

Create the folder `cache` in the script directory, ensure it is writable.

Environment setup:

```
python3 -m venv venv
source venv/bin/activate
pip install -r beautifulsoup4 lxml
```

Run as cronjob, this example pipes the results to a file and to a Telegram notification script:

```
# every day at 10 past full hour, in the hours between 07 to 19
10 7-19 * * * cd /home/you/webdiff/ && /home/you/webdiff/venv/bin/python /home/you/webdiff/differ.py | tee /tmp/webdifflog.txt | /usr/local/bin/telegr
```

## License

MIT
