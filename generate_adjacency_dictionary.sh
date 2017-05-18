#!/usr/bin/bash
rm -f links.json
cd ScrapyProject
scrapy crawl title --logfile scrap.log -o links.json
cat links.json | jq 'add' > ../adjacency_dictionary.json
