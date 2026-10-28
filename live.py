"""One switch for the launch night (05.11.2026 01:00 Kyiv): False = the pre-launch wording ("Start 05.11, 01:00"), True = "Live now".
To roll out: set LIVE = True, run `python tools/make_og.py` (cards without the date), then `python build.py` (descriptions of the home pages,
new ?v= on every card), check, push."""
LIVE = False
