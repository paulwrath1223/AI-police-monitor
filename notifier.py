# Notify targets (maybe through telegram) and send audio file and transcript


def notify(targets, path, keyword="any"):
    with open((path + "transcript.txt"), "r") as f:
        transcript_list = f.readlines()
    f.close()
    transcript = ""
    for line in transcript_list:
        transcript += (line + "\n")

    if keyword == "any":
        message = "New message: \"" + transcript + "\""
    else:
        message = "Keyword \"" + keyword + "\" detected: \"" + transcript + "\""

    for target in targets:
        print("pretend I notify " + target + " with message \"" + message + "\".")


