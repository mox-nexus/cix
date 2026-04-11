# Stream A — Extraction Triage

**Input corpus:** 609 unique papers across 26 JSONL files (sweep 1 + sweep 2)  
**Triage method:** OpenAlex relevance-ordered top 5 per query, deduped, citation-ceiling 50k to exclude topic-outlier ML/physics/stats software
**Output:** 127 unique triaged papers, grouped by research question

## Papers appearing in multiple queries (cross-cutting relevance)

- **Six views of embodied cognition** — Margaret Wilson (2002, 4438 cites)
  Found in: openalex-rq2-conversation, openalex-p2-distributed-cognition
- **Précis of Elements of episodic memory** — Endel Tulving (1984, 804 cites)
  Found in: openalex-rq3-encoding-specificity, openalex-rq0-episodic-semantic-systems
- **Handbook of Metamemory and Memory** — John Dunlosky, Robert A. Bjork (2013, 296 cites)
  Found in: openalex-rq4-feeling-knowing, openalex-rq4-judgment-learning

## P2-bridges

### Implementation intentions: Strong effects of simple plans.
- **Authors:** Peter M. Gollwitzer
- **Year:** 1999 | **Citations:** 5209
- **Venue:** American Psychologist
- **PDF:** https://kops.uni-konstanz.de/server/api/core/bitstreams/14cc2a36-5f01-4dc1-b9ca-f2d0ca0c8930/content
- **OpenAlex ID:** https://openalex.org/W2133044046
- **Query:** openalex-p2-memory-imagination
- **Abstract:** When people encounter problems in translating their goals into action (e.g., failing to get started, becoming distracted, or falling into bad habits), they may strategically call on automatic processes in an attempt to secure goal attain-ment. This can be achieved by plans in the form of imple-menta...

### Identity and interaction: a sociocultural linguistic approach
- **Authors:** Mary Bucholtz, Kira Hall
- **Year:** 2005 | **Citations:** 3610
- **Venue:** Discourse Studies
- **PDF:** https://escholarship.org/content/qt5tk670n8/qt5tk670n8.pdf
- **OpenAlex ID:** https://openalex.org/W2109151141
- **Query:** openalex-p2-distributed-cognition
- **Abstract:** The article proposes a framework for the analysis of identity as produced in linguistic interaction, based on the following principles: (1) identity is the product rather than the source of linguistic and other semiotic practices and therefore is a social and cultural rather than primarily internal ...

### Supersizing the mind: embodiment, action, and cognitive extension
- **Authors:** 
- **Year:** 2009 | **Citations:** 2237
- **Venue:** Choice Reviews Online
- **OpenAlex ID:** https://openalex.org/W1552415422
- **Query:** openalex-p2-extended-mind
- **Abstract:** Forward: By David Chalmers / Acknowledgements / Introduction: BRAINBOUND versus EXTENDED / I: From Embodiment to Cognitive Extension - 1. The Active Body: 1.1 A Walk on the Wild Side 1.2 Inhabited Interaction 1.3 Active Sensing 1.4 Distributed Functional Decomposition 1.5 Sensing for Coupling 1.6 In...

### THE ROBUSTNESS OF CRITICAL PERIOD EFFECTS IN SECOND LANGUAGEACQUISITION
- **Authors:** Robert DeKeyser
- **Year:** 2000 | **Citations:** 1419
- **Venue:** Studies in Second Language Acquisition
- **PDF:** https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6963A1AFEB8148B7F3B719D60994CD65/S0272263100004022a.pdf/div-class-title-the-robustness-of-critical-period-effects-in-second-language-acquisition-div.pdf
- **OpenAlex ID:** https://openalex.org/W2127041292
- **Query:** openalex-p2-deacon-symbolic
- **Abstract:** This study was designed to test the Fundamental Difference Hypothesis (Bley-Vroman, 1988), which states that, whereas children are known to learn language almost completely through (implicit) domain-specific mechanisms, adults have largely lost the ability to learn a language without reflecting on i...

### AUGMENTING HUMAN INTELLECT: A CONCEPTUAL FRAMEWORK
- **Authors:** Douglas C. Engelbart
- **Year:** 1962 | **Citations:** 1026
- **Venue:** —
- **OpenAlex ID:** https://openalex.org/W2152304295
- **Query:** openalex-p2-engelbart-augmenting
- **Abstract:** Final report of in-depth study conducted by Doug Engelbart 1959-1962 into improving human intellect and human effectiveness, outlining a conceptual framework re: what makes us intellectually capable and effective, and best approach for systematically augmenting this capability, concluding with a pro...

### Phenomenology of Practice
- **Authors:** Max van Manen
- **Year:** 2007 | **Citations:** 798
- **Venue:** Phenomenology & Practice
- **PDF:** https://doi.org/10.29173/pandpr19803
- **OpenAlex ID:** https://openalex.org/W1480064541
- **Query:** openalex-p2-husserl-time-memory
- **Abstract:** Phenomenology of practice is formative of sensitive practice, issuing from the pathic power of phenomenological reflections. Pathic knowing inheres in the sense and sensuality of our practical actions, in encounters with others and in the ways that our bodies are responsive to the things of our worl...

### Disgust as an adaptive system for disease avoidance behaviour
- **Authors:** Valérie Curtis, Mícheál de Barra, Robert Aunger
- **Year:** 2011 | **Citations:** 738
- **Venue:** Philosophical Transactions of the Royal Society B Biological Sciences
- **PDF:** https://royalsocietypublishing.org/doi/pdf/10.1098/rstb.2010.0117
- **OpenAlex ID:** https://openalex.org/W2138011226
- **Query:** openalex-p2-deacon-symbolic
- **Abstract:** Disgust is an evolved psychological system for protecting organisms from infection through disease avoidant behaviour. This 'behavioural immune system', present in a diverse array of species, exhibits universal features that orchestrate hygienic behaviour in response to cues of risk of contact with ...

### Neurophenomenology Integrating Subjective Experience and Brain Dynamics in the Neuroscienc
- **Authors:** Antoine Lutz, Evan Thompson
- **Year:** 2003 | **Citations:** 417
- **Venue:** Journal of Consciousness Studies
- **OpenAlex ID:** https://openalex.org/W2146431307
- **Query:** openalex-p2-neurophenomenology
- **Abstract:** The paper presents a research programme for the neuroscience of con- sciousness called 'neurophenomenology' (Varela 1996) and illustrates it with a recent pilot study (Lutz et al., 2002). At a theoretical level, neurophenomenology pursues a n e mbodied a nd l arge-scale d ynamical a pproach t o t he...

### The Extended Mind
- **Authors:** 
- **Year:** 2010 | **Citations:** 401
- **Venue:** The MIT Press eBooks
- **OpenAlex ID:** https://openalex.org/W4210318093
- **Query:** openalex-p2-extended-mind
- **Abstract:** Leading scholars respond to the famous proposition by Andy Clark and David Chalmers that cognition and mind are not located exclusively in the head. Where does the mind stop and the rest of the world begin? In their famous 1998 paper "The Extended Mind," philosophers Andy Clark and David J. Chalmers...

### Generalization through the recurrent interaction of episodic memories: A model of the hipp
- **Authors:** Dharshan Kumaran, James L. McClelland
- **Year:** 2012 | **Citations:** 401
- **Venue:** Psychological Review
- **PDF:** https://doi.org/10.1037/a0028681
- **OpenAlex ID:** https://openalex.org/W2130156168
- **Query:** openalex-p2-hippocampus-relational
- **Abstract:** In this article, we present a perspective on the role of the hippocampal system in generalization, instantiated in a computational model called REMERGE (recurrency and episodic memory results in generalization). We expose a fundamental, but neglected, tension between prevailing computational theorie...

### Perceptual Anomalies in Schizophrenia: Integrating Phenomenology and Cognitive Neuroscienc
- **Authors:** Peter J. Uhlhaas, Aaron L. Mishara
- **Year:** 2006 | **Citations:** 316
- **Venue:** Schizophrenia Bulletin
- **PDF:** https://academic.oup.com/schizophreniabulletin/article-pdf/33/1/142/5429356/sbl047.pdf
- **OpenAlex ID:** https://openalex.org/W2119969856
- **Query:** openalex-p2-husserl-time-memory
- **Abstract:** From phenomenological and experimental perspectives, research in schizophrenia has emphasized deficits in "higher" cognitive functions, including attention, executive function, as well as memory. In contrast, general consensus has viewed dysfunctions in basic perceptual processes to be relatively un...

### Recognizing group cognition
- **Authors:** Georg Theiner, Colin Allen, Robert L. Goldstone
- **Year:** 2010 | **Citations:** 226
- **Venue:** Cognitive Systems Research
- **OpenAlex ID:** https://openalex.org/W2033617583
- **Query:** openalex-p2-extended-mind

### Phenomenology for the Twenty-First Century
- **Authors:** J. Aaron Simmons
- **Year:** 2016 | **Citations:** 222
- **Venue:** Palgrave Macmillan UK eBooks
- **PDF:** https://uscholar.univie.ac.at/detail/o:647190.pdf
- **OpenAlex ID:** https://openalex.org/W2510287499
- **Query:** openalex-p2-husserl-time-memory
- **Abstract:** This volume illustrates the relevance of phenomenology to a range of contemporary concerns. Displaying both the epistemological rigor of classical phenomenology and the empirical analysis of more rece

### Constructive episodic simulation: Dissociable effects of a specificity induction on rememb
- **Authors:** Kevin P. Madore, Brendan Gaesser, Daniel L. Schacter
- **Year:** 2013 | **Citations:** 207
- **Venue:** Journal of Experimental Psychology Learning Memory and Cognition
- **PDF:** https://www.ncbi.nlm.nih.gov/pmc/articles/4006318
- **OpenAlex ID:** https://openalex.org/W2165012907
- **Query:** openalex-p2-memory-imagination
- **Abstract:** According to the constructive episodic simulation hypothesis (Schacter & Addis, 2007), both remembered past and imagined future events rely heavily on episodic memory. An alternative hypothesis is that observed similarities between remembering and imagining reflect the influence of broader factors s...

### Remembering the past and imagining the future: Identifying and enhancing the contribution 
- **Authors:** Daniel L. Schacter, Kevin P. Madore
- **Year:** 2016 | **Citations:** 198
- **Venue:** Memory Studies
- **PDF:** https://www.ncbi.nlm.nih.gov/pmc/articles/5289412
- **OpenAlex ID:** https://openalex.org/W2467239256
- **Query:** openalex-p2-memory-imagination
- **Abstract:** Recent studies have shown that imagining or simulating future events relies on many of the same cognitive and neural processes as remembering past events. According to the constructive episodic simulation hypothesis (Schacter and Addis, 2007), such overlap indicates that both remembered past and ima...

## RQ0-baseline

### The Neuropsychology of Memory
- **Authors:** Larry R. Squire
- **Year:** 1984 | **Citations:** 2129
- **Venue:** —
- **OpenAlex ID:** https://openalex.org/W1540086863
- **Query:** openalex-rq0-consolidation

### Long-Term Potentiation and Memory
- **Authors:** Marina A. Lynch
- **Year:** 2004 | **Citations:** 1957
- **Venue:** Physiological Reviews
- **OpenAlex ID:** https://openalex.org/W2141998004
- **Query:** openalex-rq0-consolidation
- **Abstract:** One of the most significant challenges in neuroscience is to identify the cellular and molecular processes that underlie learning and memory formation. The past decade has seen remarkable progress in understanding changes that accompany certain forms of acquisition and recall, particularly those for...

### Mechanisms of emotional arousal and lasting declarative memory
- **Authors:** L Cahill, James L. McGaugh
- **Year:** 1998 | **Citations:** 1573
- **Venue:** Trends in Neurosciences
- **OpenAlex ID:** https://openalex.org/W2139502395
- **Query:** openalex-rq0-consolidation

### A single standard for memory: the case for reconsolidation
- **Authors:** Karim Nader, Oliver Hardt
- **Year:** 2009 | **Citations:** 781
- **Venue:** Nature reviews. Neuroscience
- **OpenAlex ID:** https://openalex.org/W2161113761
- **Query:** openalex-rq0-consolidation

### Region-specific changes in prefrontal function with age: a review of PET and fMRI studies 
- **Authors:** M. Natasha Rajah, Mark D’Esposito
- **Year:** 2005 | **Citations:** 520
- **Venue:** Brain
- **OpenAlex ID:** https://openalex.org/W2095882961
- **Query:** openalex-rq0-episodic-review
- **Abstract:** Several neuroimaging studies of cognitive ageing have found that age-related deficits in working memory (WM) and episodic memory abilities are related to changes in prefrontal cortex (PFC) function. Reviews of these neuroimaging studies have generally concluded that with age there is a reduction in ...

### The effects of acute stress on episodic memory: A meta-analysis and integrative review.
- **Authors:** Grant S. Shields, Matthew A. Sazma, Andrew M. McCullough
- **Year:** 2017 | **Citations:** 427
- **Venue:** Psychological Bulletin
- **PDF:** https://doi.org/10.1037/bul0000100
- **OpenAlex ID:** https://openalex.org/W2604384875
- **Query:** openalex-rq0-episodic-review
- **Abstract:** A growing body of research has indicated that acute stress can critically impact memory. However, there are a number of inconsistencies in the literature, and important questions remain regarding the conditions under which stress effects emerge as well as basic questions about how stress impacts dif...

### From Knowing to Remembering: The Semantic–Episodic Distinction
- **Authors:** Louis Renoult, Muireann Irish, Morris Moscovitch
- **Year:** 2019 | **Citations:** 344
- **Venue:** Trends in Cognitive Sciences
- **PDF:** https://ueaeprints.uea.ac.uk/id/eprint/72823/1/Accepted_manuscript.pdf
- **OpenAlex ID:** https://openalex.org/W2981452806
- **Query:** openalex-rq0-episodic-semantic-systems

### The relationships between memory systems and sleep stages
- **Authors:** Géraldine Rauchs, Béatrice Desgranges, J. Foret
- **Year:** 2005 | **Citations:** 267
- **Venue:** Journal of Sleep Research
- **OpenAlex ID:** https://openalex.org/W2125031140
- **Query:** openalex-rq0-episodic-semantic-systems
- **Abstract:** Sleep function remains elusive despite our rapidly increasing comprehension of the processes generating and maintaining the different sleep stages. Several lines of evidence support the hypothesis that sleep is involved in the off-line reprocessing of recently-acquired memories. In this review, we s...

### How many memory systems? Evidence from aging.
- **Authors:** David B. Mitchell
- **Year:** 1989 | **Citations:** 237
- **Venue:** Journal of Experimental Psychology Learning Memory and Cognition
- **OpenAlex ID:** https://openalex.org/W2008631622
- **Query:** openalex-rq0-episodic-semantic-systems
- **Abstract:** older (ages 63-80) adults were given procedural, semantic, and episodic memory tasks. Repetition, lag, and codability were manipulated in a picture-naming task, followed by incidental memory tests. Relative to young adults, older adults exhibited lower levels of recall and recognition, but these epi...

### Episodic memory in frontotemporal dementia: a critical review
- **Authors:** Michael Hornberger, Olivier Piguet
- **Year:** 2012 | **Citations:** 204
- **Venue:** Brain
- **PDF:** https://academic.oup.com/brain/article-pdf/135/3/678/5509826/aws011.pdf
- **OpenAlex ID:** https://openalex.org/W2135433550
- **Query:** openalex-rq0-episodic-review
- **Abstract:** This review offers a critical appraisal of the literature on episodic memory performance in frontotemporal dementia. Historically, description of patients diagnosed with what was then known as Pick's disease included the presence of memory deficits and an underlying amnestic syndrome was noted in so...

### Semantic Memory and the Hippocampus: Revisiting, Reaffirming, and Extending the Reach of T
- **Authors:** Melissa C. Duff, Natalie V. Covington, Caitlin Hilverman
- **Year:** 2020 | **Citations:** 189
- **Venue:** Frontiers in Human Neuroscience
- **PDF:** https://www.frontiersin.org/articles/10.3389/fnhum.2019.00471/pdf
- **OpenAlex ID:** https://openalex.org/W3007266467
- **Query:** openalex-rq0-episodic-semantic-systems
- **Abstract:** Since Tulving proposed a distinction in memory between semantic and episodic memory, considerable effort has been directed towards understanding their similar and unique features. Of particular interest has been the extent to which semantic and episodic memory have a shared dependence on the hippoca...

### Virtual reality in episodic memory research: A review
- **Authors:** Stephanie A. Smith
- **Year:** 2019 | **Citations:** 176
- **Venue:** Psychonomic Bulletin & Review
- **PDF:** https://link.springer.com/content/pdf/10.3758/s13423-019-01605-w.pdf
- **OpenAlex ID:** https://openalex.org/W2943575974
- **Query:** openalex-rq0-episodic-review

### The Temporal Effects of Acute Exercise on Episodic Memory Function: Systematic Review with
- **Authors:** Paul D. Loprinzi, Jeremiah Blough, Lindsay Crawford
- **Year:** 2019 | **Citations:** 164
- **Venue:** Brain Sciences
- **PDF:** https://www.mdpi.com/2076-3425/9/4/87/pdf?version=1556185886
- **OpenAlex ID:** https://openalex.org/W2939559417
- **Query:** openalex-rq0-episodic-review
- **Abstract:** Accumulating research demonstrates that the timing of exercise plays an important role in influencing episodic memory. However, we have a limited understanding as to the factors that moderate this temporal effect. Thus, the purpose of this systematic review with meta-analysis was to evaluate the eff...

### Cognitive Neuroscience of Memory Consolidation
- **Authors:** Rasch, BjÃ¶rn, Nikolai Axmacher
- **Year:** 2017 | **Citations:** 92
- **Venue:** Studies in neuroscience, psychology and behavioral economics
- **OpenAlex ID:** https://openalex.org/W2587563606
- **Query:** openalex-rq0-consolidation

### Episodic Memory formation: A review of complex Hippocampus input pathways.
- **Authors:** Krubeal Danieli, A. Guyon, I. Bethus
- **Year:** 2023 | **Citations:** 51
- **Venue:** Progress in Neuro-psychopharmacology and Biological Psychiatry
- **Query:** s2-rq0-episodic-review
- **Abstract:** Memories of everyday experiences involve the encoding of a rich and dynamic representation of present objects and their contextual features. Traditionally, the resulting mnemonic trace is referred to as Episodic Memory, i.e. the "what", "where" and "when" of a lived episode. The journey for such mem...

## RQ1-insight

### Neural Activity When People Solve Verbal Problems with Insight
- **Authors:** Mark Beeman, Edward M. Bowden, Jason Haberman
- **Year:** 2004 | **Citations:** 1029
- **Venue:** PLoS Biology
- **PDF:** https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.0020097&type=printable
- **OpenAlex ID:** https://openalex.org/W2087038843
- **Query:** openalex-rq1-insight-neural
- **Abstract:** People sometimes solve problems with a unique process called insight, accompanied by an "Aha!" experience. It has long been unclear whether different cognitive and neural processes lead to insight versus noninsight solutions, or if solutions differ only in subsequent subjective feeling. Recent behav...

### Normative data for 144 compound remote associate problems
- **Authors:** Edward M. Bowden, Mark Beeman
- **Year:** 2003 | **Citations:** 647
- **Venue:** Behavior Research Methods, Instruments, & Computers
- **PDF:** https://link.springer.com/content/pdf/10.3758/BF03195543.pdf
- **OpenAlex ID:** https://openalex.org/W2013214147
- **Query:** openalex-rq1-aha-eeg

### The <i>Aha!</i> Moment
- **Authors:** John Kounios, Mark Beeman
- **Year:** 2009 | **Citations:** 413
- **Venue:** Current Directions in Psychological Science
- **OpenAlex ID:** https://openalex.org/W2121406983
- **Query:** openalex-rq1-aha-eeg
- **Abstract:** A sudden comprehension that solves a problem, reinterprets a situation, explains a joke, or resolves an ambiguous percept is called an insight (i.e., the “Aha! moment”). Psychologists have studied insight using behavioral methods for nearly a century. Recently, the tools of cognitive neuroscience ha...

### A Brain Mechanism for Facilitation of Insight by Positive Affect
- **Authors:** Karuna Subramaniam, John Kounios, Todd B. Parrish
- **Year:** 2008 | **Citations:** 382
- **Venue:** Journal of Cognitive Neuroscience
- **PDF:** https://direct.mit.edu/jocn/article-pdf/21/3/415/1937443/jocn.2009.21057.pdf
- **OpenAlex ID:** https://openalex.org/W2127054206
- **Query:** openalex-rq1-eureka
- **Abstract:** Previous research has shown that people solve insight or creative problems better when in a positive mood (assessed or induced), although the precise mechanisms and neural substrates of this facilitation remain unclear. We assessed mood and personality variables in 79 participants before they attemp...

### Active Inference, Curiosity and Insight
- **Authors:** Karl Friston, Meiyu Lin, Chris Frith
- **Year:** 2017 | **Citations:** 376
- **Venue:** Neural Computation
- **PDF:** https://discovery.ucl.ac.uk/1570070/1/Friston_Active%20Inference%20Curiosity%20and%20Insight.pdf
- **OpenAlex ID:** https://openalex.org/W2743911451
- **Query:** openalex-rq1-eureka
- **Abstract:** This article offers a formal account of curiosity and insight in terms of active (Bayesian) inference. It deals with the dual problem of inferring states of the world and learning its statistical structure. In contrast to current trends in machine learning (e.g., deep learning), we focus on how peop...

### Deconstructing Insight: EEG Correlates of Insightful Problem Solving
- **Authors:** Simone Sandkühler, Joydeep Bhattacharya
- **Year:** 2008 | **Citations:** 219
- **Venue:** PLoS ONE
- **PDF:** https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0001459&type=printable
- **OpenAlex ID:** https://openalex.org/W1970117928
- **Query:** openalex-rq1-eureka
- **Abstract:** Our results provide a first account of cognitive insight by dissociating its constituent components and potential neural correlates.

### Revenge of the “Neurds”: Characterizing Creative Thought in Terms of the Structure and Dyn
- **Authors:** Liane Gabora
- **Year:** 2010 | **Citations:** 156
- **Venue:** Creativity Research Journal
- **PDF:** https://arxiv.org/pdf/1308.5037
- **OpenAlex ID:** https://openalex.org/W2073872868
- **Query:** openalex-rq1-eureka
- **Abstract:** There is cognitive, neurological, and computational support for the hypothesis that defocusing attention results in divergent or associative thought, conducive to insight and finding unusual connections, while focusing attention results in convergent or analytic thought, conducive to rule-based oper...

### The neural basis of insight problem solving: An event-related potential study
- **Authors:** Jiang Qiu, Hong Li, Dong Yang
- **Year:** 2008 | **Citations:** 121
- **Venue:** Brain and Cognition
- **OpenAlex ID:** https://openalex.org/W2014313539
- **Query:** openalex-rq1-insight-neural

### Neural correlates of the “Aha” experiences: Evidence from an fMRI study of insight problem
- **Authors:** Jiang Qiu, Hong Li, Jerwen Jou
- **Year:** 2009 | **Citations:** 119
- **Venue:** Cortex
- **OpenAlex ID:** https://openalex.org/W2068683312
- **Query:** openalex-rq1-insight-neural

### A computational model of scientific insight
- **Authors:** Pat Langley, Randolph Jones
- **Year:** 1986 | **Citations:** 107
- **Venue:** eScholarship (California Digital Library)
- **PDF:** https://escholarship.org/uc/item/54x8v354
- **OpenAlex ID:** https://openalex.org/W100217140
- **Query:** openalex-rq1-eureka
- **Abstract:** Scientific discoveries often take the form of insight, in which previously unseen and unexpected connections suddenly reveal themselves to the mind. In this paper, we present a computational theory of this phenomenon. We recount a number of well-known examples of the process, along with some early a...

### Neural correlates of Eureka moment
- **Authors:** Giulia Sprugnoli, Símone Rossi, Alexandra K. Emmendorfer
- **Year:** 2017 | **Citations:** 80
- **Venue:** Intelligence
- **PDF:** https://www.sciencedirect.com/science/article/am/pii/S0160289616302756?via%3Dihub
- **OpenAlex ID:** https://openalex.org/W2600546158
- **Query:** openalex-rq1-aha-eeg

### TDCS to the right anterior temporal lobe facilitates insight problem-solving
- **Authors:** Carola Salvi, Mark Beeman, Marom Bikson
- **Year:** 2020 | **Citations:** 58
- **Venue:** Scientific Reports
- **PDF:** https://www.nature.com/articles/s41598-020-57724-1.pdf
- **OpenAlex ID:** https://openalex.org/W3001183637
- **Query:** openalex-rq1-aha-eeg
- **Abstract:** Problem-solving is essential for advances in cultural, social, and scientific knowledge. It is also one of the most challenging cognitive processes to facilitate. Some problem-solving is deliberate, but frequently people solve problems with a sudden insight, also known as a Eureka or "Aha!" moment. ...

### Neural correlates of mental preparation for successful insight problem solving
- **Authors:** Fang Tian, Shen Tu, Jiang Qiu
- **Year:** 2010 | **Citations:** 48
- **Venue:** Behavioural Brain Research
- **OpenAlex ID:** https://openalex.org/W1998506670
- **Query:** openalex-rq1-insight-neural

### Neural pathway in the right hemisphere underlies verbal insight problem solving.
- **Authors:** Q. Zhao, Zhong Zhou, H. Xu
- **Year:** 2014 | **Citations:** 35
- **Venue:** Neuroscience
- **Query:** s2-rq1-insight-neural

### Neural pathway in the right hemisphere underlies verbal insight problem solving
- **Authors:** Qingbai Zhao, Zongkui Zhou, Haibo Xu
- **Year:** 2013 | **Citations:** 32
- **Venue:** Neuroscience
- **OpenAlex ID:** https://openalex.org/W1968330762
- **Query:** openalex-rq1-insight-neural

## RQ2-storage

### Six views of embodied cognition
- **Authors:** Margaret Wilson
- **Year:** 2002 | **Citations:** 4438
- **Venue:** Psychonomic Bulletin & Review
- **PDF:** https://link.springer.com/content/pdf/10.3758/BF03196322.pdf
- **OpenAlex ID:** https://openalex.org/W2023015865
- **Query:** openalex-rq2-conversation

### Toward a mechanistic psychology of dialogue
- **Authors:** Martin J. Pickering, Simon Garrod
- **Year:** 2004 | **Citations:** 2593
- **Venue:** Behavioral and Brain Sciences
- **PDF:** https://www.cambridge.org/core/services/aop-cambridge-core/content/view/83442BA495E0D5F81BDB615E4109DBD2/S0140525X04000056a.pdf/div-class-title-toward-a-mechanistic-psychology-of-dialogue-div.pdf
- **OpenAlex ID:** https://openalex.org/W2159398820
- **Query:** openalex-rq2-conversation
- **Abstract:** Traditional mechanistic accounts of language processing derive almost entirely from the study of monologue. Yet, the most natural and basic form of language use is dialogue. As a result, these accounts may only offer limited theories of the mechanisms that underlie language processing in general. We...

### Remembering
- **Authors:** F. C. Bartlett, Walter Kintsch
- **Year:** 1995 | **Citations:** 2362
- **Venue:** Cambridge University Press eBooks
- **OpenAlex ID:** https://openalex.org/W1493772365
- **Query:** openalex-rq2-bartlett-schema
- **Abstract:** In 1932, Cambridge University Press published Remembering, by psychologist, Frederic Bartlett. The landmark book described fascinating studies of memory and presented the theory of schema which informs much of cognitive science and psychology today. In Bartlett's most famous experiment, he had subje...

### Memory for goal-directed events
- **Authors:** Edward Lichtenstein, William F. Brewer
- **Year:** 1980 | **Citations:** 289
- **Venue:** Cognitive Psychology
- **OpenAlex ID:** https://openalex.org/W2013292852
- **Query:** openalex-rq2-reconstructive

### What do connectionism and social psychology offer each other?
- **Authors:** Eliot R. Smith
- **Year:** 1996 | **Citations:** 253
- **Venue:** Journal of Personality and Social Psychology
- **OpenAlex ID:** https://openalex.org/W2136453575
- **Query:** openalex-rq2-reconstructive
- **Abstract:** Social psychologists can benefit from exploring connectionist or parallel distributed processing models of mental representation and process also can contribute much to connectionist theory in return. Connectionist models involve many simple processing units that send activation signals over connect...

### Postexperience Advertising Effects on Consumer Memory
- **Authors:** Kathryn A. Braun
- **Year:** 1999 | **Citations:** 237
- **Venue:** Journal of Consumer Research
- **OpenAlex ID:** https://openalex.org/W2123496781
- **Query:** openalex-rq2-reconstructive
- **Abstract:** Past research suggests that marketing communications create expectations that influence the way consumers subsequently learn from their product experiences. Since postexperience information can also be important and is widespread for established goods and services, it is appropriate to ask about the...

### CONVERSATIONAL MEMORY.
- **Authors:** Laura Stafford, John A. Daly
- **Year:** 1984 | **Citations:** 108
- **Venue:** Human Communication Research
- **OpenAlex ID:** https://openalex.org/W4251883946
- **Query:** openalex-rq2-conversation
- **Abstract:** While there has recently been a notable increase in attempts by memory researchers to focus on more naturalistic stimuli little attention has been paid to conversations. Conversations represent stimuli that are distinctly different in a number of ways from most other stimuli that people are required...

### Bartlett’s concept of schema in reconstruction
- **Authors:** Brady Wagoner
- **Year:** 2013 | **Citations:** 82
- **Venue:** Theory & Psychology
- **PDF:** https://vbn.aau.dk/da/publications/b126d264-ddf2-4b02-b81b-c93dcee09aac
- **OpenAlex ID:** https://openalex.org/W2003331117
- **Query:** openalex-rq2-bartlett-schema
- **Abstract:** The concept of schema was advanced by Frederic Bartlett to provide the basis for a radical temporal alternative to traditional spatial storage theories of memory. Bartlett took remembering out of the head and situated it at the enfolding relation between organism and environment. Through an activity...

### Hedges enhance memory but inhibit retelling
- **Authors:** Kris Liu, Jean E. Fox Tree
- **Year:** 2012 | **Citations:** 73
- **Venue:** Psychonomic Bulletin & Review
- **PDF:** https://link.springer.com/content/pdf/10.3758%2Fs13423-012-0275-1.pdf
- **OpenAlex ID:** https://openalex.org/W2119126732
- **Query:** openalex-rq2-conversation

### Misremembering Bartlett: A study in serial reproduction
- **Authors:** James Ost, Alan Costall
- **Year:** 2002 | **Citations:** 51
- **Venue:** British Journal of Psychology
- **PDF:** https://researchportal.port.ac.uk/ws/files/207753/filetodownload,62635,en.pdf
- **OpenAlex ID:** https://openalex.org/W2048004597
- **Query:** openalex-rq2-bartlett-schema
- **Abstract:** According to much of the recent psychological literature on memory, Bartlett should be credited with the insight that remembering can never be accurate but is, instead, more or less of a distortion (a view to which many modern authors themselves seem to subscribe). In the present paper, we argue tha...

### Levels of Encoding and Retention of Prose
- **Authors:** D. James Dooling, Robert E. Christiaansen
- **Year:** 1977 | **Citations:** 41
- **Venue:** The Psychology of learning and motivation/The psychology of learning and motivation
- **OpenAlex ID:** https://openalex.org/W1014815591
- **Query:** openalex-rq2-bartlett-schema

### Learning to Reminisce: A Case Study
- **Authors:** Judith A. Hudson
- **Year:** 1991 | **Citations:** 34
- **Venue:** Journal of Narrative and Life History
- **OpenAlex ID:** https://openalex.org/W2267872083
- **Query:** openalex-rq2-conversation
- **Abstract:** Abstract This study examined mother-child conversation about past events as a context in which children acquire the discourse skills for talking about the past and develop the ability to recall past events. Conversations about past events were recorded in one mother-child dyad from 20 to 28 months. ...

### What Is It Like to Remember? On Phenomenal Qualities of Memory
- **Authors:** Steen F. Larsen
- **Year:** 2014 | **Citations:** 20
- **Venue:** Psychology Press eBooks
- **OpenAlex ID:** https://openalex.org/W2905490811
- **Query:** openalex-rq2-bartlett-schema
- **Abstract:** The superior vividness of remembered events suggests that autobiographical memory images are not entirely generated from generic representations, but that they do-at least to some extent-have a basis in specific, probably perceptual, traces. Conway has proposed a separate experiential level of autob...

### “Twist Blindness”: The Role of Primacy, Priming, Schemas, and Reconstructive Memory in a F
- **Authors:** Daniel Barratt
- **Year:** 2008 | **Citations:** 17
- **Venue:** —
- **OpenAlex ID:** https://openalex.org/W1534475841
- **Query:** openalex-rq2-reconstructive
- **Abstract:** This chapter contains sections titled: Introduction Methodology Analysis Conclusion Bibliography

### The Reconstructive Play of Memory: Commentary on David Edwards’ Case Study of Schema Thera
- **Authors:** Jefferson A. Singer
- **Year:** 2022 | **Citations:** 1
- **Venue:** Pragmatic Case Studies in Psychotherapy
- **PDF:** https://pcsp.nationalregister.org/index.php/pcsp/article/download/2121/3521
- **OpenAlex ID:** https://openalex.org/W4381088397
- **Query:** openalex-rq2-reconstructive
- **Abstract:** This commentary discusses David Edwards’s (2022) case study of "Kelly’s circle of safety and healing: An extended schema therapy narrative and interpretative investigation," published in Pragmatic Case Studies in Psychotherapy. It examines Edwards’s efforts to integrate his imagistic/experiential th...

## RQ3-retrieval

### Emotion, attention, and the startle reflex.
- **Authors:** Peter J. Lang, Margaret M. Bradley, Bruce N. Cuthbert
- **Year:** 1990 | **Citations:** 2134
- **Venue:** Psychological Review
- **OpenAlex ID:** https://openalex.org/W2021502766
- **Query:** openalex-rq3-context-dependent
- **Abstract:** This theoretical model of emotion is based on research using the startle-probe methodology. It explains inconsistencies in probe studies of attention and fear conditioning and provides a new approach to emotional perception, imagery, and memory. Emotions are organized biphasically, as appetitive or ...

### The Prefrontal Cortex—An Update
- **Authors:** Joaquı́n M. Fuster
- **Year:** 2001 | **Citations:** 1775
- **Venue:** Neuron
- **PDF:** http://www.cell.com/article/S0896627301002859/pdf
- **OpenAlex ID:** https://openalex.org/W2093072166
- **Query:** openalex-rq3-encoding-specificity

### Varieties of Memory and Consciousness: Essays in Honour of Endel Tulving
- **Authors:** Henry L. Roediger, Fergus I. M. Craik
- **Year:** 2014 | **Citations:** 1654
- **Venue:** Medical Entomology and Zoology
- **PDF:** http://ci.nii.ac.jp/ncid/BA0752784X
- **OpenAlex ID:** https://openalex.org/W1586677966
- **Query:** openalex-rq3-context-dependent
- **Abstract:** Contents: Part I:Encoding and Retrieval Processes. H.L. Roediger, III, M.S. Weldon, B.H. Challis, Explaining Dissociations Between Implicit and Explicit Measures of Retention: A Processing Account. F.I.M. Craik, On the Making of Episodes. M.J. Watkins, Willful and Nonwillful Determinants of Memory. ...

### Ex Vivo Isolation and Characterization of Cd4+Cd25+ T Cells with Regulatory Properties fro
- **Authors:** Detlef Dieckmann, Heidi Plöttner, Susanne Berchtold
- **Year:** 2001 | **Citations:** 1129
- **Venue:** The Journal of Experimental Medicine
- **PDF:** http://jem.rupress.org/content/jem/193/11/1303.full.pdf
- **OpenAlex ID:** https://openalex.org/W2122445377
- **Query:** openalex-rq3-context-dependent
- **Abstract:** It has been known for years that rodents harbor a unique population of CD4(+)CD25(+) "professional" regulatory/suppressor T cells that is crucial for the prevention of spontaneous autoimmune diseases. Here we demonstrate that CD4(+)CD25(+)CD45RO(+) T cells (mean 6% of CD4(+) T cells) are present in ...

### The Neuropsychopharmacology of Fronto-Executive Function: Monoaminergic Modulation
- **Authors:** Trevor W. Robbins, Amy F.T. Arnsten
- **Year:** 2009 | **Citations:** 963
- **Venue:** Annual Review of Neuroscience
- **PDF:** https://www.ncbi.nlm.nih.gov/pmc/articles/2863127
- **OpenAlex ID:** https://openalex.org/W2160985876
- **Query:** openalex-rq3-context-dependent
- **Abstract:** We review the modulatory effects of the catecholamine neurotransmitters noradrenaline and dopamine on prefrontal cortical function. The effects of pharmacologic manipulations of these systems, sometimes in comparison with the indoleamine serotonin (5-HT), on performance on a variety of tasks that ta...

### Précis of Elements of episodic memory
- **Authors:** Endel Tulving
- **Year:** 1984 | **Citations:** 804
- **Venue:** Behavioral and Brain Sciences
- **OpenAlex ID:** https://openalex.org/W2034470020
- **Query:** openalex-rq3-encoding-specificity
- **Abstract:** Abstract Elements of episodic memory (Tulving 1983b) consists of three parts. Part I argues for the distinction between episodic and semantic memory as functionally separate albeit closely interacting systems. It begins with a review of the 1972 essay on the topic (Tulving 1972) and its shortcomings...

### Effective LSTMs for Target-Dependent Sentiment Classification
- **Authors:** Duyu Tang, Bing Qin, Xiaocheng Feng
- **Year:** 2015 | **Citations:** 559
- **Venue:** arXiv (Cornell University)
- **PDF:** https://arxiv.org/pdf/1512.01100
- **OpenAlex ID:** https://openalex.org/W2529550020
- **Query:** openalex-rq3-context-dependent
- **Abstract:** Target-dependent sentiment classification remains a challenge: modeling the semantic relatedness of a target with its context words in a sentence. Different context words have different influences on determining the sentiment polarity of a sentence towards the target. Therefore, it is desirable to i...

### Working Memory Contributions to Human Learning and Remembering
- **Authors:** Anthony D. Wagner
- **Year:** 1999 | **Citations:** 194
- **Venue:** Neuron
- **PDF:** http://www.cell.com/article/S0896627300806741/pdf
- **OpenAlex ID:** https://openalex.org/W1971658102
- **Query:** openalex-rq3-encoding-specificity

### Beyond HERA: Contributions of specific prefrontal brain areas to long-term memory retrieva
- **Authors:** Randy L. Buckner
- **Year:** 1996 | **Citations:** 184
- **Venue:** Psychonomic Bulletin & Review
- **PDF:** https://link.springer.com/content/pdf/10.3758/BF03212413.pdf
- **OpenAlex ID:** https://openalex.org/W2083492091
- **Query:** openalex-rq3-encoding-specificity

### Encoding specificity: Relation between recall superiority and recognition failure.
- **Authors:** Sandor Wiseman, Endel Tulving
- **Year:** 1976 | **Citations:** 107
- **Venue:** Journal of Experimental Psychology Human Learning & Memory
- **OpenAlex ID:** https://openalex.org/W2131343965
- **Query:** openalex-rq3-encoding-specificity
- **Abstract:** The results of four experiments show that (a) recall superiority over recognition is reversed by the use of unrelated word pairs in the study list, and (b) the reversal of recall superiority leaves intact the phenomenon of recognition failure of recallable words. These results extend the generality ...

## RQ4-metacog

### Handbook of Metacognition in Education
- **Authors:** 
- **Year:** 2009 | **Citations:** 1471
- **Venue:** —
- **OpenAlex ID:** https://openalex.org/W595197191
- **Query:** openalex-rq4-judgment-learning
- **Abstract:** Foreword, Robert J. Sternberg Chapter 1. A Growing Sense of Agency, Douglas J. Hacker, John Dunlosky, and Arthur C. Graesser Part I: Comprehension Strategies Chapter 2. The Role of Metacognition in Understanding and Supporting Reading Comprehension, Margaret G. McKeown and Isabel L. Beck Chapter 3. ...

### Intuition in insight and noninsight problem solving
- **Authors:** Janet Metcalfe, David Wiebe
- **Year:** 1987 | **Citations:** 745
- **Venue:** Memory & Cognition
- **PDF:** https://link.springer.com/content/pdf/10.3758/BF03197722.pdf
- **OpenAlex ID:** https://openalex.org/W2103818390
- **Query:** openalex-rq4-feeling-knowing

### Accuracy of metacognitive monitoring affects learning of texts.
- **Authors:** Keith W. Thiede, Mary C. Anderson, David J. Therriault
- **Year:** 2003 | **Citations:** 742
- **Venue:** Journal of Educational Psychology
- **OpenAlex ID:** https://openalex.org/W2099893266
- **Query:** openalex-rq4-metacognitive-accuracy
- **Abstract:** Metacognitive monitoring affects regulation of study, and this affects overall learning. The authors created differences in monitoring accuracy by instructing participants to generate a list of 5 keywords that captured the essence of each text. Accuracy was greater for a group that wrote keywords af...

### Implicit Memory and Metacognition
- **Authors:** 
- **Year:** 2014 | **Citations:** 488
- **Venue:** Psychology Press eBooks
- **OpenAlex ID:** https://openalex.org/W1534024588
- **Query:** openalex-rq4-feeling-knowing
- **Abstract:** Contents: Preface. J.F. Kihlstrom, V.A. Shames, J.D. Dorfman, Intimations of Memory and Thought. P. Graf, A.R. Birt, Explicit and Implicit Memory Retrieval: Intentions and Strategies. L.M. Reder, C.D. Schunn, Metacognition Does Not Imply Awareness: Strategy Choice Is Governed by Implicit Learning an...

### The comparative psychology of uncertainty monitoring and metacognition
- **Authors:** J. David Smith, Wendy E. Shields, David A. Washburn
- **Year:** 2003 | **Citations:** 403
- **Venue:** Behavioral and Brain Sciences
- **OpenAlex ID:** https://openalex.org/W2042289516
- **Query:** openalex-rq4-feeling-knowing
- **Abstract:** Researchers have begun to explore animals' capacities for uncertainty monitoring and metacognition. This exploration could extend the study of animal self-awareness and establish the relationship of self-awareness to other-awareness. It could sharpen descriptions of metacognition in the human litera...

### The Oxford Handbook of Metamemory
- **Authors:** Dunlosky, John, Tauber, Sarah K.
- **Year:** 2015 | **Citations:** 402
- **Venue:** Oxford University Press eBooks
- **OpenAlex ID:** https://openalex.org/W2500107058
- **Query:** openalex-rq4-judgment-learning
- **Abstract:** The Oxford Handbook of Metamemory Edited by John Dunlosky and Sarah K. Tauber Part I. Preface (R. Bjork) Part II. Introduction to Metamemory 1. A Brief History of Metamemory Research and Handbook Overview (Tauber and Dunlosky) 2. Methodology for Investigating Human Metamemory: Problems and Pitfalls ...

### Feeling of knowing in memory and problem solving.
- **Authors:** Janet Metcalfe
- **Year:** 1986 | **Citations:** 334
- **Venue:** Journal of Experimental Psychology Learning Memory and Cognition
- **OpenAlex ID:** https://openalex.org/W2066379812
- **Query:** openalex-rq4-feeling-knowing
- **Abstract:** This study investigates feelings of knowing for problem solving and memory. In Experiment 1 subjects judged their feelings of knowing to trivia questions they had been unable to answer, then performed a multiple-choice recognition test In a second task, subjects gave feeling-of-knowing judgments for...

### Handbook of Metamemory and Memory
- **Authors:** John Dunlosky, Robert A. Bjork
- **Year:** 2013 | **Citations:** 296
- **Venue:** —
- **PDF:** https://ci.nii.ac.jp/ncid/BA86929816
- **OpenAlex ID:** https://openalex.org/W635788281
- **Query:** openalex-rq4-feeling-knowing
- **Abstract:** J. Dunlosky, R.A. Bjork, Introduction: The Integrated Nature of Metamemory and Memory. J. Metcalfe, Evolution of Metacognition. J.P. Van Overschelde, Metacognition: Knowing About Knowing. A.S. Benjamin, M. Diaz, Measurement of Relative Metamnemonic Accuracy. B.A. Spellman, A. Blumenthal, R.A. Bjork,...

### Metacognitive Monitoring Accuracy and Student Performance in the Postsecondary Classroom.
- **Authors:** John L. Nietfeld, Li Cao, Jason W. Osborne
- **Year:** 2005 | **Citations:** 231
- **Venue:** The Journal of Experimental Education
- **OpenAlex ID:** https://openalex.org/W4660786
- **Query:** openalex-rq4-metacognitive-accuracy
- **Abstract:** The literature on metacognition suggests that having students practice metacognitive monitoring consistently should lead to significant improvement over time. In this study, students practiced metacognitive monitoring through the course of a full semester. The authors then examined changes in monito...

### Judgments of learning are influenced by memory for past test
- **Authors:** Bridgid Finn, Janet Metcalfe
- **Year:** 2007 | **Citations:** 122
- **Venue:** Journal of Memory and Language
- **PDF:** https://www.ncbi.nlm.nih.gov/pmc/articles/2836879
- **OpenAlex ID:** https://openalex.org/W2128802273
- **Query:** openalex-rq4-judgment-learning

### Eyewitness memory: Balancing the accuracy, precision and quantity of information through m
- **Authors:** Jacqueline R. Evans, Ronald P. Fisher
- **Year:** 2010 | **Citations:** 105
- **Venue:** Applied Cognitive Psychology
- **OpenAlex ID:** https://openalex.org/W2057474990
- **Query:** openalex-rq4-metacognitive-accuracy
- **Abstract:** Although memory deteriorates over time, people may be able to maintain high accuracy by metacognitively monitoring the quality of their memories and strategically controlling their memory reports. We test two mechanisms of metacognitive control: Exercising a report option (withholding uncertain resp...

### Overconfidence in children's multi-trial judgments of learning
- **Authors:** Bridgid Finn, Janet Metcalfe
- **Year:** 2014 | **Citations:** 86
- **Venue:** Learning and Instruction
- **OpenAlex ID:** https://openalex.org/W2059731449
- **Query:** openalex-rq4-judgment-learning

### Metacognitive monitoring and control processes in children with autism spectrum disorder: 
- **Authors:** Catherine Grainger, David M. Williams, Sophie E. Lind
- **Year:** 2016 | **Citations:** 71
- **Venue:** Consciousness and Cognition
- **PDF:** https://www.sciencedirect.com/science/article/pii/S1053810016300320
- **OpenAlex ID:** https://openalex.org/W2300270475
- **Query:** openalex-rq4-metacognitive-accuracy

### Changes in metacognitive monitoring accuracy in an introductory physics course
- **Authors:** Jason Morphew
- **Year:** 2020 | **Citations:** 47
- **Venue:** Metacognition and Learning
- **OpenAlex ID:** https://openalex.org/W3082065087
- **Query:** openalex-rq4-metacognitive-accuracy
