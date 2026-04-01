def normalize_calc(data):
    result = {}

    if not isinstance(data, list):
        return result

    for item in data:
        if not isinstance(item, dict):
            continue

        article = item.get("article")

        if not article:
            continue

        result[article] = {
            "qty": item.get("qty"),
            "price": item.get("price"),
            "sum": item.get("sum"),
        }

    return result


def compare_calc(baseline_raw, current_raw):
    baseline = normalize_calc(baseline_raw)
    current = normalize_calc(current_raw)

    added = []
    removed = []
    changed = []

    all_articles = set(baseline.keys()) | set(current.keys())

    for art in all_articles:
        b = baseline.get(art)
        c = current.get(art)

        if b and not c:
            removed.append({"article": art, "data": b})

        elif c and not b:
            added.append({"article": art, "data": c})

        else:
            if b != c:
                changed.append({
                    "article": art,
                    "changes": {
                        "qty": {"old": b["qty"], "new": c["qty"]},
                        "price": {"old": b["price"], "new": c["price"]},
                        "sum": {"old": b["sum"], "new": c["sum"]},
                    }
                })

    return added, removed, changed