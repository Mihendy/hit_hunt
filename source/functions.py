def get_statistic_by(field, r_data):
    """Put statistics by themselves"""
    out = {}
    unique_out = {}
    for line in r_data:
        date = line["session_time"]
        day, month, year = date.day, date.month, date.year
        value = line[field]

        if year not in out:
            out[year] = {"total": 0, "by_month": {}}

        if year not in unique_out:
            unique_out[year] = {"unique": [], "length": 0}

        if value not in out[year]:
            out[year][value] = 0

        if value not in unique_out[year]["unique"]:
            unique_out[year]["unique"].append(value)
            unique_out[year]["length"] += 1
            unique_out[year]["by_month"] = {}

        if month not in out[year]["by_month"]:
            out[year]["by_month"][month] = {"total": 0, "by_day": {}}

        if month not in unique_out[year]["by_month"]:
            unique_out[year]["by_month"][month] = {"unique": [], "length": 0}

        if value not in out[year]["by_month"][month]:
            out[year]["by_month"][month][value] = 0

        if value not in unique_out[year]["by_month"][month]["unique"]:
            unique_out[year]["by_month"][month]["unique"].append(value)
            unique_out[year]["by_month"][month]["length"] += 1
            unique_out[year]["by_month"][month]["by_day"] = {}

        if day not in out[year]["by_month"][month]["by_day"]:
            out[year]["by_month"][month]["by_day"][day] = {"total": 0}

        if day not in unique_out[year]["by_month"][month]["by_day"]:
            unique_out[year]["by_month"][month]["by_day"][day] = {"unique": [], "length": 0}

        if value not in out[year]["by_month"][month]["by_day"][day]:
            out[year]["by_month"][month]["by_day"][day][value] = 0

        if value not in unique_out[year]["by_month"][month]["by_day"][day]["unique"]:
            unique_out[year]["by_month"][month]["by_day"][day]["unique"].append(value)
            unique_out[year]["by_month"][month]["by_day"][day]["length"] += 1

        out[year][value] += 1
        out[year]["total"] += 1
        out[year]["by_month"][month][value] += 1
        out[year]["by_month"][month]["total"] += 1
        out[year]["by_month"][month]["by_day"][day][value] += 1
        out[year]["by_month"][month]["by_day"][day]["total"] += 1

    return {"all": out, "unique": unique_out}
