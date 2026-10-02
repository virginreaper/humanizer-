"""Pattern tables. Based on blader/humanizer's 26 patterns and Wikipedia's
"Signs of AI writing". Everything here is data so it is easy to extend."""

# (regex, replacement). Case is preserved. Longer phrases first.
PHRASES = [
    # chatbot residue / run-ups (removed outright)
    (r"(?:great|good|excellent|fantastic) question[!.]?\s*", ""),
    (r"i hope this helps[!.]?\s*", ""),
    (r"let me know if you(?:'d| would)? (?:like|want|need)[^.!?]*[.!?]\s*", ""),
    (r"certainly[!,]\s*", ""),
    (r"let(?:'|’)s dive (?:in|into)[^.!?]*[.!?]\s*", ""),
    (r"let(?:'|’)s (?:take a closer look|explore)[^.!?]*[.!?]\s*", ""),
    (r"as an ai(?: language model)?,?[^.!?]*[.!?]\s*", ""),
    # filler openers
    (r"it(?:'|’)?s (?:important|worth|crucial|essential) (?:to note|noting|to remember|to mention) that,? ", ""),
    (r"it is (?:important|worth|crucial|essential) (?:to note|noting|to remember|to mention) that,? ", ""),
    (r"it should be noted that,? ", ""),
    (r"needless to say,? ", ""),
    (r"in today(?:'|’)s (?:fast-paced |digital |modern |ever-changing )*(?:world|age|era|landscape),? ", ""),
    (r"in the (?:ever-evolving|ever-changing|rapidly evolving) (?:world|landscape|field) of ", "in "),
    (r"when it comes to ", "for "),
    (r"at the end of the day,? ", ""),
    (r"at its core,? ", ""),
    (r"in essence,? ", ""),
    (r"(?:in conclusion|in summary|to sum up|to summarize|to conclude|overall),? ", ""),
    # connectors
    (r"furthermore,? ", "Also, "),
    (r"moreover,? ", "And "),
    (r"additionally,? ", "Also, "),
    (r"consequently,? ", "So "),
    (r"subsequently,? ", "Then "),
    (r"nevertheless,? ", "Still, "),
    (r"nonetheless,? ", "Still, "),
    # wordy constructions
    (r"due to the fact that ", "because "),
    (r"in light of the fact that ", "since "),
    (r"despite the fact that ", "although "),
    (r"in order to ", "to "),
    (r"with regard(?:s)? to ", "about "),
    (r"in the event that ", "if "),
    (r"for the purpose of ", "for "),
    (r"a (?:wide|broad|vast) (?:range|array|variety) of ", "many "),
    (r"a (?:myriad|plethora) of ", "lots of "),
    (r"plays an? (?:crucial|pivotal|vital|key|significant) role in ", "matters for "),
    (r"play an? (?:crucial|pivotal|vital|key|significant) role in ", "matter for "),
    (r"stands as a testament to ", "shows "),
    (r"stand as a testament to ", "show "),
    (r"(?:is|was) a testament to ", "shows "),
    (r"(?:are|were) a testament to ", "show "),
    (r"a testament to ", "proof of "),
    (r"(?:serves|stands|acts) as ", "is "),
    (r"(?:serve|stand|act) as ", "are "),
    (r"boasts ", "has "),
    (r"boast ", "have "),
    (r"delves? into ", "looks at "),
    (r"dives? deep into ", "digs into "),
    (r"embarks? on ", "starts "),
    (r"shed(?:s|ding)? light on ", "explain "),
    (r"paves? the way for ", "makes room for "),
    (r"sets? the stage for ", "leads to "),
    (r"a rich tapestry of ", "a mix of "),
    (r"nestled (?:within|in|among) ", "in "),
    (r"(?:breathtaking|stunning|picturesque) ", ""),
    (r"in a (?:seamless|holistic) (?:way|manner)", "smoothly"),
]

# single words (word-boundary, case preserved)
WORDS = {
    "delve": "dig", "tapestry": "mix", "pivotal": "key", "crucial": "important",
    "vital": "important", "testament": "proof", "vibrant": "lively",
    "intricate": "detailed", "intricacies": "details", "meticulous": "careful",
    "meticulously": "carefully", "garner": "get", "garnered": "got",
    "bolster": "support", "bolstered": "supported", "bolsters": "supports",
    "interplay": "interaction", "foster": "encourage", "fosters": "encourages",
    "fostering": "encouraging", "fostered": "encouraged", "enhance": "improve",
    "enhances": "improves", "enhanced": "better", "enhancing": "improving",
    "showcase": "show", "showcases": "shows", "showcasing": "showing",
    "realm": "area", "multifaceted": "complex", "robust": "solid",
    "seamless": "smooth", "seamlessly": "smoothly", "holistic": "whole",
    "comprehensive": "thorough", "leverage": "use", "leverages": "uses",
    "leveraging": "using", "leveraged": "used", "harness": "use",
    "harnesses": "uses", "harnessing": "using", "empower": "let",
    "empowers": "lets", "empowering": "letting", "elevate": "raise",
    "elevates": "raises", "embark": "start", "navigate": "handle",
    "navigating": "handling", "enduring": "lasting", "transformative": "big",
    "groundbreaking": "new", "ecosystem": "system", "nuanced": "subtle",
    "underscore": "show", "underscores": "shows", "underscored": "showed",
    "utilize": "use", "utilizes": "uses", "utilizing": "using", "utilise": "use",
    "facilitate": "help", "facilitates": "helps", "numerous": "many",
    "commence": "begin", "endeavor": "try", "endeavour": "try",
    "paramount": "key", "myriad": "many", "plethora": "lot",
    "cutting-edge": "new", "game-changer": "big change", "game-changing": "major",
    "unparalleled": "unmatched", "unlock": "open up", "unleash": "release",
}

# "the political landscape" style metaphor only (not literal landscape)
LANDSCAPE = r"\b(\w+(?:-\w+)?) landscape\b"
LANDSCAPE_CTX = {"political", "digital", "competitive", "evolving", "changing",
                 "modern", "current", "media", "legal", "economic", "cultural",
                 "technological", "regulatory", "governance", "policy", "data", "business", "market", "social"}

# detection only (need a real source, can't be fixed mechanically)
VAGUE_ATTRIBUTION = (r"\b(?:studies (?:show|suggest|indicate)|research (?:shows|suggests|indicates)|"
                     r"experts (?:say|believe|agree|suggest)|critics (?:argue|say)|"
                     r"many (?:believe|argue|say)|it is widely (?:believed|known|accepted)|"
                     r"some (?:argue|say|believe))\b")

# present-participle tails that add fake weight
TAIL_VERBS = ("highlighting", "underscoring", "showcasing", "reflecting", "symbolizing",
              "marking", "illustrating", "emphasizing", "emphasising", "demonstrating",
              "cementing", "solidifying", "reinforcing", "contributing to", "serving as",
              "paving the way", "setting the stage", "shaping", "signaling", "signalling",
              "ensuring", "fostering", "cultivating")

CONTRACTIONS = [
    (r"\bdo not\b", "don't"), (r"\bdoes not\b", "doesn't"), (r"\bdid not\b", "didn't"),
    (r"\bis not\b", "isn't"), (r"\bare not\b", "aren't"), (r"\bwas not\b", "wasn't"),
    (r"\bwere not\b", "weren't"), (r"\bhave not\b", "haven't"), (r"\bhas not\b", "hasn't"),
    (r"\bcannot\b", "can't"), (r"\bcan not\b", "can't"), (r"\bwill not\b", "won't"),
    (r"\bwould not\b", "wouldn't"), (r"\bshould not\b", "shouldn't"),
    (r"\bcould not\b", "couldn't"), (r"\bit is\b", "it's"), (r"\bthat is\b", "that's"),
    (r"\bthere is\b", "there's"), (r"\bI am\b", "I'm"), (r"\bthey are\b", "they're"),
    (r"\bwe are\b", "we're"), (r"\byou are\b", "you're"), (r"\bI have\b", "I've"),
    (r"\bwe have\b", "we've"), (r"\bthey have\b", "they've"), (r"\bI will\b", "I'll"),
    (r"\bwe will\b", "we'll"), (r"\bit will\b", "it'll"), (r"\blet us\b", "let's"),
]
