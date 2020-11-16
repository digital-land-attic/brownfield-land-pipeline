import re
import csv


class HarmoniseCallback:
    organisation_uri = {}
    end_of_uri_regex = re.compile(r".*/")

    def init(self):
        for row in csv.DictReader(open("var/cache/organisation.csv", newline="")):
            if "opendatacommunities" in row:
                uri = row["opendatacommunities"].lower()
                self.organisation_uri[row["organisation"].lower()] = uri
                self.organisation_uri[uri] = uri
                self.organisation_uri[self.end_of_uri(uri)] = uri
                self.organisation_uri[row["statistical-geography"].lower()] = uri
                if "local-authority-eng" in row["organisation"]:
                    dl_url = "https://digital-land.github.io/organisation/%s/" % (
                        row["organisation"]
                    )
                    dl_url = dl_url.lower().replace("-eng:", "-eng/")
                    self.organisation_uri[dl_url] = uri

        self.organisation_uri.pop("")

    def patch(self, field, fieldvalue, log_issue):
        if field == "OrganisationURI":
            value = self.lower_uri(fieldvalue)

            if value in self.organisation_uri:
                return self.organisation_uri[value]

            s = self.end_of_uri(value)
            if s in self.organisation_uri:
                return self.organisation_uri[s]

            log_issue(field, "opendatacommunities-uri", fieldvalue)
        return fieldvalue

    def set_resource_default_values(self, default_values):
        if "organisation" in default_values:
            default_values["OrganisationURI"] = self.organisation_uri[
                default_values["organisation"].lower()
            ]

        if "entry-date" in default_values:
            default_values["LastUpdatedDate"] = default_values["entry-date"]

    def lower_uri(self, value):
        return "".join(value.split()).lower()

    def end_of_uri(self, value):
        return self.end_of_uri_regex.sub("", value.rstrip("/").lower())


class PipelineCallback:
    harmonise = HarmoniseCallback()
