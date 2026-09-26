"""
codebook.py – WHAT the AI has to classify (content, not technology)
====================================================================
When you change a category or add a rule:
  1. change it here
  2. increase CODEBOOK_VERSION (e.g. "v3" -> "v4")
  -> The version is part of every result file name. This way you always know
     which codebook produced a result, and old results are never overwritten.

Every definition describes VISIBLE features of the text, not the reader's interpretation.
"""

CODEBOOK_VERSION = "v8"

# ---------------------------------------------------------------
# TOPICS: What is the MAIN STATEMENT (usually the headline) about?
# ---------------------------------------------------------------
TOPICS = {
    "military": (
        "The main statement is about armed force: attacks, strikes, missiles, drones, weapons, "
        "troop or naval movements, military exercises, casualties caused by attacks, military readiness "
        "for war, or threats and operational statements of armed forces "
        "(e.g. IRGC, army, Khatam al-Anbiya headquarters). "
        "Statements by Iran's armed forces about such matters are 'military' even if they mention other countries. "
        "NOT military: greetings, congratulations, ceremonies, visits or speeches by commanders about "
        "non-military matters – classify these by their content. "
        "Also military: war events in other countries that belong to the war involving Iran, the USA and Israel – "
        "attacks, explosions, sirens, shelters or damage in Israel, the Gulf states (Saudi Arabia, UAE, Qatar, "
        "Bahrain, Kuwait), Iraq or Jordan, and military cooperation of these states in the war. "
        "The Gulf states are directly or indirectly involved in this war, even if Iran is not named in the post. "
        "Posts about Lebanon/Hezbollah, Gaza, Yemen/Houthis, Iraqi militias or Syria stay resistance_axis."
    ),
    "diplomacy": (
        "The main statement is about Iran's relations with foreign states or international organizations: "
        "negotiations, mediation, ceasefire talks, agreements, foreign-policy positions of Iranian officials, "
        "or disputes with other states about sovereignty or territory."
    ),
    "domestic_politics": (
        "The main statement is about the Iranian state acting inside Iran: government decisions, "
        "government spokespersons on internal matters, parliament, courts, prosecutors, arrests, "
        "corruption cases, laws and regulations, police, internal security, protests, public services, "
        "repair of infrastructure, or authorities responding to disasters."
    ),
    "economy": (
        "The main statement is about money or markets: prices, inflation, exchange rates, oil and energy "
        "prices, trade volumes, trade agreements, subsidies, wages, rents, budgets, or companies. "
        "Test: if the core information is a price, an amount of money or a market development -> economy; "
        "if the core information is an action or decision of an authority -> domestic_politics."
    ),
    "ideology_propaganda": (
        "The main statement promotes the ideology of the Islamic Republic: praise of the Leader or the "
        "revolution, revolutionary or religious-political slogans, calls to attend regime rallies, "
        "justification of religious rulings, or statements about the values of the political system."
        " Also: anniversaries of historical battles, operations or revolutionary events, "
        "unless the focus is on specific deceased persons."
    ),
    "mourning_commemoration": (
        "The main statement is about a death or remembrance: funerals, burials, mourning ceremonies, "
        "mourning crowds, condolences, obituaries, tributes to a deceased person, death anniversaries, "
        "or commemoration of martyrs."
        " The focus must be on the dead or on mourning, not on a historical event as such."
    ),
    "resistance_axis": (
        "The main statement is about Lebanon/Hezbollah, Gaza/Palestinian groups, Iraqi militias, "
        "Yemen/Houthis or Syria, and Iran itself is not the acting party."
    ),
    "foreign_affairs": (
        "The main statement is about events inside or between other countries, Iran is not involved, "
        "and the topic is not the resistance axis. "
        "NOT foreign_affairs: war events connected to the war involving Iran -> military."
    ),
    "other": (
        "Anything else: science, nature, weather, accidents, fires, sports, culture, media notices, "
        "or posts with too little text to judge."
    ),
}

# ---------------------------------------------------------------
# TONES: Which VISIBLE features does the text have?
# The order matters: the AI takes the FIRST tone that clearly applies.
# ---------------------------------------------------------------
TONES = {
    "threatening": (
        "The text explicitly states a harmful consequence for an opponent or wrongdoer: retaliation, "
        "attack, punishment, 'they will pay', 'responsible for the consequences', often in the form "
        "'if ... then ...'. Quoted threats count. The consequence must be written in the text."
    ),
    "accusatory": (
        "The main statement blames or condemns an opponent with explicit negative claims: calls them "
        "criminals, murderers, puppets, liars or aggressors, or says they commit crimes, genocide, "
        "deception, or secretly control others. "
        "NOT accusatory: neutral reporting that only uses standard labels such as 'Zionist regime'. "
        "Arrests and trials: labelling political opponents, protesters, journalists, ethnic or religious "
        "minorities (e.g. Kurds, Baluch, Baha'is) or monarchists as terrorists, rioters, traitors, spies or "
        "mercenaries is accusatory when no final court verdict is reported – even if the label appears only in "
        "the body of the post. NOT accusatory: reports on arrests of members of groups listed as terrorist "
        "organisations by the UN or the EU (e.g. ISIS)."
    ),
    "mobilizing": (
        "The text contains a direct call or a collective commitment: an imperative or 'must/should' "
        "addressed to the own people or officials (come, participate, stand firm, support, be ready), "
        "or 'we' statements of determination ('we will not give up', 'we are ready for a long war'). "
        "NOT mobilizing: an official merely 'emphasizing the need' for a policy -> neutral."
    ),
    "triumphant": (
        "The text explicitly celebrates with evaluative words: victory, great success, humiliation or "
        "failure of the enemy, pride in strength. "
        "NOT triumphant: a factual report of an achievement (repair finished, fire contained) -> neutral."
    ),
    "mournful": (
        "The text contains explicit grief language: expressions of sorrow, pain, lament or condolence "
        "(e.g. 'with deep sorrow', 'heartbroken', 'condolences'). "
        "NOT mournful: a report about a funeral, a mourning ceremony or a mourning crowd "
        "without such words -> neutral."
    ),
    "neutral": (
        "None of the tones above clearly applies: factual reporting, information, announcements or analysis."
    ),
}

# ---------------------------------------------------------------
# SOURCES: Who is behind the channels? (neutral wording)
# Only given to the AI WITH context:
#   - as an overview of all sources in the prompt
#   - and before every post: "Source of this post: ..."
# Key = channel name exactly as in the data column 'kanal'.
# New source? Just add a line.
# ---------------------------------------------------------------
SOURCES = {
    "irna_1313": "IRNA (Islamic Republic News Agency) – Iran's official state news agency, "
                 "supervised by the government (Ministry of Culture and Islamic Guidance).",
    "iribnews": "IRIB News – news service of Islamic Republic of Iran Broadcasting, the state broadcaster "
                "whose head is appointed by the Supreme Leader.",
    "mehrnews": "Mehr News Agency – semi-official news agency owned by the Islamic Development Organization, "
                "which is supervised by the Supreme Leader.",
    "Tasnimnews": "Tasnim News Agency – semi-official news agency widely described as affiliated with the IRGC.",
    "farsna": "Fars News Agency – semi-official news agency widely described as affiliated with the IRGC.",
    "jamarannews": "Jamaran – news outlet linked to the institute publishing Ayatollah Khomeini's works; "
                   "generally associated with the reformist camp.",
    "sepahnews": "Sepah News – official news outlet of the IRGC.",
}

SOURCE_RULE = (
    "9. The source information tells you who is publishing the post. It helps to understand who is "
    "speaking and whose statements are quoted. It must NOT decide topic or tone: classify what the text says, "
    "exactly as you would for a post from any other source."
)

# ---------------------------------------------------------------
# RULES – rule 1 depends on whether the AI receives background knowledge
# v8: the AI again gives only ONE topic (as in v6). A secondary topic is set only by the human
#     coder in the test set (column topic2_manual) – for a fair evaluation of borderline cases.
# v7: secondary topic set by the AI was tested – used too often (39%), therefore rejected
# v6: military extended to war events abroad, accusatory extended to arrests/trials,
#     rule 8 extended (civilian victims) and worded more strictly
# v5: rule 3 (tone by main statement), rule 4 (quotations) and rule 8 (legal terms) changed/new;
#     the source rule is now no. 9
# ---------------------------------------------------------------
RULE_1_NO_CONTEXT = (
    "1. Judge only what is written in the post. Do not use outside knowledge about people or events."
)
RULE_1_WITH_CONTEXT = (
    "1. Judge what is written in the post. Use the BACKGROUND only to understand references "
    "(who a person is, whether someone has died, which event is meant). "
    "The background must not decide topic or tone on its own."
)
FURTHER_RULES = """2. Choose the topic by the main statement of the post (usually the headline), not by side details.
3. Check the tones in the listed order (threatening, accusatory, mobilizing, triumphant, mournful)
   and choose the FIRST one that clearly applies to the MAIN STATEMENT of the post.
   A single side sentence does not decide the tone. If none clearly applies, choose neutral.
4. Quotations count like the post's own text.
5. Standard labels used routinely by Iranian media ('martyr', 'Zionist regime', 'occupying regime',
   'arrogance') do not decide the tone on their own.
6. If you are unsure between a tone and neutral, choose neutral.
7. If the post has too little text to judge, use topic 'other' and tone 'neutral'.
8. Legal and descriptive terms for the wars in Gaza, Lebanon and Iran and their consequences
   ('genocide', 'war crimes', 'crimes against humanity', 'aggression', 'illegal war', 'occupation')
   are descriptive terms, like the standard labels in rule 5. This includes calling the killing of
   civilians or children, or attacks on hospitals, schools, homes or nuclear plants, a war crime.
   Apply this rule strictly: if these terms are the only negative wording in a post, the tone is neutral."""

