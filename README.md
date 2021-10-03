# modulargrid-to-csv

Convert a modulargrid rack to a CSV file

I wanted a simple way to export my rack for inventory and simpler playing around in a spreadsheet. Knut doesn't want to create an API or have people scrape the site and I respect that, so I created this tool. It isn't that useful for scraping, but on a single rack it is good.

To create the input file, go to the data sheet view of your rack, view source, and save the source text to a file (like I said, wasn't making this too easy to do a bunch of racks).

invoke the tool with

    python mg_to_csv.py filname

the output will be a file with the *rack name*.csv

note: this tool is **very** dependant on the current HTML output from modulargrid and will totally fail when Knut updates it, so if you try it and it isn't working, check the source format against the files in the test directory.
