"""Un emoji coupé en deux par une source (moitié de paire UTF-16) ne doit plus
faire planter l'écriture des fichiers (robot du 2026-11-13 : UnicodeEncodeError
dans json.dump, aucune donnée publiée ce jour-là)."""
import json
from datetime import date, timedelta

import scrape


def _ev(**kw):
    day = (date.today() + timedelta(days=3)).isoformat()
    base = dict(id="0123456789ab", title="Atelier makesense", date=day, time="18:00", end_time="19:30",
                institution="makesense", discipline="Sociologie", location="Paris", price="0",
                description="", speaker="", image="", source_type="association",
                url="https://example.org/atelier")
    base.update(kw)
    return base


def test_lone_surrogate_removed_and_valid_pairs_kept():
    lone = chr(0xD83D)
    evts = scrape.finalize_events([_ev(description="Rejoignez-nous " + lone + " dès 18h \U0001F600")])
    desc = evts[0]["description"]
    assert lone not in desc
    assert "\U0001F600" in desc
    desc.encode("utf-8")
    json.dumps(evts, ensure_ascii=False).encode("utf-8")
