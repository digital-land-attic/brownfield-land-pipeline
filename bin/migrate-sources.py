#!/usr/bin/env python3

#
#  migrate dataset/brownfield-land.csv into source and endpoint registers
#
import hashlib
import csv


collection_dir = "collection/"

# https://digital-land.github.io/specification/schema/source/
source_fieldnames = ["collection", "pipeline", "organisation", "endpoint", "documentation-url", "licence", "attribution", "start-date", "end-date"]
source = {}

endpoint_fieldnames = ["endpoint", "endpoint-url", "start-date", "end-date"]
endpoint = {}


def save(fieldnames, d, path):
    writer = csv.DictWriter(open(path, "w", newline=""), fieldnames=fieldnames)
    writer.writeheader()
    for key, row in sorted(d.items()):
        writer.writerow(row)


if __name__ == "__main__":
    for row in csv.DictReader(open('dataset/brownfield-land.csv')):
        endpoint_url = row["resource-url"]
        if endpoint_url:
            endpoint_key = hashlib.sha256(endpoint_url.encode("utf-8")).hexdigest()
            e = {
                "endpoint": endpoint_key,
                "endpoint-url": endpoint_url,
                "start-date": row["start-date"],
                "end-date": row["end-date"],
            }
            endpoint[endpoint_key] = e

        # organisation,documentation-url,resource-url,start-date,end-date
        s = {
            "collection": "brownfield-land",
            "pipeline": "brownfield-land",
            "organisation": row["organisation"],
            "documentation-url": row["documentation-url"],
            "endpoint": endpoint_key,
            "start-date": row["start-date"],
            "end-date": row["end-date"],
        }
        # order by, and uniqueness ..
        source_key = ":".join([s[f] for f in ["organisation", "start-date", "end-date", "documentation-url", "endpoint"]])
        source[source_key] = s

    save(source_fieldnames, source, "collection/source.csv")
    save(endpoint_fieldnames, endpoint, "collection/endpoint.csv")
