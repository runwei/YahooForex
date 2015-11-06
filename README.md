# YahooForex
This program query the Yahoo Finance FOREX API every 5 seconds.

This is a non-blocking multi-threaded design, where we periodically create an thread sending HTTP requests. 

The HTTP requests are handled asynchronously.

Therefore, this program will not be blocked and is robust to network errors such as a HTTP timeouot.
