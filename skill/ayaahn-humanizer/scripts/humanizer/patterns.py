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
    "paradigm": "model", "paradigms": "models", "spearhead": "lead", "spearheads": "leads",
    "spearheaded": "led", "spearheading": "leading", "streamline": "simplify",
    "streamlines": "simplifies", "streamlined": "simplified", "streamlining": "simplifying",
    "cornerstone": "foundation", "burgeoning": "growing", "quintessential": "typical",
    "underpin": "support", "underpins": "supports", "underpinned": "supported",
    "underpinning": "supporting", "daunting": "hard", "bustling": "busy",
    "ever-evolving": "changing", "impactful": "effective", "actionable": "practical",
    "learnings": "lessons", "indelible": "lasting",
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


# ---- second pass: tells catalogued by Wikipedia's "Signs of AI writing" and
# later skill catalogues (blader/humanizer 3.1, avoid-ai-writing). Removed or
# swapped like PHRASES, and counted by the detector as stock phrases.
TELL_PHRASES = [
    # chatbot residue and flattery
    (r"you(?:'|’)re absolutely right[!.,]?\s*", ""),
    (r"you are absolutely right[!.,]?\s*", ""),
    (r"(?:that(?:'|’)s )?(?:a |an )?(?:great|excellent|fantastic|good|really good|sharp) (?:point|catch|observation)[!.]\s*", ""),
    (r"of course[!]\s*", ""),
    (r"(?:would you like|do you want|want) me to[^.!?\n]*\?\s*", ""),
    (r"(?:is there )?anything else (?:i can|you(?:'|’)d like)[^.!?\n]*[.!?]\s*", ""),
    (r"here(?:'|’)s (?:a |an )?(?:detailed |quick |brief )?(?:overview|breakdown|summary)[^.!?\n]*:\s*", ""),
    # knowledge-limit disclaimers
    (r"(?:as of|up to) my (?:last )?(?:knowledge|training)(?: update| cutoff| date)?(?: in \w+ \d{4})?,?\s*", ""),
    (r"while (?:specific )?(?:details|information) (?:about [^,.]{2,60} )?(?:are|is) (?:limited|scarce|not (?:widely |publicly |extensively )?(?:available|documented|disclosed))[^,.]*,\s*", ""),
    (r"based on (?:the )?(?:available|provided) (?:information|sources|search results),?\s*", ""),
    # staged run-ups
    (r"here(?:'|’)s the thing[:,.]?\s*", ""),
    (r"the thing is,\s*", ""),
    (r"honestly\?\s+", ""),
    (r"to be clear,\s*", ""),
    (r"don(?:'|’)t get me wrong,?\s*", ""),
    (r"without further ado,?\s*", ""),
    (r"(?:here(?:'|’)s )?what you need to know[:.]?\s*", ""),
    (r"here(?:'|’)s the (?:kicker|catch|real story)[:,.]?\s*", ""),
    # one-line closers
    (r"read that again[.!]?\s*", ""),
    (r"let that sink in[.!]?\s*", ""),
    (r"that(?:'|’)?s the real (?:win|kicker|takeaway|story)[.!]?\s*", ""),
    (r"that is the real (?:win|kicker|takeaway|story)[.!]?\s*", ""),
    (r"the future (?:looks|is) bright[^.!?\n]*[.!?]\s*", ""),
    (r"exciting times (?:lie|are) ahead[^.!?\n]*[.!?]\s*", ""),
    (r"only time will tell[.!]?\s*", ""),
    # filler adverbs and transitions
    (r"notably,?\s+", ""),
    (r"importantly,?\s+", ""),
    (r"genuinely\s+", ""),
    (r"that being said,?\s+", "Still, "),
    (r"in addition,?\s+", "Also, "),
    # sales language
    (r"in the heart of ", "in "),
    (r"a (?:diverse|rich) (?:array|tapestry|mix) of ", "many "),
    (r"(?:functions|operates) as ", "is "),
]

# detection only: wording that can be a real claim, so it needs a human call
FLAG_ONLY = [
    ("significance-inflation",
     r"\bdespite (?:these|its|the|such)\b[^.]{0,60}\bchallenges\b|\bcontinues? to thrive\b|\bindelible mark\b|"
     r"\b(?:marking|marks) a (?:pivotal|key|significant) (?:moment|turning point)\b|\bkey turning point\b|\bdeeply rooted\b",
     "stock 'despite challenges... continues to thrive' and legacy language", 7),
    ("notability-padding",
     r"\b(?:maintains?|has) an? (?:strong |active )?(?:social media|digital) presence\b|\bindependent (?:media )?coverage\b|"
     r"\bprominent media outlets\b|\bfeatured in [^.]{0,80}\band other\b",
     "lists of outlets or social presence standing in for what was said", 6),
    ("cutoff-disclaimer",
     r"\bnot (?:widely|publicly|extensively) (?:documented|available|disclosed)\b|\bin the (?:provided|available) (?:sources|search results)\b|"
     r"\bmaintains? a low profile\b|\bkeeps? (?:his|her|their) personal (?:life|details) private\b",
     "says the source ran out, then guesses; state what is missing or cut it", 10),
    ("placeholder",
     r"\[(?:your |insert |describe |add |entertainer|company|name|date|subject)[^\]\n]{0,60}\]|\b\d{4}-XX-XX\b|<!--\s*add\b",
     "unfilled template text", 10),
    ("arguing-with-no-one",
     r"\b(?:this|that) isn(?:'|’)t (?:mainly |really |just )?about\b|\bi(?:'|’)m not saying\b|\bthis is not to say\b|"
     r"\byou might think\b|\bone might be tempted\b|\ba tempting approach\b|\bsome might say\b",
     "rejects an objection nobody raised", 5),
    ("narrated-candor",
     r"\bin the interest of full disclosure\b|\bi(?:'|’)d rather flag this\b|\bthe line i keep coming back to\b|\bi can(?:'|’)t stop thinking about\b",
     "announces honesty instead of being specific", 5),
    ("sycophancy",
     r"\b(?:what a|such a) (?:great|wonderful|fascinating|insightful) (?:question|point|idea)\b|\byou(?:'|’)re (?:so )?right to\b",
     "praise for the reader", 6),
]
