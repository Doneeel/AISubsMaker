from typing import List, Dict


def _justify_text(words: List[str], maxWidth: int) -> List[str]:
    """
    Justify a list of strings to a given width.
    """
    res, line, width = [], [], 0

    for w in words:
        if width + len(w) + len(line) > maxWidth:
            res, line, width = res + [" ".join(line)], [], 0
        line += [w]
        width += len(w)

    return res + [" ".join(line)]


def process_subs(subs: List[Dict], width: int = 15) -> List[Dict]:
    """
    Process a list of subtitles and timestamps.

    Width is for defining how much symbols should be on each chunk

    Example of chunk:
    {
        'timestamp': (0.0, 4.0),
        'text': 'The stale smell of old beer lingers.'
    }
    """
    processed = []

    for sub in subs:
        texts = _justify_text(sub["text"].strip().split(" "), width)
        difference = sub["timestamp"][1] - sub["timestamp"][0]
        step = difference / len(texts)

        stamp = sub["timestamp"][0]
        for text in texts:
            processed.append({"timestamp": (stamp, stamp + step), "text": text})
            stamp += step

    return processed
