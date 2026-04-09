import re


class ConstraintDetector:
    """
    Classifies sentences as constraints (situation changes) or non-constraints
    (interiority, meaning-making, reflection).

    A constraint is a sentence where the subject changes what it's doing
    or something external changes the conditions.
    """

    def __init__(self):
        # Physical/transitional verbs — indicate situation change
        self.constraint_verbs = {
            "turned", "stopped", "set", "stood", "crossed", "lifted",
            "lowered", "opened", "closed", "entered", "left", "dropped",
            "picked", "pulled", "pushed", "cut", "broke", "struck",
            "placed", "carried", "threw", "caught", "dug", "poured",
            "split", "dragged", "loaded", "unloaded", "hitched",
            "saddled", "mounted", "dismounted", "knelt", "rose",
            "crouched", "leaned", "reached", "gripped", "released",
            "swung", "hammered", "nailed", "sawed", "chopped",
            "slipped", "stumbled", "fell", "climbed", "stepped",
            "walked", "ran", "moved", "shifted", "slid", "sat",
            "lit", "doused", "ate", "drank", "spat", "coughed",
            "dressed", "undressed", "washed", "wiped", "scraped",
            "folded", "unfolded", "packed", "unpacked", "locked",
            "unlocked", "bolted", "fastened", "unfastened",
            "began", "finished", "started", "ended", "halted",
            "paused", "resumed", "continued",
            "plowed", "ploughed", "sowed", "harvested", "reaped",
            "threshed", "harrowed", "seeded", "mowed", "scythed",
            "buried", "dug", "filled", "covered", "laid", "lowered",
            "signed", "handed", "sold", "paid", "received",
        }

        # Present tense / gerund forms of key constraint verbs
        self.constraint_verbs.update({
            "turns", "stops", "sets", "stands", "crosses", "lifts",
            "lowers", "opens", "closes", "enters", "leaves", "drops",
            "picks", "pulls", "pushes", "cuts", "breaks", "strikes",
            "places", "carries", "throws", "catches", "digs", "pours",
            "drags", "loads", "unloads", "kneels", "rises",
            "crouches", "leans", "reaches", "grips", "releases",
            "swings", "hammers", "nails", "saws", "chops",
            "slips", "stumbles", "falls", "climbs", "steps",
            "walks", "runs", "moves", "shifts", "slides", "sits",
            "lights", "eats", "drinks", "spits", "coughs",
            "washes", "wipes", "scrapes", "folds", "unfolds",
            "packs", "unpacks", "locks", "unlocks", "bolts",
            "fastens", "begins", "finishes", "starts", "ends",
            "halts", "pauses", "resumes", "continues",
            "plows", "sows", "harvests", "reaps", "mows",
            "buries", "fills", "covers", "lays",
            "signs", "hands", "sells", "pays", "receives",
            "dig", "sit", "run", "stand", "lean", "kneel",
            "crouch", "grip", "swing", "climb", "slip",
            "wash", "wipe", "scrape", "fold", "pack",
            "lock", "bolt", "fasten", "plow", "sow",
            "harvest", "reap", "mow", "bury", "fill",
            "cover", "lay", "sign", "sell", "pay",
        })

        # Environmental transition markers
        self.env_transitions = [
            "darkened", "brightened", "froze", "thawed",
            "snow began", "rain began", "wind rose", "wind died",
            "sun broke", "sun set", "light fell", "light faded",
            "door opened", "door closed", "fire caught", "fire died",
            "sound arrived", "sound stopped", "bell rang", "clock struck",
            "ice cracked", "branch snapped", "thunder rolled",
            "temperature dropped", "fog rolled", "clouds gathered",
        ]

        # Interiority / reflection verbs — model sliding into meaning-making
        self.reflection_verbs = {
            "remembered", "recalled", "thought", "wondered",
            "realized", "understood", "knew", "felt",
            "imagined", "wished", "hoped", "feared",
            "believed", "supposed", "considered", "reflected",
            "knows", "feels", "sees", "senses", "wants",
            "mourned", "grieved", "longed", "missed",
        }

        # Narrator interpretation pattern:
        # [subject] + [seemed/felt/appeared/held/carried] + [qualifier]
        self.narrator_verbs = {
            "seemed", "appeared", "felt", "held", "carried",
            "bore", "suggested", "implied", "betrayed",
            "radiated", "emanated", "exuded",
        }

        # Copula + temporal finality — state summary detection
        # "he was gone now", "she was alone forever"
        self.finality_markers = {
            "now", "forever", "never", "always", "at last",
            "once more", "no more", "for good", "finally",
            "already", "too late", "no longer",
        }

        # Meaning-making qualifiers after narrator verbs
        self.meaning_qualifiers = [
            "more than", "almost", "as if", "as though",
            "somehow", "something", "whatever", "anything",
            "nothing", "everything", "too great", "too heavy",
            "too much", "beyond", "beneath the surface",
        ]

    def _tokenize(self, sentence):
        return re.findall(r"\w+", sentence.lower())

    def _stem(self, token):
        """Rough stem: strip common suffixes to match past/present forms."""
        # Try longest suffixes first
        if token.endswith("ting") and len(token) > 5:
            stem = token[:-4]
            return stem + "t" if stem[-1:] != "t" else stem
        if token.endswith("ning") and len(token) > 5:
            stem = token[:-4]
            return stem + "n" if stem[-1:] != "n" else stem
        if token.endswith("ging") and len(token) > 5:
            stem = token[:-4]
            return stem + "g" if stem[-1:] != "g" else stem
        if token.endswith("pping") and len(token) > 5:
            return token[:-4]
        if token.endswith("ing") and len(token) > 4:
            stem = token[:-3]
            # "digging" -> "digg" -> "dig"
            if len(stem) > 2 and stem[-1] == stem[-2]:
                stem = stem[:-1]
            return stem
        if token.endswith("ed") and len(token) > 4:
            return token[:-2]
        if token.endswith("ches") or token.endswith("shes") or token.endswith("sses"):
            return token[:-2]
        if token.endswith("es") and len(token) > 4:
            return token[:-1]
        if token.endswith("s") and not token.endswith("ss") and len(token) > 3:
            return token[:-1]
        return token

    def _has_constraint_verb(self, tokens):
        stems = {self._stem(t) for t in tokens}
        verb_stems = {self._stem(v) for v in self.constraint_verbs}
        return bool(stems & verb_stems)

    def _has_env_transition(self, sentence):
        s = sentence.lower()
        return any(phrase in s for phrase in self.env_transitions)

    def _has_reflection_verb(self, tokens):
        return any(t in self.reflection_verbs for t in tokens)

    def _has_narrator_interpretation(self, sentence):
        """
        Detects structural meaning-making:
        - narrator verbs + meaning qualifiers
        - copula + finality markers
        """
        s = sentence.lower()
        tokens = self._tokenize(sentence)

        # Pattern 1: narrator verb + qualifier
        has_narrator_verb = any(t in self.narrator_verbs for t in tokens)
        has_qualifier = any(q in s for q in self.meaning_qualifiers)
        if has_narrator_verb and has_qualifier:
            return True

        # Pattern 2: copula (was/were/is) + finality
        copulas = {"was", "were", "is", "had been", "would be"}
        has_copula = any(c in s for c in copulas)
        has_finality = any(t in self.finality_markers for t in tokens)
        if has_copula and has_finality:
            return True

        # Pattern 3: em-dash followed by abstract/figurative clause
        # "walked to the barn—a silent reminder of generations past"
        if "—" in s or "--" in s:
            after_dash = re.split(r"[—]|--", s)[-1].strip()
            dash_signals = ["reminder", "testament", "symbol", "echo",
                           "promise", "sign", "shadow", "ghost",
                           "canvas", "mirror", "weight", "silence"]
            if any(d in after_dash for d in dash_signals):
                return True

        # Pattern 4: participial narration — "knowing that", "offering comfort",
        # "wanting to", "hoping to", "wishing"
        if re.search(r"\b(knowing|realizing|offering|wanting|hoping|wishing|fearing|sensing|feeling)\b", s):
            return True

        # Pattern 5: hypothetical action — "as though to [verb]", "as if to [verb]"
        if re.search(r"\b(as though to|as if to)\s+\w+", s):
            return True

        # Pattern 6: "a look of [X]", "with a sense of [X]", "spoke volumes"
        if re.search(r"\b(a look of|a sense of|spoke volumes|the weight of|a reminder of|the scent of memory)\b", s):
            return True

        return False

    def _has_emotional_labeling(self, sentence):
        """
        Catches emotional state naming that bypasses the lexical scorer.
        Looks for 'felt [adjective]' and 'heart [verb]' patterns.
        """
        s = sentence.lower()
        # "felt altered", "felt heavy", "felt nothing", "felt empty"
        if re.search(r"\bfelt\s+\w+", s):
            return True
        # "heart clenched", "heart sank", "heart pounded"
        if re.search(r"\bheart\s+(clenched|sank|pounded|ached|broke|tightened|raced|stopped)", s):
            return True
        return False


    def _scan_dialogue(self, sentence):
        """Dialogue-specific gate. Returns non-constraint if dialogue is explanatory."""
        s = sentence.lower()

        # Collective framing — "we're still", "we have to", "us"
        collective = bool(re.search(r"\b(we're|we are|we still|we have|we need|we can|us)\b", s))

        # Speculative reassurance — "I guess", "probably", "maybe we"
        speculative = bool(re.search(r"\b(i guess|probably|maybe we|i suppose|perhaps)\b", s))

        # Expressive speech — character articulating interiority
        expressive = bool(re.search(
            r"\b(i\s+(felt|feel|knew|know|hoped|wished|promised|couldn't|can't|need to|have to)|please|don't make me|don't let me|i can't bear|forgive me)\b", s))

        if collective or speculative or expressive:
            return {
                "is_constraint": False,
                "verb_class": "explanatory_dialogue",
                "confidence": 0.8,
                "flags": [f for f, v in [
                    ("collective_framing", collective),
                    ("speculative_reassurance", speculative),
                    ("expressive_speech", expressive),
                ] if v],
            }

        # Dialogue that transmits information or creates friction — allow
        return None  # fall through to standard scan

    def scan(self, sentence):
        """
        Returns classification for a single sentence.

        {
            "is_constraint": bool,
            "verb_class": "physical" | "environmental" | "reflection" | "narration" | "neutral",
            "confidence": float (0-1),
            "flags": list of triggered detectors
        }
        """
        # Dialogue gate — check before standard scan
        if any(q in sentence for q in ['"', chr(8220), chr(8221), chr(8216), chr(8217)]):
            dialogue_result = self._scan_dialogue(sentence)
            if dialogue_result is not None:
                return dialogue_result

        tokens = self._tokenize(sentence)
        flags = []

        has_physical = self._has_constraint_verb(tokens)
        has_env = self._has_env_transition(sentence)
        has_reflection = self._has_reflection_verb(tokens)
        has_narration = self._has_narrator_interpretation(sentence)
        has_emotional = self._has_emotional_labeling(sentence)

        if has_physical:
            flags.append("physical_verb")
        if has_env:
            flags.append("env_transition")
        if has_reflection:
            flags.append("reflection_verb")
        if has_narration:
            flags.append("narrator_interpretation")
        if has_emotional:
            flags.append("emotional_labeling")

        # Decision logic:
        # A sentence with a physical verb or env transition IS a constraint,
        # UNLESS it also has narrator interpretation (meaning the physical
        # action is being used as a vehicle for meaning-making).
        # e.g. "He stepped forward as if carrying the weight of the world"

        if has_narration or has_emotional:
            # Narrator interpretation overrides physical verb
            # unless the physical action is the main clause
            if has_physical and not has_reflection:
                # Physical verb tainted by narration = not a real constraint
                # Physical verb present but tainted by narration
                # Lower confidence constraint
                return {
                    "is_constraint": False,
                    "verb_class": "narration",
                    "confidence": 0.6,
                    "flags": flags,
                }
            return {
                "is_constraint": False,
                "verb_class": "narration" if has_narration else "reflection",
                "confidence": 0.8,
                "flags": flags,
            }

        if has_reflection:
            # Reflection verb present — even with a physical verb,
            # the sentence is serving interiority not situation change
            return {
                "is_constraint": False,
                "verb_class": "reflection",
                "confidence": 0.7,
                "flags": flags,
            }

        if has_physical or has_env:
            return {
                "is_constraint": True,
                "verb_class": "physical" if has_physical else "environmental",
                "confidence": 0.8,
                "flags": flags,
            }

        # Neutral — no strong signal either way
        return {
            "is_constraint": False,
            "verb_class": "neutral",
            "confidence": 0.3,
            "flags": flags,
        }
