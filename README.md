Introduction
============

You can see this running (if the AWS server is up) at http://whattogiveher.com.

This used to work until Pinterest changed their entire site architecture. The current version uses an unofficial API since Pinterest doesn't have one yet. I'm not planning on working on this more until Pinterest releases an official API because I'm tired of rewriting it every time they change something.

How it works
============
It looks at all the pins of a user and creates a list of pins that contain buyable things by comparing it to a whitelist. Then it uses masonry.js to display the results. 

The version I had before Pinterest changed also looked the users closest 3 friends, scraped their pins, and did the same thing. If the pin belongs to the original user, we know they have seen it and like it. If it belongs to one of the 3 friends, we know that they may not have seen it but will probably like it. Monetization scheme involves using affiliate links for all products.
