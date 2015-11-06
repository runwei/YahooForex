# YahooForex
This program query the Yahoo Finance FOREX API every 5 seconds
Every 5 seconds, we creates an thread sending HTTP requests. The HTTP requests are handled asynchronously.
Therefore, this program will not be blocked or has errors when there is a HTTP timeouot.
