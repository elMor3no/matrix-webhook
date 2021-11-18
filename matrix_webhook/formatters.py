"""Formatters for matrix webhook."""


def grafana(data, headers):
    """Pretty-print a grafana notification."""
    text = ""
    if "title" in data:
        text = "#### " + data["title"] + "\n"
    if "message" in data:
        text = text + data["message"] + "\n\n"
    if "evalMatches" in data:
        for match in data["evalMatches"]:
            text = text + "* " + match["metric"] + ": " + str(match["value"]) + "\n"
    data["body"] = text
    return data

def gitlab(data, headers):
    """Pretty-print a gitlab notification."""
    text = ""
    text = "# A new action has been registered in the repository " + data["repository"]["name"] + "\n\n" 
    if "user_name" in data:
        text = text + "**User:** " + data["user_name"] + "\n\n"
    if "object_kind" in data:
        text = text + "Make a " + data["object_kind"] + "\n\n"
    if "commits" in data:
        count_commits = len(data['commits'])
        if count_commits > 1:
            text = text + data["user_name"] + " pushed " + str(count_commits) + " commits \n\n"
        else:
            text = text + data["user_name"] + " pushed " + str(count_commits) + " commit \n\n"
        for match in data["commits"]:
            text = text + "* [" + match["message"] + " ](" + match["url"] + ")\n\n"
            [TUD](https://tu-dresden.de/++theme++tud.theme.webcms2/img/tud-logo-white.svg)
    if "checkout_sha" in data:
        text = text + "**With hash:** " + data["checkout_sha"] + "\n\n"
    if "repository" in data:
        text = text + "**Repository:** " + data["repository"]["name"] + "\n\n"        
    data["body"] = text
    return data

def github(data, headers):
    """Pretty-print a github notification."""
    # TODO: Write nice useful formatters. This is only an example.
    if headers["X-GitHub-Event"] == "push":
        pusher, ref, a, b, c = [
            data[k] for k in ["pusher", "ref", "after", "before", "compare"]
        ]
        pusher = f"[@{pusher['name']}](https://github.com/{pusher['name']})"
        data["body"] = f"{pusher} pushed on {ref}: [{b} → {a}]({c}):\n\n"
        for commit in data["commits"]:
            data["body"] += f"- [{commit['message']}]({commit['url']})\n"
    else:
        data["body"] = "notification from github"
    data["digest"] = headers["X-Hub-Signature-256"].replace("sha256=", "")
    return data
