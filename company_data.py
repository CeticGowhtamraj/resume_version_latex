"""
company_data.py — Company Suggestions Database
Covers 9 job roles × 5 experience levels with curated company lists,
career page URLs, work culture tags, and salary range indicators.

Roles  : Data Analyst, Data Scientist, Data Engineer, Web Developer,
         Android Developer, UI/UX Designer, Software Engineer,
         BI Analyst, SQL Developer
Levels : Fresher, Entry Level, Intermediate, Senior, Expert
"""

# ─────────────────────────────────────────────────────────────────────────────
# ROLE ALIASES  — map the analyzer's detected role strings to our keys
# ─────────────────────────────────────────────────────────────────────────────
ROLE_ALIASES = {
    # exact matches
    "data analyst":        "data_analyst",
    "data scientist":      "data_scientist",
    "data engineer":       "data_engineer",
    "web developer":       "web_developer",
    "full stack developer":"web_developer",
    "android developer":   "android_developer",
    "mobile developer":    "android_developer",
    "ui/ux designer":      "ui_ux_designer",
    "software engineer":   "software_engineer",
    "bi analyst":          "bi_analyst",
    "sql developer":       "sql_developer",
    # partials handled in get_suggestions()
}

# ─────────────────────────────────────────────────────────────────────────────
# COMPANY DATABASE
# Each entry:
#   name        – display name
#   careers_url – direct careers/jobs page
#   type        – "Product" | "Service" | "Startup" | "MNC" | "Consulting"
#   tags        – culture / perk keywords shown as chips
#   salary_band – "₹2–5 LPA" style indicator
# ─────────────────────────────────────────────────────────────────────────────

COMPANIES = {

    # ══════════════════════════════════════════════════════
    #  DATA ANALYST
    # ══════════════════════════════════════════════════════
    "data_analyst": {

        "Fresher": [
            {"name": "Mu Sigma",         "careers_url": "https://www.mu-sigma.com/careers",         "type": "Analytics",   "tags": ["Analytics Leader","Training Program","Bangalore"],   "salary_band": "₹3–5 LPA"},
            {"name": "Fractal Analytics","careers_url": "https://fractal.ai/careers",                "type": "Analytics",   "tags": ["AI Focus","Global Clients","Learning Culture"],       "salary_band": "₹3.5–6 LPA"},
            {"name": "EXL Service",      "careers_url": "https://www.exlservice.com/careers",        "type": "Consulting",  "tags": ["Analytics BPO","US Clients","Structured Growth"],    "salary_band": "₹3–5 LPA"},
            {"name": "Wipro",            "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["Large Company","Training","Pan India"],               "salary_band": "₹3.5–5 LPA"},
            {"name": "Infosys",          "careers_url": "https://www.infosys.com/careers",           "type": "Service",     "tags": ["InfyTQ","Structured Onboarding","Pan India"],         "salary_band": "₹3.6–5 LPA"},
            {"name": "Accenture",        "careers_url": "https://www.accenture.com/in-en/careers",   "type": "MNC",         "tags": ["Global MNC","Analytics CoE","Diverse Projects"],      "salary_band": "₹4–6 LPA"},
        ],

        "Entry Level": [
            {"name": "Nielsen",          "careers_url": "https://www.nielsen.com/careers",           "type": "MNC",         "tags": ["Consumer Data","Market Research","FMCG Domain"],      "salary_band": "₹4–7 LPA"},
            {"name": "Genpact",          "careers_url": "https://www.genpact.com/careers",           "type": "Consulting",  "tags": ["Analytics BPO","Process Excellence","Global Scale"],  "salary_band": "₹4–7 LPA"},
            {"name": "WNS Global",       "careers_url": "https://www.wns.com/careers",               "type": "Consulting",  "tags": ["Decision Analytics","BPM","UK/US Clients"],           "salary_band": "₹4–8 LPA"},
            {"name": "Amazon",           "careers_url": "https://www.amazon.jobs",                   "type": "Product",     "tags": ["FAANG","High Bar","Data-Driven Culture"],              "salary_band": "₹8–14 LPA"},
            {"name": "Flipkart",         "careers_url": "https://www.flipkartcareers.com",           "type": "Product",     "tags": ["E-Commerce","Fast Paced","India Scale"],               "salary_band": "₹7–12 LPA"},
            {"name": "Capgemini",        "careers_url": "https://www.capgemini.com/in-en/careers",   "type": "MNC",         "tags": ["Digital Analytics","European MNC","Hybrid Work"],      "salary_band": "₹5–8 LPA"},
        ],

        "Intermediate": [
            {"name": "Google",           "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","Top Pay","Perks"],                             "salary_band": "₹18–35 LPA"},
            {"name": "Microsoft",        "careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["FAANG","Azure","Work-Life Balance"],                   "salary_band": "₹16–30 LPA"},
            {"name": "Swiggy",           "careers_url": "https://careers.swiggy.com",                "type": "Startup",     "tags": ["HyperGrowth","Food-Tech","Real-Time Analytics"],       "salary_band": "₹10–18 LPA"},
            {"name": "Razorpay",         "careers_url": "https://razorpay.com/jobs",                 "type": "Startup",     "tags": ["Fintech","Unicorn","High Ownership"],                  "salary_band": "₹12–20 LPA"},
            {"name": "Deloitte",         "careers_url": "https://www2.deloitte.com/in/en/careers",   "type": "Consulting",  "tags": ["Big 4","Enterprise Clients","Analytics Strategy"],     "salary_band": "₹8–15 LPA"},
            {"name": "KPMG",             "careers_url": "https://home.kpmg/in/en/home/careers",      "type": "Consulting",  "tags": ["Big 4","Risk Analytics","Cross-Industry"],             "salary_band": "₹8–14 LPA"},
        ],

        "Senior": [
            {"name": "Meta",             "careers_url": "https://www.metacareers.com",               "type": "Product",     "tags": ["FAANG","RSU","Top Compensation"],                      "salary_band": "₹35–70 LPA"},
            {"name": "Uber",             "careers_url": "https://www.uber.com/in/en/careers",        "type": "Product",     "tags": ["Mobility Data","Global Scale","High Impact"],          "salary_band": "₹25–45 LPA"},
            {"name": "Walmart Global Tech","careers_url":"https://careers.walmart.com",              "type": "Product",     "tags": ["Retail Analytics","Large Scale","Bangalore Hub"],      "salary_band": "₹22–40 LPA"},
            {"name": "McKinsey & Co.",   "careers_url": "https://www.mckinsey.com/careers",          "type": "Consulting",  "tags": ["Strategy + Analytics","Prestige","Global Travel"],    "salary_band": "₹25–50 LPA"},
            {"name": "BCG Gamma",        "careers_url": "https://careers.bcg.com",                   "type": "Consulting",  "tags": ["AI Division","Top Consulting","Data Science+"],        "salary_band": "₹25–50 LPA"},
            {"name": "Groww",            "careers_url": "https://groww.in/open-positions",           "type": "Startup",     "tags": ["Fintech","Unicorn","Wealth-Tech"],                     "salary_band": "₹20–35 LPA"},
        ],

        "Expert": [
            {"name": "Apple",            "careers_url": "https://www.apple.com/careers/in",          "type": "Product",     "tags": ["Premium Brand","High Bar","RSU"],                      "salary_band": "₹50–90 LPA"},
            {"name": "Goldman Sachs",    "careers_url": "https://www.goldmansachs.com/careers",      "type": "MNC",         "tags": ["Quant Finance","Bangalore Eng Hub","High Pay"],        "salary_band": "₹40–80 LPA"},
            {"name": "Airbnb",           "careers_url": "https://careers.airbnb.com",                "type": "Product",     "tags": ["Travel Data","Global Remote","Strong Culture"],        "salary_band": "₹50–100 LPA"},
            {"name": "LinkedIn",         "careers_url": "https://careers.linkedin.com",              "type": "Product",     "tags": ["Professional Network Data","Microsoft Umbrella"],      "salary_band": "₹40–75 LPA"},
            {"name": "Atlassian",        "careers_url": "https://www.atlassian.com/company/careers", "type": "Product",     "tags": ["Remote-First","Collaboration Tools","Strong Pay"],     "salary_band": "₹45–85 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  DATA SCIENTIST
    # ══════════════════════════════════════════════════════
    "data_scientist": {

        "Fresher": [
            {"name": "Fractal Analytics","careers_url": "https://fractal.ai/careers",                "type": "Analytics",   "tags": ["AI/ML Focus","Great Mentorship","Global Clients"],     "salary_band": "₹5–8 LPA"},
            {"name": "Tiger Analytics",  "careers_url": "https://www.tigeranalytics.com/careers",    "type": "Analytics",   "tags": ["Pure Analytics","US Projects","Chennai/Bangalore"],    "salary_band": "₹4–7 LPA"},
            {"name": "Mu Sigma",         "careers_url": "https://www.mu-sigma.com/careers",          "type": "Analytics",   "tags": ["Decision Science","Analytics Academy","Bangalore"],    "salary_band": "₹4–6 LPA"},
            {"name": "Wipro HOLMES",     "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["AI Division","Training","Large Scale"],                "salary_band": "₹4–6 LPA"},
            {"name": "TCS Research",     "careers_url": "https://www.tcs.com/careers",               "type": "Service",     "tags": ["R&D Division","Published Research","Pan India"],       "salary_band": "₹4–7 LPA"},
            {"name": "Sigmoid",          "careers_url": "https://www.sigmoid.com/careers",           "type": "Analytics",   "tags": ["Data Engineering+ML","Startup Feel","Bangalore"],      "salary_band": "₹5–9 LPA"},
        ],

        "Entry Level": [
            {"name": "Amazon ML",        "careers_url": "https://www.amazon.jobs",                   "type": "Product",     "tags": ["FAANG","Applied Science","Scale"],                     "salary_band": "₹12–20 LPA"},
            {"name": "Myntra",           "careers_url": "https://careers.myntra.com",                "type": "Product",     "tags": ["Fashion-Tech","Recommendation Systems","Flipkart Group"],"salary_band": "₹10–18 LPA"},
            {"name": "PhonePe",          "careers_url": "https://careers.phonepe.com",               "type": "Startup",     "tags": ["Fintech","Unicorn","Payments Data"],                   "salary_band": "₹10–18 LPA"},
            {"name": "Ola",              "careers_url": "https://www.olacabs.com/careers",           "type": "Startup",     "tags": ["Mobility ML","Real-Time Data","Fast Growth"],          "salary_band": "₹10–16 LPA"},
            {"name": "H2O.ai",           "careers_url": "https://www.h2o.ai/careers",                "type": "Product",     "tags": ["AutoML Platform","Remote","Global Team"],              "salary_band": "₹10–18 LPA"},
            {"name": "Sigmoid",          "careers_url": "https://www.sigmoid.com/careers",           "type": "Analytics",   "tags": ["ML Engineering","Data Pipelines","Growth Stage"],      "salary_band": "₹8–14 LPA"},
        ],

        "Intermediate": [
            {"name": "Google DeepMind",  "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["Top AI Research","FAANG","London/Bangalore"],          "salary_band": "₹25–50 LPA"},
            {"name": "Microsoft AI",     "careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["Azure ML","Research Division","Strong WLB"],           "salary_band": "₹20–40 LPA"},
            {"name": "Zomato",           "careers_url": "https://www.zomato.com/careers",            "type": "Startup",     "tags": ["Food-Tech","Demand Forecasting","India Scale"],        "salary_band": "₹15–25 LPA"},
            {"name": "CRED",             "careers_url": "https://careers.cred.club",                 "type": "Startup",     "tags": ["Credit Data","Design Culture","Unicorn"],              "salary_band": "₹18–30 LPA"},
            {"name": "Salesforce AI",    "careers_url": "https://www.salesforce.com/company/careers","type": "Product",     "tags": ["Einstein AI","CRM Data","Hybrid Work"],               "salary_band": "₹20–35 LPA"},
            {"name": "Adobe Research",   "careers_url": "https://www.adobe.com/careers",             "type": "Product",     "tags": ["Creative AI","Sensei Platform","Noida/Bangalore"],     "salary_band": "₹18–32 LPA"},
        ],

        "Senior": [
            {"name": "Meta AI",          "careers_url": "https://www.metacareers.com",               "type": "Product",     "tags": ["FAANG","LLMs/GenAI","Top RSU"],                        "salary_band": "₹45–90 LPA"},
            {"name": "Netflix",          "careers_url": "https://jobs.netflix.com",                  "type": "Product",     "tags": ["Rec Systems","Freedom & Responsibility","Top Pay"],    "salary_band": "₹50–100 LPA"},
            {"name": "Stripe",           "careers_url": "https://stripe.com/jobs",                   "type": "Product",     "tags": ["Payments ML","Remote-Friendly","Global Scale"],        "salary_band": "₹40–80 LPA"},
            {"name": "IBM Research",     "careers_url": "https://www.ibm.com/careers",               "type": "MNC",         "tags": ["Watson AI","Research Papers","Bangalore Hub"],         "salary_band": "₹25–45 LPA"},
            {"name": "Palantir",         "careers_url": "https://www.palantir.com/careers",          "type": "Product",     "tags": ["Defense/Enterprise AI","Mission-Driven","High Bar"],   "salary_band": "₹35–65 LPA"},
        ],

        "Expert": [
            {"name": "OpenAI",           "careers_url": "https://openai.com/careers",                "type": "Product",     "tags": ["Frontier AI","Mission-Driven","Top Comp"],             "salary_band": "₹80–200 LPA"},
            {"name": "Anthropic",        "careers_url": "https://www.anthropic.com/careers",         "type": "Product",     "tags": ["AI Safety","Frontier Research","Top Comp"],            "salary_band": "₹80–200 LPA"},
            {"name": "Google Brain",     "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["Top AI Research","Publications","FAANG+"],             "salary_band": "₹70–150 LPA"},
            {"name": "Apple ML",         "careers_url": "https://www.apple.com/careers/in",          "type": "Product",     "tags": ["On-Device ML","Privacy-First","Top Pay"],              "salary_band": "₹60–130 LPA"},
            {"name": "Two Sigma",        "careers_url": "https://www.twosigma.com/careers",          "type": "Consulting",  "tags": ["Quant Finance","ML + Finance","NYC/Remote"],           "salary_band": "₹80–180 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  DATA ENGINEER
    # ══════════════════════════════════════════════════════
    "data_engineer": {

        "Fresher": [
            {"name": "Sigmoid",          "careers_url": "https://www.sigmoid.com/careers",           "type": "Analytics",   "tags": ["Pipelines","Spark/Kafka","Great Learning Env"],        "salary_band": "₹4–7 LPA"},
            {"name": "Tata Consultancy", "careers_url": "https://www.tcs.com/careers",               "type": "Service",     "tags": ["Large Scale","Training","Pan India"],                  "salary_band": "₹3.5–6 LPA"},
            {"name": "Infosys BPM",      "careers_url": "https://www.infosys.com/careers",           "type": "Service",     "tags": ["ETL Focus","Structured Growth","Pan India"],           "salary_band": "₹3.6–6 LPA"},
            {"name": "Hexaware",         "careers_url": "https://www.hexaware.com/careers",          "type": "Service",     "tags": ["Cloud Migration","Data Platforms","Mumbai"],           "salary_band": "₹4–7 LPA"},
            {"name": "Mphasis",          "careers_url": "https://careers.mphasis.com",               "type": "Service",     "tags": ["BFSI Domain","AWS/Azure","Bangalore"],                 "salary_band": "₹4–6 LPA"},
            {"name": "Persistent Sys",   "careers_url": "https://www.persistent.com/careers",        "type": "Service",     "tags": ["Product Engineering","Agile","Pune"],                  "salary_band": "₹4–7 LPA"},
        ],

        "Entry Level": [
            {"name": "Cloudera",         "careers_url": "https://www.cloudera.com/about/careers",    "type": "Product",     "tags": ["Hadoop/Spark","Data Platform","Santa Clara/Remote"],   "salary_band": "₹8–14 LPA"},
            {"name": "Databricks",       "careers_url": "https://www.databricks.com/company/careers","type": "Product",     "tags": ["Delta Lake","Lakehouse","Fast Growth"],               "salary_band": "₹10–18 LPA"},
            {"name": "Swiggy Data",      "careers_url": "https://careers.swiggy.com",                "type": "Startup",     "tags": ["Real-Time Pipelines","Fast Iteration","Bangalore"],    "salary_band": "₹8–15 LPA"},
            {"name": "Razorpay",         "careers_url": "https://razorpay.com/jobs",                 "type": "Startup",     "tags": ["Payments Data","Kafka/Flink","High Ownership"],        "salary_band": "₹10–18 LPA"},
            {"name": "Walmart Lab",      "careers_url": "https://careers.walmart.com",               "type": "Product",     "tags": ["Petabyte Scale","Spark","Bangalore"],                  "salary_band": "₹10–16 LPA"},
            {"name": "Capgemini DE",     "careers_url": "https://www.capgemini.com/in-en/careers",   "type": "MNC",         "tags": ["Azure/GCP","Client Projects","Hybrid Work"],           "salary_band": "₹6–10 LPA"},
        ],

        "Intermediate": [
            {"name": "Snowflake",        "careers_url": "https://careers.snowflake.com",             "type": "Product",     "tags": ["Cloud Data Warehouse","Hyper Growth","Remote OK"],     "salary_band": "₹18–30 LPA"},
            {"name": "Airbnb",           "careers_url": "https://careers.airbnb.com",                "type": "Product",     "tags": ["Airflow","Spark","Strong Eng Culture"],                "salary_band": "₹20–35 LPA"},
            {"name": "Uber Engineering", "careers_url": "https://www.uber.com/in/en/careers",        "type": "Product",     "tags": ["Flink/Kafka","Massive Scale","Open Source"],           "salary_band": "₹20–38 LPA"},
            {"name": "LinkedIn Engg",    "careers_url": "https://careers.linkedin.com",              "type": "Product",     "tags": ["Kafka Creators","Data Platform","Microsoft Group"],    "salary_band": "₹20–36 LPA"},
            {"name": "Zomato Platform",  "careers_url": "https://www.zomato.com/careers",            "type": "Startup",     "tags": ["Order Data","Real-Time Systems","India Scale"],        "salary_band": "₹15–25 LPA"},
            {"name": "Thoughtworks",     "careers_url": "https://www.thoughtworks.com/careers",      "type": "Consulting",  "tags": ["Data Mesh","Agile","Global Clients"],                  "salary_band": "₹14–22 LPA"},
        ],

        "Senior": [
            {"name": "Netflix DE",       "careers_url": "https://jobs.netflix.com",                  "type": "Product",     "tags": ["Iceberg/Spark","Freedom Culture","Top Pay"],           "salary_band": "₹50–90 LPA"},
            {"name": "Amazon AWS",       "careers_url": "https://www.amazon.jobs",                   "type": "Product",     "tags": ["Redshift/Glue","FAANG","High Bar"],                    "salary_band": "₹30–55 LPA"},
            {"name": "Palantir DE",      "careers_url": "https://www.palantir.com/careers",          "type": "Product",     "tags": ["Enterprise Data","Gotham/Foundry","Mission-Driven"],  "salary_band": "₹35–60 LPA"},
            {"name": "Google Cloud",     "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["BigQuery/Dataflow","FAANG","Hyderabad/Bangalore"],     "salary_band": "₹35–65 LPA"},
            {"name": "dbt Labs",         "careers_url": "https://www.getdbt.com/careers",            "type": "Product",     "tags": ["Data Transformation","Analytics Eng","Remote-First"],  "salary_band": "₹30–55 LPA"},
        ],

        "Expert": [
            {"name": "Confluent",        "careers_url": "https://www.confluent.io/careers",          "type": "Product",     "tags": ["Kafka Company","Streaming Pioneer","Remote OK"],       "salary_band": "₹55–110 LPA"},
            {"name": "Stripe Data",      "careers_url": "https://stripe.com/jobs",                   "type": "Product",     "tags": ["Payments at Scale","Strong Eng","Global Remote"],      "salary_band": "₹50–100 LPA"},
            {"name": "Databricks Sr",    "careers_url": "https://www.databricks.com/company/careers","type": "Product",     "tags": ["Lakehouse Pioneer","High Comp","Pre-IPO"],             "salary_band": "₹60–120 LPA"},
            {"name": "Apple DE",         "careers_url": "https://www.apple.com/careers/in",          "type": "Product",     "tags": ["Privacy-First","iPhone/Services Data","Top Pay"],      "salary_band": "₹60–120 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  WEB DEVELOPER / FULL STACK
    # ══════════════════════════════════════════════════════
    "web_developer": {

        "Fresher": [
            {"name": "Infosys",          "careers_url": "https://www.infosys.com/careers",           "type": "Service",     "tags": ["Training Program","Large Scale","Pan India"],          "salary_band": "₹3.6–5 LPA"},
            {"name": "Wipro",            "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["Web Projects","Training","Pan India"],                 "salary_band": "₹3.5–5 LPA"},
            {"name": "HCL Technologies","careers_url": "https://www.hcltech.com/careers",            "type": "Service",     "tags": ["IT Service","Global Delivery","Noida/Chennai"],        "salary_band": "₹3.5–5 LPA"},
            {"name": "Freshworks",       "careers_url": "https://www.freshworks.com/company/careers","type": "Product",     "tags": ["SaaS Product","Chennai HQ","Good Culture"],            "salary_band": "₹5–9 LPA"},
            {"name": "Zoho",             "careers_url": "https://www.zoho.com/careers",              "type": "Product",     "tags": ["Bootstrapped","Diverse Products","Chennai/Remote"],    "salary_band": "₹4–8 LPA"},
            {"name": "Hasura",           "careers_url": "https://hasura.io/careers",                 "type": "Startup",     "tags": ["GraphQL","Remote-First","Open Source"],                "salary_band": "₹5–9 LPA"},
        ],

        "Entry Level": [
            {"name": "Postman",          "careers_url": "https://www.postman.com/company/careers",   "type": "Product",     "tags": ["API Platform","Bangalore/SF","Developer-First"],       "salary_band": "₹8–14 LPA"},
            {"name": "BrowserStack",     "careers_url": "https://www.browserstack.com/careers",      "type": "Product",     "tags": ["Dev Tools","Mumbai","Remote OK"],                      "salary_band": "₹8–14 LPA"},
            {"name": "Chargebee",        "careers_url": "https://www.chargebee.com/careers",         "type": "Startup",     "tags": ["SaaS Billing","Chennai","Unicorn"],                    "salary_band": "₹8–13 LPA"},
            {"name": "Turing",           "careers_url": "https://www.turing.com/careers",            "type": "Product",     "tags": ["Remote-First","US Clients","Comp in USD"],             "salary_band": "₹10–18 LPA"},
            {"name": "Springworks",      "careers_url": "https://www.springworks.in/careers",        "type": "Startup",     "tags": ["HR Tech","React/Node","Bangalore"],                    "salary_band": "₹7–12 LPA"},
            {"name": "Moengage",         "careers_url": "https://www.moengage.com/about/careers",    "type": "Startup",     "tags": ["MarTech","Unicorn","Bangalore/Remote"],                "salary_band": "₹8–14 LPA"},
        ],

        "Intermediate": [
            {"name": "Atlassian",        "careers_url": "https://www.atlassian.com/company/careers", "type": "Product",     "tags": ["Remote-First","TEAM Anywhere","Strong Pay"],           "salary_band": "₹20–35 LPA"},
            {"name": "Razorpay",         "careers_url": "https://razorpay.com/jobs",                 "type": "Startup",     "tags": ["Fintech","Unicorn","React/Go Stack"],                  "salary_band": "₹15–25 LPA"},
            {"name": "Meesho",           "careers_url": "https://meesho.io/jobs",                    "type": "Startup",     "tags": ["Social Commerce","Unicorn","India Scale"],             "salary_band": "₹14–22 LPA"},
            {"name": "Druva",            "careers_url": "https://www.druva.com/company/careers",     "type": "Product",     "tags": ["Cloud Data Protection","US Clients","Pune"],          "salary_band": "₹15–25 LPA"},
            {"name": "Sprinklr",         "careers_url": "https://www.sprinklr.com/company/careers",  "type": "Product",     "tags": ["Unified CXM","Gurgaon","Pre-IPO"],                     "salary_band": "₹15–24 LPA"},
            {"name": "Gitlab",           "careers_url": "https://about.gitlab.com/jobs",             "type": "Product",     "tags": ["All-Remote","Open Source","DevOps Platform"],          "salary_band": "₹20–35 LPA"},
        ],

        "Senior": [
            {"name": "Google",           "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","Top Pay","Eng Excellence"],                    "salary_band": "₹35–70 LPA"},
            {"name": "Shopify",          "careers_url": "https://www.shopify.com/careers",           "type": "Product",     "tags": ["Digital-by-Default","Global Remote","Commerce"],       "salary_band": "₹30–60 LPA"},
            {"name": "Vercel",           "careers_url": "https://vercel.com/careers",                "type": "Product",     "tags": ["Next.js","Jamstack","Remote-First"],                   "salary_band": "₹30–55 LPA"},
            {"name": "Notion",           "careers_url": "https://www.notion.so/careers",             "type": "Product",     "tags": ["Collaborative Tools","High Impact","SF/Remote"],      "salary_band": "₹30–60 LPA"},
            {"name": "Swiggy",           "careers_url": "https://careers.swiggy.com",                "type": "Startup",     "tags": ["India Scale","Consumer Tech","Bangalore"],             "salary_band": "₹22–40 LPA"},
        ],

        "Expert": [
            {"name": "Stripe",           "careers_url": "https://stripe.com/jobs",                   "type": "Product",     "tags": ["Payments Infra","Top Eng Culture","Remote"],           "salary_band": "₹55–110 LPA"},
            {"name": "GitHub",           "careers_url": "https://github.com/about/careers",          "type": "Product",     "tags": ["Dev Platform","Microsoft","All-Remote"],               "salary_band": "₹50–100 LPA"},
            {"name": "Figma",            "careers_url": "https://www.figma.com/careers",             "type": "Product",     "tags": ["Collaborative Design","Browser-First Eng","SF"],      "salary_band": "₹55–110 LPA"},
            {"name": "Linear",           "careers_url": "https://linear.app/careers",                "type": "Startup",     "tags": ["Dev Tools","Craft Culture","Remote-First"],             "salary_band": "₹50–100 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  ANDROID DEVELOPER / MOBILE
    # ══════════════════════════════════════════════════════
    "android_developer": {

        "Fresher": [
            {"name": "Infosys",          "careers_url": "https://www.infosys.com/careers",           "type": "Service",     "tags": ["Mobile Projects","Training","Pan India"],              "salary_band": "₹3.6–5 LPA"},
            {"name": "Wipro Digital",    "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["Mobile CoE","Kotlin/Java","Training"],                 "salary_band": "₹3.5–5 LPA"},
            {"name": "Cognizant",        "careers_url": "https://careers.cognizant.com",             "type": "Service",     "tags": ["Mobile Dev","US Clients","Chennai HQ"],                "salary_band": "₹4–6 LPA"},
            {"name": "Mindtree",         "careers_url": "https://www.mindtree.com/careers",          "type": "Service",     "tags": ["Mobile Solutions","Agile","Bangalore"],                "salary_band": "₹4–6 LPA"},
            {"name": "Zoho Mobile",      "careers_url": "https://www.zoho.com/careers",              "type": "Product",     "tags": ["Mobile Suite","Chennai","Strong Dev Culture"],         "salary_band": "₹4–8 LPA"},
            {"name": "ShareChat",        "careers_url": "https://sharechat.com/careers",             "type": "Startup",     "tags": ["Social Media","Kotlin","Bangalore"],                   "salary_band": "₹5–9 LPA"},
        ],

        "Entry Level": [
            {"name": "Paytm",            "careers_url": "https://paytm.com/careers",                 "type": "Startup",     "tags": ["Fintech","Super App","Noida"],                         "salary_band": "₹7–12 LPA"},
            {"name": "PhonePe",          "careers_url": "https://careers.phonepe.com",               "type": "Startup",     "tags": ["Payments","Kotlin","Bangalore"],                       "salary_band": "₹10–16 LPA"},
            {"name": "Dream11",          "careers_url": "https://www.dream11.com/careers",           "type": "Startup",     "tags": ["Fantasy Sports","High Scale","Mumbai"],                "salary_band": "₹8–14 LPA"},
            {"name": "MakeMyTrip",       "careers_url": "https://careers.makemytrip.com",            "type": "Product",     "tags": ["Travel Tech","Android Focus","Gurgaon"],              "salary_band": "₹7–12 LPA"},
            {"name": "Ola Electric",     "careers_url": "https://www.olaelectric.com/careers",       "type": "Startup",     "tags": ["EV Tech","Mobile App","Bangalore"],                    "salary_band": "₹8–13 LPA"},
            {"name": "Navi",             "careers_url": "https://navi.com/careers",                  "type": "Startup",     "tags": ["Fintech","Sachin Bansal","Bangalore"],                 "salary_band": "₹8–14 LPA"},
        ],

        "Intermediate": [
            {"name": "Swiggy",           "careers_url": "https://careers.swiggy.com",                "type": "Startup",     "tags": ["Consumer App","Bangalore","High Scale"],               "salary_band": "₹15–25 LPA"},
            {"name": "Zomato",           "careers_url": "https://www.zomato.com/careers",            "type": "Startup",     "tags": ["Food Delivery App","Gurgaon","Unicorn"],               "salary_band": "₹15–24 LPA"},
            {"name": "Flipkart Mobile",  "careers_url": "https://www.flipkartcareers.com",           "type": "Product",     "tags": ["E-Commerce App","Bangalore","India Scale"],            "salary_band": "₹16–26 LPA"},
            {"name": "Freshworks",       "careers_url": "https://www.freshworks.com/company/careers","type": "Product",     "tags": ["SaaS Mobile","Chennai","NYSE Listed"],                 "salary_band": "₹14–22 LPA"},
            {"name": "Clevertap",        "careers_url": "https://clevertap.com/careers",             "type": "Startup",     "tags": ["Mobile Engagement","SDK Dev","Mumbai/Remote"],         "salary_band": "₹14–22 LPA"},
            {"name": "InMobi",           "careers_url": "https://www.inmobi.com/company/careers",    "type": "Product",     "tags": ["Mobile Ads","SDK","Bangalore"],                        "salary_band": "₹12–20 LPA"},
        ],

        "Senior": [
            {"name": "Google Android",   "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","Android OS Team","Hyderabad"],                 "salary_band": "₹35–65 LPA"},
            {"name": "Microsoft",        "careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["Teams/Office Mobile","Hyderabad","Strong WLB"],        "salary_band": "₹30–55 LPA"},
            {"name": "Spotify",          "careers_url": "https://www.lifeatspotify.com/jobs",        "type": "Product",     "tags": ["Music Tech","Stockholm/Remote","Strong Culture"],      "salary_band": "₹35–65 LPA"},
            {"name": "Netflix Mobile",   "careers_url": "https://jobs.netflix.com",                  "type": "Product",     "tags": ["Streaming App","Freedom Culture","Top Pay"],           "salary_band": "₹40–80 LPA"},
            {"name": "Razorpay",         "careers_url": "https://razorpay.com/jobs",                 "type": "Startup",     "tags": ["Android SDK","Fintech","High Ownership"],              "salary_band": "₹25–40 LPA"},
        ],

        "Expert": [
            {"name": "Google Play",      "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["Android Ecosystem","FAANG","Platform Team"],           "salary_band": "₹55–100 LPA"},
            {"name": "Meta",             "careers_url": "https://www.metacareers.com",               "type": "Product",     "tags": ["Instagram/WhatsApp","FAANG","Top RSU"],                "salary_band": "₹50–100 LPA"},
            {"name": "Samsung R&D",      "careers_url": "https://www.samsungcareers.com",            "type": "MNC",         "tags": ["Android OEM","One UI","Bangalore/Seoul"],              "salary_band": "₹40–80 LPA"},
            {"name": "Uber",             "careers_url": "https://www.uber.com/in/en/careers",        "type": "Product",     "tags": ["Rider/Driver App","Bangalore","High Impact"],          "salary_band": "₹45–85 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  UI/UX DESIGNER
    # ══════════════════════════════════════════════════════
    "ui_ux_designer": {

        "Fresher": [
            {"name": "Wipro Design",     "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["Design Studio","UX Projects","Training"],              "salary_band": "₹3.5–5 LPA"},
            {"name": "Infosys Design",   "careers_url": "https://www.infosys.com/careers",           "type": "Service",     "tags": ["Design Thinking","Figma","Pan India"],                 "salary_band": "₹3.6–5 LPA"},
            {"name": "Publicis Sapient", "careers_url": "https://www.publicissapient.com/careers",   "type": "Consulting",  "tags": ["Digital Agency","UX Strategy","Gurgaon"],              "salary_band": "₹4–7 LPA"},
            {"name": "Lollypop Design",  "careers_url": "https://lollypop.design/jobs",              "type": "Agency",      "tags": ["UX Agency","Award Winning","Bangalore"],               "salary_band": "₹3.5–6 LPA"},
            {"name": "ThoughtWorks UX",  "careers_url": "https://www.thoughtworks.com/careers",      "type": "Consulting",  "tags": ["Agile UX","Global Clients","Research Culture"],        "salary_band": "₹4–7 LPA"},
            {"name": "Pepper Content",   "careers_url": "https://www.peppercontent.io/careers",      "type": "Startup",     "tags": ["Content Platform","UI Focus","Mumbai"],                "salary_band": "₹4–7 LPA"},
        ],

        "Entry Level": [
            {"name": "Razorpay Design",  "careers_url": "https://razorpay.com/jobs",                 "type": "Startup",     "tags": ["Fintech Design","Design Systems","Bangalore"],         "salary_band": "₹7–12 LPA"},
            {"name": "CRED Design",      "careers_url": "https://careers.cred.club",                 "type": "Startup",     "tags": ["Award-Winning Design","Premium UX","Bangalore"],       "salary_band": "₹8–14 LPA"},
            {"name": "Clevertap UX",     "careers_url": "https://clevertap.com/careers",             "type": "Startup",     "tags": ["Product Design","SaaS","Mumbai/Remote"],               "salary_band": "₹7–12 LPA"},
            {"name": "Meesho Design",    "careers_url": "https://meesho.io/jobs",                    "type": "Startup",     "tags": ["Social Commerce","Inclusive Design","Bangalore"],      "salary_band": "₹8–14 LPA"},
            {"name": "Zeta",             "careers_url": "https://www.zeta.tech/careers",             "type": "Startup",     "tags": ["Fintech","Design Forward","Mumbai"],                   "salary_band": "₹7–12 LPA"},
            {"name": "Ditto Insurance",  "careers_url": "https://joinditto.in/careers",             "type": "Startup",     "tags": ["Conversational UX","Zerodha Group","Bangalore"],       "salary_band": "₹7–11 LPA"},
        ],

        "Intermediate": [
            {"name": "Adobe",            "careers_url": "https://www.adobe.com/careers",             "type": "Product",     "tags": ["Design Tools Company","Noida/Bangalore","Industry Leader"],"salary_band": "₹15–28 LPA"},
            {"name": "Figma",            "careers_url": "https://www.figma.com/careers",             "type": "Product",     "tags": ["Design Platform","SF/Remote","Mission Aligned"],       "salary_band": "₹20–38 LPA"},
            {"name": "Swiggy Design",    "careers_url": "https://careers.swiggy.com",                "type": "Startup",     "tags": ["Consumer UX","Bangalore","Scale"],                     "salary_band": "₹14–22 LPA"},
            {"name": "Flipkart Design",  "careers_url": "https://www.flipkartcareers.com",           "type": "Product",     "tags": ["E-Commerce UX","India Scale","Bangalore"],             "salary_band": "₹14–24 LPA"},
            {"name": "MoEngage Design",  "careers_url": "https://www.moengage.com/about/careers",    "type": "Startup",     "tags": ["B2B SaaS UX","Unicorn","Remote OK"],                   "salary_band": "₹12–20 LPA"},
        ],

        "Senior": [
            {"name": "Google UX",        "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["Material Design","FAANG","Hyderabad"],                 "salary_band": "₹30–60 LPA"},
            {"name": "Microsoft Design", "careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["Fluent Design","Hyderabad","WLB"],                     "salary_band": "₹28–52 LPA"},
            {"name": "Airbnb Design",    "careers_url": "https://careers.airbnb.com",                "type": "Product",     "tags": ["Design-Driven Company","SF/Remote","Celan"],           "salary_band": "₹35–65 LPA"},
            {"name": "Zomato Design",    "careers_url": "https://www.zomato.com/careers",            "type": "Startup",     "tags": ["Consumer Design","Unicorn","Gurgaon"],                 "salary_band": "₹22–38 LPA"},
            {"name": "Atlassian Design", "careers_url": "https://www.atlassian.com/company/careers", "type": "Product",     "tags": ["B2B Design","Remote-First","Australia Co"],            "salary_band": "₹28–50 LPA"},
        ],

        "Expert": [
            {"name": "Apple HIG",        "careers_url": "https://www.apple.com/careers/in",          "type": "Product",     "tags": ["Human Interface Guidelines","Top Pay","High Bar"],     "salary_band": "₹50–100 LPA"},
            {"name": "Spotify Design",   "careers_url": "https://www.lifeatspotify.com/jobs",        "type": "Product",     "tags": ["Music+Design","Stockholm/Remote","Culture"],           "salary_band": "₹45–90 LPA"},
            {"name": "Linear Design",    "careers_url": "https://linear.app/careers",                "type": "Startup",     "tags": ["Craft Culture","Pixel Perfect","Remote-First"],        "salary_band": "₹50–100 LPA"},
            {"name": "Meta Design",      "careers_url": "https://www.metacareers.com",               "type": "Product",     "tags": ["AR/VR Design","FAANG","Metaverse"],                    "salary_band": "₹50–100 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  SOFTWARE ENGINEER
    # ══════════════════════════════════════════════════════
    "software_engineer": {

        "Fresher": [
            {"name": "TCS",              "careers_url": "https://www.tcs.com/careers",               "type": "Service",     "tags": ["Largest IT Co","Training","Pan India"],                "salary_band": "₹3.5–5 LPA"},
            {"name": "Infosys",          "careers_url": "https://www.infosys.com/careers",           "type": "Service",     "tags": ["InfyTQ","Onboarding","Pan India"],                     "salary_band": "₹3.6–5 LPA"},
            {"name": "Wipro",            "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["Training","Large Company","Pan India"],                "salary_band": "₹3.5–5 LPA"},
            {"name": "Zoho",             "careers_url": "https://www.zoho.com/careers",              "type": "Product",     "tags": ["Product Company","Chennai","Good Culture"],            "salary_band": "₹4–8 LPA"},
            {"name": "Freshworks",       "careers_url": "https://www.freshworks.com/company/careers","type": "Product",     "tags": ["SaaS","NYSE Listed","Chennai"],                        "salary_band": "₹5–9 LPA"},
            {"name": "Infosys Springboard","careers_url":"https://www.infosys.com/careers",          "type": "Service",     "tags": ["Free Learning","600+ Courses","Entry Bridge"],         "salary_band": "₹3.6–5 LPA"},
        ],

        "Entry Level": [
            {"name": "Amazon",           "careers_url": "https://www.amazon.jobs",                   "type": "Product",     "tags": ["FAANG","High Bar","SDE-I"],                            "salary_band": "₹12–22 LPA"},
            {"name": "Microsoft",        "careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["FAANG","Azure","WLB"],                                 "salary_band": "₹16–28 LPA"},
            {"name": "Zepto",            "careers_url": "https://www.zeptonow.com/careers",          "type": "Startup",     "tags": ["Quick Commerce","Fast Growth","Mumbai"],               "salary_band": "₹10–18 LPA"},
            {"name": "Jupiter Money",    "careers_url": "https://jupiter.money/careers",             "type": "Startup",     "tags": ["Neobank","Fintech","Bangalore"],                       "salary_band": "₹10–16 LPA"},
            {"name": "Hasura",           "careers_url": "https://hasura.io/careers",                 "type": "Startup",     "tags": ["Open Source","Remote-First","GraphQL"],                "salary_band": "₹10–18 LPA"},
            {"name": "Setu",             "careers_url": "https://setu.co/careers",                   "type": "Startup",     "tags": ["API Infra","PINE Labs Group","Bangalore"],             "salary_band": "₹10–16 LPA"},
        ],

        "Intermediate": [
            {"name": "Google",           "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","SWE L4/L5","Top Pay"],                         "salary_band": "₹25–50 LPA"},
            {"name": "Atlassian",        "careers_url": "https://www.atlassian.com/company/careers", "type": "Product",     "tags": ["Remote-First","Jira/Confluence","Strong Pay"],         "salary_band": "₹20–38 LPA"},
            {"name": "Stripe",           "careers_url": "https://stripe.com/jobs",                   "type": "Product",     "tags": ["Payments","Top Eng Culture","Remote"],                 "salary_band": "₹22–40 LPA"},
            {"name": "Groww",            "careers_url": "https://groww.in/open-positions",           "type": "Startup",     "tags": ["Fintech","Unicorn","Wealth-Tech"],                     "salary_band": "₹18–30 LPA"},
            {"name": "Meesho",           "careers_url": "https://meesho.io/jobs",                    "type": "Startup",     "tags": ["Social Commerce","Unicorn","India Scale"],             "salary_band": "₹16–26 LPA"},
            {"name": "Salesforce",       "careers_url": "https://www.salesforce.com/company/careers","type": "Product",     "tags": ["Ohana Culture","CRM Leader","Hyderabad"],              "salary_band": "₹18–32 LPA"},
        ],

        "Senior": [
            {"name": "Google",           "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","L5/L6","Top Total Comp"],                      "salary_band": "₹40–80 LPA"},
            {"name": "Meta",             "careers_url": "https://www.metacareers.com",               "type": "Product",     "tags": ["FAANG","RSU","E5/E6"],                                 "salary_band": "₹45–90 LPA"},
            {"name": "Netflix",          "careers_url": "https://jobs.netflix.com",                  "type": "Product",     "tags": ["Senior SWE","Freedom Culture","Top Pay"],              "salary_band": "₹50–100 LPA"},
            {"name": "Coinbase",         "careers_url": "https://www.coinbase.com/careers",          "type": "Product",     "tags": ["Crypto","Remote-First","High Pay"],                    "salary_band": "₹35–70 LPA"},
            {"name": "Uber",             "careers_url": "https://www.uber.com/in/en/careers",        "type": "Product",     "tags": ["Mobility","Bangalore CoE","High Impact"],              "salary_band": "₹30–60 LPA"},
            {"name": "Walmart Labs",     "careers_url": "https://careers.walmart.com",               "type": "Product",     "tags": ["Retail Tech","Bangalore","Scale"],                     "salary_band": "₹28–52 LPA"},
        ],

        "Expert": [
            {"name": "Google",           "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","L7+ Staff","Highest Comp"],                    "salary_band": "₹70–160 LPA"},
            {"name": "Apple",            "careers_url": "https://www.apple.com/careers/in",          "type": "Product",     "tags": ["Premium Brand","Staff Eng","RSU"],                     "salary_band": "₹65–140 LPA"},
            {"name": "Stripe",           "careers_url": "https://stripe.com/jobs",                   "type": "Product",     "tags": ["Staff Eng","Payments Infra","Remote"],                 "salary_band": "₹70–150 LPA"},
            {"name": "Cloudflare",       "careers_url": "https://www.cloudflare.com/careers",        "type": "Product",     "tags": ["Internet Infra","Principal Eng","Remote-OK"],          "salary_band": "₹65–130 LPA"},
            {"name": "Databricks",       "careers_url": "https://www.databricks.com/company/careers","type": "Product",     "tags": ["Pre-IPO","Staff Eng","Data+AI"],                       "salary_band": "₹70–150 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  BI ANALYST
    # ══════════════════════════════════════════════════════
    "bi_analyst": {

        "Fresher": [
            {"name": "Mu Sigma",         "careers_url": "https://www.mu-sigma.com/careers",          "type": "Analytics",   "tags": ["Decision Science","BI Tools","Bangalore"],             "salary_band": "₹3–5 LPA"},
            {"name": "EXL Service",      "careers_url": "https://www.exlservice.com/careers",        "type": "Consulting",  "tags": ["Analytics BPO","Tableau/PowerBI","Delhi"],             "salary_band": "₹3.5–6 LPA"},
            {"name": "Accenture",        "careers_url": "https://www.accenture.com/in-en/careers",   "type": "MNC",         "tags": ["BI CoE","Global Clients","Diverse Domains"],           "salary_band": "₹4–7 LPA"},
            {"name": "Capgemini",        "careers_url": "https://www.capgemini.com/in-en/careers",   "type": "MNC",         "tags": ["BI Practice","Power BI","Hybrid Work"],                "salary_band": "₹4–6 LPA"},
            {"name": "MicroStrategy",    "careers_url": "https://www.microstrategy.com/en/careers",  "type": "Product",     "tags": ["BI Platform","Product Company","Bangalore"],           "salary_band": "₹4–7 LPA"},
            {"name": "Genpact",          "careers_url": "https://www.genpact.com/careers",           "type": "Consulting",  "tags": ["Analytics","Tableau","Global Scale"],                  "salary_band": "₹3.5–6 LPA"},
        ],

        "Entry Level": [
            {"name": "Nielsen IQ",       "careers_url": "https://www.nielseniq.com/global/en/careers","type": "MNC",        "tags": ["Consumer Data","FMCG","Market Research"],              "salary_band": "₹5–9 LPA"},
            {"name": "Dunnhumby",        "careers_url": "https://www.dunnhumby.com/careers",         "type": "Analytics",   "tags": ["Retail Analytics","Tesco Group","Mumbai"],             "salary_band": "₹5–9 LPA"},
            {"name": "Kantar",           "careers_url": "https://www.kantar.com/careers",             "type": "MNC",        "tags": ["Market Research","FMCG BI","Mumbai/Delhi"],            "salary_band": "₹5–8 LPA"},
            {"name": "HDFC Bank Analytics","careers_url":"https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/?folderName=/footer/Careers","type": "BFSI","tags": ["Banking BI","Tableau/SQL","Mumbai"],"salary_band": "₹5–9 LPA"},
            {"name": "Cognizant BI",     "careers_url": "https://careers.cognizant.com",             "type": "Service",     "tags": ["BI Services","US Clients","Pan India"],                "salary_band": "₹5–8 LPA"},
            {"name": "Mindtree BI",      "careers_url": "https://www.mindtree.com/careers",          "type": "Service",     "tags": ["Business Intelligence","Agile","Bangalore"],           "salary_band": "₹5–8 LPA"},
        ],

        "Intermediate": [
            {"name": "Microsoft Power BI","careers_url":"https://careers.microsoft.com",             "type": "Product",     "tags": ["Product Team","Power BI","Hyderabad"],                 "salary_band": "₹15–25 LPA"},
            {"name": "Tableau / Salesforce","careers_url":"https://www.salesforce.com/company/careers","type":"Product",    "tags": ["Viz Platform","CRM Data","Hyderabad"],                 "salary_band": "₹14–24 LPA"},
            {"name": "Amazon QuickSight","careers_url": "https://www.amazon.jobs",                   "type": "Product",     "tags": ["AWS BI","FAANG","Cloud BI"],                           "salary_band": "₹18–30 LPA"},
            {"name": "Deloitte Analytics","careers_url":"https://www2.deloitte.com/in/en/careers",   "type": "Consulting",  "tags": ["Big 4","BI Strategy","Enterprise"],                    "salary_band": "₹10–18 LPA"},
            {"name": "KPMG Data & Analytics","careers_url":"https://home.kpmg/in/en/home/careers",  "type": "Consulting",  "tags": ["Big 4","Risk BI","Cross-Industry"],                    "salary_band": "₹10–17 LPA"},
            {"name": "Flipkart BI",      "careers_url": "https://www.flipkartcareers.com",           "type": "Product",     "tags": ["E-Commerce Data","Bangalore","India Scale"],           "salary_band": "₹14–22 LPA"},
        ],

        "Senior": [
            {"name": "Google",           "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","Looker Platform","Top Comp"],                  "salary_band": "₹30–55 LPA"},
            {"name": "McKinsey Analytics","careers_url":"https://www.mckinsey.com/careers",          "type": "Consulting",  "tags": ["Strategy","Analytics","Prestige"],                     "salary_band": "₹25–50 LPA"},
            {"name": "Walmart",          "careers_url": "https://careers.walmart.com",               "type": "Product",     "tags": ["Retail BI","Petabyte Scale","Bangalore"],              "salary_band": "₹22–40 LPA"},
            {"name": "Target India",     "careers_url": "https://india.target.com/careers",          "type": "Product",     "tags": ["Retail Analytics","Bangalore","US Retail"],            "salary_band": "₹20–38 LPA"},
            {"name": "Goldman Sachs",    "careers_url": "https://www.goldmansachs.com/careers",      "type": "MNC",         "tags": ["Finance BI","Bangalore","High Pay"],                   "salary_band": "₹25–45 LPA"},
        ],

        "Expert": [
            {"name": "Looker (Google)",  "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["BI Platform","Google Cloud","Remote"],                 "salary_band": "₹45–90 LPA"},
            {"name": "ThoughtSpot",      "careers_url": "https://www.thoughtspot.com/careers",       "type": "Product",     "tags": ["Search Analytics","AI-BI","Sunnyvale/Remote"],        "salary_band": "₹40–80 LPA"},
            {"name": "Sigma Computing",  "careers_url": "https://www.sigmacomputing.com/company/careers","type": "Startup", "tags": ["Cloud BI","Pre-IPO","SF/Remote"],                     "salary_band": "₹45–90 LPA"},
            {"name": "Palantir",         "careers_url": "https://www.palantir.com/careers",          "type": "Product",     "tags": ["Foundry Platform","Enterprise BI","Mission"],         "salary_band": "₹40–80 LPA"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  SQL DEVELOPER
    # ══════════════════════════════════════════════════════
    "sql_developer": {

        "Fresher": [
            {"name": "TCS",              "careers_url": "https://www.tcs.com/careers",               "type": "Service",     "tags": ["SQL Training","Large Scale","Pan India"],              "salary_band": "₹3.5–5 LPA"},
            {"name": "Wipro",            "careers_url": "https://careers.wipro.com",                 "type": "Service",     "tags": ["DBA Projects","Training","Pan India"],                 "salary_band": "₹3.5–5 LPA"},
            {"name": "Cognizant",        "careers_url": "https://careers.cognizant.com",             "type": "Service",     "tags": ["Database Projects","US Clients","Pan India"],          "salary_band": "₹4–6 LPA"},
            {"name": "Mphasis",          "careers_url": "https://careers.mphasis.com",               "type": "Service",     "tags": ["BFSI","SQL Focus","Bangalore"],                        "salary_band": "₹3.5–5.5 LPA"},
            {"name": "Hexaware",         "careers_url": "https://www.hexaware.com/careers",          "type": "Service",     "tags": ["Data Migration","SQL Server","Mumbai"],                "salary_band": "₹4–6 LPA"},
            {"name": "Mastech Digital",  "careers_url": "https://www.mastechdigital.com/careers",    "type": "Service",     "tags": ["IT Staffing","SQL Roles","Pan India"],                 "salary_band": "₹3.5–5.5 LPA"},
        ],

        "Entry Level": [
            {"name": "Oracle India",     "careers_url": "https://www.oracle.com/in/corporate/careers","type": "Product",    "tags": ["DB Giant","SQL/PLSQL","Hyderabad/Bangalore"],          "salary_band": "₹6–10 LPA"},
            {"name": "Microsoft",        "careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["SQL Server Team","Hyderabad","Strong WLB"],            "salary_band": "₹10–18 LPA"},
            {"name": "SAP",              "careers_url": "https://www.sap.com/india/about/careers",   "type": "Product",     "tags": ["SAP HANA","ERP Data","Bangalore/Gurgaon"],             "salary_band": "₹6–11 LPA"},
            {"name": "Genpact",          "careers_url": "https://www.genpact.com/careers",           "type": "Consulting",  "tags": ["SQL Reporting","Analytics BPO","Delhi/Hyderabad"],    "salary_band": "₹5–9 LPA"},
            {"name": "NIIT Technologies","careers_url": "https://www.coforge.com/careers",           "type": "Service",     "tags": ["Data Migration","SQL Focus","Noida"],                  "salary_band": "₹5–8 LPA"},
            {"name": "Accenture",        "careers_url": "https://www.accenture.com/in-en/careers",   "type": "MNC",         "tags": ["Global MNC","SQL + ETL","Diverse Projects"],           "salary_band": "₹5–9 LPA"},
        ],

        "Intermediate": [
            {"name": "Amazon Redshift",  "careers_url": "https://www.amazon.jobs",                   "type": "Product",     "tags": ["AWS DB Team","FAANG","SQL at Scale"],                  "salary_band": "₹16–28 LPA"},
            {"name": "Snowflake",        "careers_url": "https://careers.snowflake.com",             "type": "Product",     "tags": ["Cloud DW","SQL Expertise","Remote OK"],                "salary_band": "₹16–28 LPA"},
            {"name": "Thoughtworks",     "careers_url": "https://www.thoughtworks.com/careers",      "type": "Consulting",  "tags": ["Data Engineering","Agile","Global Clients"],           "salary_band": "₹12–20 LPA"},
            {"name": "Flipkart",         "careers_url": "https://www.flipkartcareers.com",           "type": "Product",     "tags": ["E-Commerce DB","India Scale","Bangalore"],             "salary_band": "₹14–22 LPA"},
            {"name": "HDFC Bank",        "careers_url": "https://www.hdfcbank.com/content/bbp/repositories/723fb80a-2dde-42a3-9793-7ae1be57c87f/?folderName=/footer/Careers","type": "BFSI","tags": ["Banking SQL","Core Banking","Mumbai"],"salary_band": "₹10–18 LPA"},
            {"name": "Deloitte",         "careers_url": "https://www2.deloitte.com/in/en/careers",   "type": "Consulting",  "tags": ["Big 4","Data Warehousing","Enterprise SQL"],           "salary_band": "₹10–18 LPA"},
        ],

        "Senior": [
            {"name": "Google BigQuery",  "careers_url": "https://careers.google.com",                "type": "Product",     "tags": ["FAANG","SQL at Petabyte","Top Pay"],                   "salary_band": "₹30–58 LPA"},
            {"name": "Microsoft SQL Svr","careers_url": "https://careers.microsoft.com",             "type": "Product",     "tags": ["SQL Server Team","Senior DBA","Hyderabad"],            "salary_band": "₹28–50 LPA"},
            {"name": "Palantir",         "careers_url": "https://www.palantir.com/careers",          "type": "Product",     "tags": ["Enterprise Data","Foundry","Mission"],                 "salary_band": "₹30–55 LPA"},
            {"name": "Walmart Labs",     "careers_url": "https://careers.walmart.com",               "type": "Product",     "tags": ["Retail SQL","Hive/Presto","Bangalore"],                "salary_band": "₹22–40 LPA"},
            {"name": "Goldman Sachs",    "careers_url": "https://www.goldmansachs.com/careers",      "type": "MNC",         "tags": ["Finance DB","Bangalore","High Comp"],                  "salary_band": "₹25–45 LPA"},
        ],

        "Expert": [
            {"name": "Oracle Cloud DB",  "careers_url": "https://www.oracle.com/in/corporate/careers","type": "Product",   "tags": ["DB Pioneer","Autonomous DB","Hyderabad"],              "salary_band": "₹45–90 LPA"},
            {"name": "CockroachDB",      "careers_url": "https://www.cockroachlabs.com/careers",     "type": "Startup",     "tags": ["Distributed SQL","Cloud Native","Remote"],             "salary_band": "₹50–100 LPA"},
            {"name": "PlanetScale",      "careers_url": "https://planetscale.com/careers",           "type": "Startup",     "tags": ["MySQL at Scale","Vitess","Remote-First"],              "salary_band": "₹45–95 LPA"},
            {"name": "Neon",             "careers_url": "https://neon.tech/careers",                  "type": "Startup",     "tags": ["Serverless Postgres","Remote","Series B"],             "salary_band": "₹45–90 LPA"},
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def normalise_role(raw_role: str) -> str:
    """Map the analyzer's job_role string to a COMPANIES key."""
    r = raw_role.strip().lower()
    # Direct alias lookup
    if r in ROLE_ALIASES:
        return ROLE_ALIASES[r]
    # Partial match fallback
    for alias, key in ROLE_ALIASES.items():
        if alias in r or r in alias:
            return key
    return "software_engineer"   # safe default


def normalise_level(raw_level: str) -> str:
    """Map the analyzer's experience_level string to a COMPANIES level key."""
    mapping = {
        "fresher":      "Fresher",
        "entry level":  "Entry Level",
        "entry":        "Entry Level",
        "intermediate": "Intermediate",
        "mid":          "Intermediate",
        "mid-level":    "Intermediate",
        "senior":       "Senior",
        "expert":       "Expert",
        "lead":         "Expert",
        "principal":    "Expert",
    }
    return mapping.get(raw_level.strip().lower(), "Entry Level")


def get_suggestions(job_role: str, experience_level: str,
                    total_years: float = 0, limit: int = 6) -> dict:
    """
    Return company suggestions for the given role + level.
    Falls back gracefully if exact level not found.
    """
    role_key  = normalise_role(job_role)
    level_key = normalise_level(experience_level)

    role_data = COMPANIES.get(role_key, COMPANIES["software_engineer"])

    # Primary level — fallback order
    level_order = ["Fresher", "Entry Level", "Intermediate", "Senior", "Expert"]
    companies   = role_data.get(level_key, [])

    if not companies:
        # Walk to nearest non-empty level
        idx = level_order.index(level_key) if level_key in level_order else 1
        for offset in [1, -1, 2, -2]:
            fallback = level_order[idx + offset] if 0 <= idx + offset < len(level_order) else None
            if fallback and role_data.get(fallback):
                companies = role_data[fallback]
                level_key = fallback
                break

    return {
        "role_key":   role_key,
        "level_key":  level_key,
        "companies":  companies[:limit],
        "total_found": len(companies),
    }