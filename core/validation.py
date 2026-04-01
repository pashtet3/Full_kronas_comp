import json

def normalize_errors(data):
    result = {}

    errors = data.get("errors", {})
    if isinstance(errors, list):
        errors = {str(i): v for i, v in enumerate(errors)}

    if not isinstance(errors, dict):
        return result

    for detail_id, detail in errors.items():
        if not isinstance(detail, dict):
            continue

        result[detail_id] = []

        for section, section_value in detail.items():
            if isinstance(section_value, bool) or section_value is None:
                continue

            if isinstance(section_value, list):
                for group in section_value:
                    if isinstance(group, bool) or group is None:
                        continue

                    if isinstance(group, list):
                        for err in group:
                            if not isinstance(err, dict):
                                continue
                            if err.get("type") == "success":
                                continue

                            result[detail_id].append({
                                "section": section,
                                "index": str(err.get("index")),
                                "type": err.get("type"),
                                "message": err.get("message"),
                            })

                    elif isinstance(group, dict):
                        if group.get("type") != "success":
                            result[detail_id].append({
                                "section": section,
                                "index": str(group.get("index")),
                                "type": group.get("type"),
                                "message": group.get("message"),
                            })

            elif isinstance(section_value, dict):
                for key, arr in section_value.items():
                    if isinstance(arr, bool) or arr is None:
                        continue
                    if not isinstance(arr, list):
                        continue

                    for err in arr:
                        if not isinstance(err, dict):
                            continue
                        if err.get("type") == "success":
                            continue

                        result[detail_id].append({
                            "section": section,
                            "index": str(err.get("index")),
                            "type": err.get("type"),
                            "message": err.get("message"),
                        })

        result[detail_id].sort(
            key=lambda x: (x["section"], x["index"], x["type"], x["message"])
        )

    return result


def compare_validation(baseline, current):
    added = []
    removed = []

    all_details = set(baseline.keys()) | set(current.keys())

    for detail_id in all_details:
        base_list = baseline.get(detail_id, [])
        curr_list = current.get(detail_id, [])

        if not isinstance(base_list, list):
            base_list = []
        if not isinstance(curr_list, list):
            curr_list = []

        base_set = set(json.dumps(e, ensure_ascii=False) for e in base_list if isinstance(e, dict))
        curr_set = set(json.dumps(e, ensure_ascii=False) for e in curr_list if isinstance(e, dict))

        for e in curr_set - base_set:
            added.append({"detailId": detail_id, "error": json.loads(e)})

        for e in base_set - curr_set:
            removed.append({"detailId": detail_id, "error": json.loads(e)})

    return added, removed