#!/usr/bin/env python3
import urllib.request
import lxml
import hashlib
import os
from difflib import Differ
from bs4 import BeautifulSoup

config = [
	{
		"title": "Stadt Münster - Impfung in Münster",
		"url": "https://www.muenster.de/corona_impfung.html",
		"selector": "div#inhalts-spalte > main"
	},
	{
		"title": "Stadt Münster - Corona: Die aktuell in Münster geltenden Regelungen",
		"url": "https://www.muenster.de/corona_aktuell.html",
		"selector": "div#inhalts-spalte > main"
	},
# 404 since 2021-06-07
#	{
#		"title": "KVWL - Impffahrplan für NRW",
#		"url": "https://www.corona-kvwl.de/patienteninfos/corona-schutzimpfung/impffahrplan-fuer-nrw",
#		"selector": "div.content-main"
#	},
	{
		"title": "MAGS - Corona-Schutzimpfung",
		"url": "https://www.mags.nrw/coronavirus-schutzimpfung",
		"selector": ".pane-content > article.node-full"
	},
	{
		"title": "KVWL - Terminbuchung in Westfalen-Lippe",
		"url": "https://impfterminservice-kvwl.service-now.com/",
		"selector": "div#root"
	}
]

cache_folder = "./cache/"
d = Differ()
def parse_and_compare(cfg):
	show_max_lines_per_diff = 25
	req = urllib.request.Request(cfg["url"], headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'})
	soup = BeautifulSoup(urllib.request.urlopen(req, timeout=15), 'lxml')
	ele = soup.select_one(cfg["selector"])
	content_stripped = ele.get_text("\n", strip=True)
	url_hash = hashlib.sha224(cfg["url"].encode()).hexdigest()
	diff_a = content_stripped.splitlines(keepends=True)
	website_cache_path = "{}/{}".format(cache_folder, url_hash)
	if not os.path.isfile(website_cache_path):
		with open(website_cache_path, "wb") as f:
			f.write(content_stripped.encode())
			f.close()
			print("Now tracking '{}' - {}".format(cfg["title"], cfg["url"]))
			print("")
	else:
		with open(website_cache_path, "rb") as f:
			content_cached = f.readlines()
			f.close()
		diff_b = [x.decode() for x in content_cached]
		diff_result = list(d.compare(diff_b, diff_a))
		changed_lines = [x for x in diff_result if (not x.startswith("  ") and not x.startswith("? "))]
		if changed_lines:
			print("Update for '{}' - {}".format(cfg["title"], cfg["url"]))
			print("".join(changed_lines[:show_max_lines_per_diff]).strip())
			if len(changed_lines) > show_max_lines_per_diff:
				print("(max. {} lines shown)".format(show_max_lines_per_diff))
			print("")
		# write update
		with open(website_cache_path, "wb") as f:
			f.write(content_stripped.encode())
			f.close()


for cfg in config:
	try:
		parse_and_compare(cfg)
	except Exception as e:
		print("Error with '{}' {}".format(cfg["title"], cfg["url"]))
		print(e)
		print("")
