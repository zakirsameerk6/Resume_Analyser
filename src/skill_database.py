"""
Comprehensive Skill Taxonomy and Learning Resource Mapping.
Contains categories, canonical names, regex patterns, aliases,
and curated learning resources for automatic gap recommendation.
"""

from typing import Dict, List, Any

# Map category names to list of skills
SKILL_TAXONOMY: Dict[str, Dict[str, Any]] = {
    # ----------------- Programming Languages -----------------
    "Python": {
        "category": "Programming Languages",
        "aliases": [r"\bpython\b", r"\bpython3\b"],
        "resource": {
            "title": "Python Official Documentation & Tutorials",
            "url": "https://docs.python.org/3/tutorial/",
            "platform": "Python.org",
            "type": "Documentation & Hands-on",
            "estimated_time": "2-3 weeks"
        }
    },
    "SQL": {
        "category": "Programming Languages",
        "aliases": [r"\bsql\b", r"\bstructured query language\b", r"\bt-sql\b", r"\bpl/sql\b"],
        "resource": {
            "title": "SQL Tutorial - Mode Analytics & W3Schools",
            "url": "https://mode.com/sql-tutorial/",
            "platform": "Mode Analytics",
            "type": "Interactive Course",
            "estimated_time": "1-2 weeks"
        }
    },
    "JavaScript": {
        "category": "Programming Languages",
        "aliases": [r"\bjavascript\b", r"\bjs\b", r"\bes6\b"],
        "resource": {
            "title": "The Modern JavaScript Tutorial",
            "url": "https://javascript.info/",
            "platform": "javascript.info",
            "type": "Interactive Guide",
            "estimated_time": "3-4 weeks"
        }
    },
    "TypeScript": {
        "category": "Programming Languages",
        "aliases": [r"\btypescript\b", r"\bts\b"],
        "resource": {
            "title": "TypeScript Handbook",
            "url": "https://www.typescriptlang.org/docs/handbook/intro.html",
            "platform": "TypeScript Official",
            "type": "Handbook & Documentation",
            "estimated_time": "1-2 weeks"
        }
    },
    "Java": {
        "category": "Programming Languages",
        "aliases": [r"\bjava\b(?!script)"],
        "resource": {
            "title": "Java Programming & Concepts",
            "url": "https://dev.java/learn/",
            "platform": "Oracle Java Tutorials",
            "type": "Official Tutorial",
            "estimated_time": "4 weeks"
        }
    },
    "C++": {
        "category": "Programming Languages",
        "aliases": [r"\bc\+\+\b", r"\bcpp\b"],
        "resource": {
            "title": "C++ Language Reference & LearnCpp",
            "url": "https://www.learncpp.com/",
            "platform": "LearnCpp.com",
            "type": "Comprehensive Guide",
            "estimated_time": "4-6 weeks"
        }
    },
    "C#": {
        "category": "Programming Languages",
        "aliases": [r"\bc#\b", r"\bcsharp\b", r"\bc-sharp\b"],
        "resource": {
            "title": "C# Documentation & Learning Path",
            "url": "https://learn.microsoft.com/en-us/dotnet/csharp/",
            "platform": "Microsoft Learn",
            "type": "Official Documentation",
            "estimated_time": "3 weeks"
        }
    },
    "R": {
        "category": "Programming Languages",
        "aliases": [r"\br\s+programming\b", r"\br\s+language\b", r"\bbase\s+r\b"],
        "resource": {
            "title": "R for Data Science (Hadley Wickham)",
            "url": "https://r4ds.had.co.nz/",
            "platform": "Online Book",
            "type": "Interactive Book",
            "estimated_time": "3 weeks"
        }
    },
    "Go": {
        "category": "Programming Languages",
        "aliases": [r"\bgolang\b", r"\bgo\s+language\b"],
        "resource": {
            "title": "A Tour of Go",
            "url": "https://go.dev/tour/welcome/1",
            "platform": "Go.dev",
            "type": "Interactive Tour",
            "estimated_time": "1-2 weeks"
        }
    },
    "Rust": {
        "category": "Programming Languages",
        "aliases": [r"\brust\b", r"\brust-lang\b"],
        "resource": {
            "title": "The Rust Programming Language Book",
            "url": "https://doc.rust-lang.org/book/",
            "platform": "Rust Official",
            "type": "Online Book",
            "estimated_time": "4 weeks"
        }
    },
    "PHP": {
        "category": "Programming Languages",
        "aliases": [r"\bphp\b"],
        "resource": {
            "title": "PHP The Right Way",
            "url": "https://phptherightway.com/",
            "platform": "Community Guide",
            "type": "Best Practices Guide",
            "estimated_time": "2 weeks"
        }
    },
    "Bash/Shell": {
        "category": "Programming Languages",
        "aliases": [r"\bbash\b", r"\bshell\s+scripting\b", r"\bpowershell\b", r"\bzsh\b"],
        "resource": {
            "title": "Bash Scripting Guide for Beginners",
            "url": "https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/",
            "platform": "freeCodeCamp",
            "type": "Guide & Tutorial",
            "estimated_time": "1 week"
        }
    },

    # ----------------- Business Intelligence & Data Analysis -----------------
    "Power BI": {
        "category": "BI & Analytics",
        "aliases": [r"\bpower\s*bi\b", r"\bpowerbi\b", r"\bdax\b", r"\bpower\s+query\b"],
        "resource": {
            "title": "Microsoft Power BI Guided Learning",
            "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi",
            "platform": "Microsoft Learn",
            "type": "Hands-on Learning Path",
            "estimated_time": "2 weeks"
        }
    },
    "Tableau": {
        "category": "BI & Analytics",
        "aliases": [r"\btableau\b", r"\btableau\s+desktop\b", r"\btableau\s+server\b"],
        "resource": {
            "title": "Tableau Free Training Videos & Documentation",
            "url": "https://www.tableau.com/learn/training",
            "platform": "Tableau Official",
            "type": "Video Series & Docs",
            "estimated_time": "2 weeks"
        }
    },
    "Excel": {
        "category": "BI & Analytics",
        "aliases": [r"\bexcel\b", r"\badvanced\s+excel\b", r"\bvba\b", r"\bpivot\s+tables?\b", r"\bvlookup\b", r"\bxlookup\b"],
        "resource": {
            "title": "Excel for Data Analysis",
            "url": "https://support.microsoft.com/en-us/excel",
            "platform": "Microsoft Support & freeCodeCamp",
            "type": "Tutorial & Formulas Guide",
            "estimated_time": "1 week"
        }
    },
    "Looker": {
        "category": "BI & Analytics",
        "aliases": [r"\blooker\b", r"\blookml\b", r"\blooker\s+studio\b", r"\bgoogle\s+data\s+studio\b"],
        "resource": {
            "title": "Google Cloud Looker Tutorials & Guides",
            "url": "https://cloud.google.com/looker/docs",
            "platform": "Google Cloud",
            "type": "Official Documentation",
            "estimated_time": "1-2 weeks"
        }
    },
    "Data Analysis": {
        "category": "BI & Analytics",
        "aliases": [r"\bdata\s+analysis\b", r"\bexploratory\s+data\s+analysis\b", r"\beda\b", r"\bdata\s+analytics\b"],
        "resource": {
            "title": "Exploratory Data Analysis with Python",
            "url": "https://www.kaggle.com/learn/data-cleaning",
            "platform": "Kaggle Learn",
            "type": "Interactive Exercises",
            "estimated_time": "1-2 weeks"
        }
    },
    "Data Visualization": {
        "category": "BI & Analytics",
        "aliases": [r"\bdata\s+visualization\b", r"\bdataviz\b", r"\bmatplotlib\b", r"\bseaborn\b", r"\bplotly\b"],
        "resource": {
            "title": "Data Visualization with Python (Plotly & Seaborn)",
            "url": "https://www.kaggle.com/learn/data-visualization",
            "platform": "Kaggle Learn",
            "type": "Interactive Course",
            "estimated_time": "1 week"
        }
    },
    "Statistics": {
        "category": "BI & Analytics",
        "aliases": [r"\bstatistics\b", r"\bstatistical\s+analysis\b", r"\bhypothesis\s+testing\b", r"\ba/b\s+testing\b"],
        "resource": {
            "title": "Practical Statistics for Data Scientists",
            "url": "https://www.statlearning.com/",
            "platform": "An Introduction to Statistical Learning",
            "type": "Comprehensive Text & Lab",
            "estimated_time": "3 weeks"
        }
    },

    # ----------------- Machine Learning & Data Science -----------------
    "Machine Learning": {
        "category": "Machine Learning & AI",
        "aliases": [r"\bmachine\s+learning\b", r"\bml\b", r"\bsupervised\s+learning\b", r"\bunsupervised\s+learning\b"],
        "resource": {
            "title": "Machine Learning Specialization by Andrew Ng",
            "url": "https://www.coursera.org/specializations/machine-learning-introduction",
            "platform": "Coursera / DeepLearning.AI",
            "type": "Foundational Course",
            "estimated_time": "4-6 weeks"
        }
    },
    "Deep Learning": {
        "category": "Machine Learning & AI",
        "aliases": [r"\bdeep\s+learning\b", r"\bneural\s+networks?\b", r"\bann\b", r"\bcnn\b", r"\brnn\b", r"\blstm\b"],
        "resource": {
            "title": "Deep Learning Specialization",
            "url": "https://www.deeplearning.ai/courses/deep-learning-specialization/",
            "platform": "DeepLearning.AI",
            "type": "Deep Dive Course",
            "estimated_time": "6 weeks"
        }
    },
    "Natural Language Processing (NLP)": {
        "category": "Machine Learning & AI",
        "aliases": [r"\bnlp\b", r"\bnatural\s+language\s+processing\b", r"\btext\s+mining\b", r"\bword2vec\b", r"\bbert\b"],
        "resource": {
            "title": "Hugging Face NLP Course",
            "url": "https://huggingface.co/learn/nlp-course/",
            "platform": "Hugging Face",
            "type": "Hands-on Practical Course",
            "estimated_time": "3 weeks"
        }
    },
    "Large Language Models (LLMs)": {
        "category": "Machine Learning & AI",
        "aliases": [r"\bllms?\b", r"\blarge\s+language\s+models?\b", r"\bgenerative\s+ai\b", r"\bgenai\b", r"\brag\b", r"\blangchain\b", r"\bllamaindex\b"],
        "resource": {
            "title": "Generative AI & LLM Systems",
            "url": "https://www.deeplearning.ai/short-courses/",
            "platform": "DeepLearning.AI Short Courses",
            "type": "Practical Short Courses",
            "estimated_time": "2 weeks"
        }
    },
    "Computer Vision": {
        "category": "Machine Learning & AI",
        "aliases": [r"\bcomputer\s+vision\b", r"\bopencv\b", r"\byolo\b", r"\bobject\s+detection\b", r"\bimage\s+segmentation\b"],
        "resource": {
            "title": "OpenCV Course & Computer Vision Guide",
            "url": "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html",
            "platform": "OpenCV Official",
            "type": "Hands-on Tutorials",
            "estimated_time": "3 weeks"
        }
    },
    "Pandas": {
        "category": "Data Science Libraries",
        "aliases": [r"\bpandas\b"],
        "resource": {
            "title": "Pandas Documentation & User Guide",
            "url": "https://pandas.pydata.org/docs/user_guide/index.html",
            "platform": "Pandas PyData",
            "type": "Official User Guide",
            "estimated_time": "1-2 weeks"
        }
    },
    "NumPy": {
        "category": "Data Science Libraries",
        "aliases": [r"\bnumpy\b"],
        "resource": {
            "title": "NumPy Absolute Basics for Beginners",
            "url": "https://numpy.org/doc/stable/user/absolute_beginners.html",
            "platform": "NumPy.org",
            "type": "Official Tutorial",
            "estimated_time": "1 week"
        }
    },
    "Scikit-learn": {
        "category": "Data Science Libraries",
        "aliases": [r"\bscikit-learn\b", r"\bsklearn\b", r"\bscikitlearn\b"],
        "resource": {
            "title": "Scikit-learn User Guide & Examples",
            "url": "https://scikit-learn.org/stable/user_guide.html",
            "platform": "Scikit-Learn Official",
            "type": "User Guide & Code Examples",
            "estimated_time": "2 weeks"
        }
    },
    "TensorFlow": {
        "category": "Data Science Libraries",
        "aliases": [r"\btensorflow\b", r"\btf\b", r"\bkeras\b"],
        "resource": {
            "title": "TensorFlow Core Tutorials",
            "url": "https://www.tensorflow.org/tutorials",
            "platform": "TensorFlow.org",
            "type": "Tutorials & Code Demos",
            "estimated_time": "3 weeks"
        }
    },
    "PyTorch": {
        "category": "Data Science Libraries",
        "aliases": [r"\bpytorch\b", r"\btorch\b"],
        "resource": {
            "title": "Deep Learning with PyTorch: A 60 Minute Blitz",
            "url": "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
            "platform": "PyTorch Official",
            "type": "Interactive Tutorial",
            "estimated_time": "2-3 weeks"
        }
    },
    "spaCy": {
        "category": "Data Science Libraries",
        "aliases": [r"\bspacy\b"],
        "resource": {
            "title": "Advanced NLP with spaCy (Ines Montani)",
            "url": "https://course.spacy.io/",
            "platform": "spaCy.io",
            "type": "Free Interactive Course",
            "estimated_time": "1 week"
        }
    },

    # ----------------- Databases & Data Engineering -----------------
    "PostgreSQL": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bpostgresql\b", r"\bpostgres\b"],
        "resource": {
            "title": "PostgreSQL Tutorial for Developers",
            "url": "https://www.postgresqltutorial.com/",
            "platform": "PostgreSQLTutorial",
            "type": "Practical Step-by-Step",
            "estimated_time": "1-2 weeks"
        }
    },
    "MySQL": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bmysql\b"],
        "resource": {
            "title": "MySQL Tutorial & Reference",
            "url": "https://www.mysqltutorial.org/",
            "platform": "MySQLTutorial",
            "type": "Reference & Hands-on",
            "estimated_time": "1 week"
        }
    },
    "MongoDB": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bmongodb\b", r"\bmongo\b", r"\bnosql\b"],
        "resource": {
            "title": "MongoDB University Courses",
            "url": "https://learn.mongodb.com/",
            "platform": "MongoDB University",
            "type": "Free Official Course",
            "estimated_time": "1-2 weeks"
        }
    },
    "Redis": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bredis\b"],
        "resource": {
            "title": "Redis University",
            "url": "https://university.redis.com/",
            "platform": "Redis University",
            "type": "Free Official Courses",
            "estimated_time": "1 week"
        }
    },
    "Apache Spark": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bapache\s+spark\b", r"\bspark\b", r"\bpyspark\b"],
        "resource": {
            "title": "Spark Programming Guide & PySpark Tutorial",
            "url": "https://spark.apache.org/docs/latest/rdd-programming-guide.html",
            "platform": "Apache Spark Official",
            "type": "Documentation & Hands-on",
            "estimated_time": "2-3 weeks"
        }
    },
    "Apache Kafka": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bkafka\b", r"\bapache\s+kafka\b"],
        "resource": {
            "title": "Confluent Kafka Developer Course",
            "url": "https://developer.confluent.io/learn-kafka/",
            "platform": "Confluent Developer",
            "type": "Free Video Course & Demos",
            "estimated_time": "2 weeks"
        }
    },
    "Snowflake": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\bsnowflake\b", r"\bsnowflake\s+db\b"],
        "resource": {
            "title": "Snowflake Hands-on Essentials",
            "url": "https://learn.snowflake.com/",
            "platform": "Snowflake Learn",
            "type": "Hands-on Workshop",
            "estimated_time": "1-2 weeks"
        }
    },
    "ETL / Data Pipelines": {
        "category": "Databases & Data Engineering",
        "aliases": [r"\betl\b", r"\belt\b", r"\bdata\s+pipelines?\b", r"\bdata\s+warehousing\b", r"\bairflow\b", r"\bdbt\b"],
        "resource": {
            "title": "Data Engineering Zoomcamp",
            "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp",
            "platform": "DataTalks.Club",
            "type": "Free Comprehensive Bootcamp",
            "estimated_time": "4-6 weeks"
        }
    },

    # ----------------- Web Frontend & Backend -----------------
    "React": {
        "category": "Web Development",
        "aliases": [r"\breact\b", r"\breact\.?js\b", r"\breactjs\b"],
        "resource": {
            "title": "React Official Documentation & Interactive Quick Start",
            "url": "https://react.dev/learn",
            "platform": "React.dev",
            "type": "Official Interactive Tutorial",
            "estimated_time": "2-3 weeks"
        }
    },
    "Node.js": {
        "category": "Web Development",
        "aliases": [r"\bnode\b", r"\bnode\.?js\b", r"\bnodejs\b"],
        "resource": {
            "title": "Node.js Guide & Documentation",
            "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs",
            "platform": "Nodejs.org",
            "type": "Official Guide",
            "estimated_time": "2 weeks"
        }
    },
    "Django": {
        "category": "Web Development",
        "aliases": [r"\bdjango\b", r"\bdjango\s+rest\s+framework\b", r"\bdrf\b"],
        "resource": {
            "title": "Django Getting Started Tutorial",
            "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
            "platform": "Django Official",
            "type": "Official Tutorial",
            "estimated_time": "2 weeks"
        }
    },
    "Flask": {
        "category": "Web Development",
        "aliases": [r"\bflask\b"],
        "resource": {
            "title": "The Flask Mega-Tutorial by Miguel Grinberg",
            "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
            "platform": "Miguel Grinberg Blog",
            "type": "Step-by-step Tutorial",
            "estimated_time": "1-2 weeks"
        }
    },
    "FastAPI": {
        "category": "Web Development",
        "aliases": [r"\bfastapi\b"],
        "resource": {
            "title": "FastAPI Tutorial - User Guide",
            "url": "https://fastapi.tiangolo.com/tutorial/",
            "platform": "tiangolo.com",
            "type": "Interactive Documentation",
            "estimated_time": "1 week"
        }
    },
    "HTML/CSS": {
        "category": "Web Development",
        "aliases": [r"\bhtml5?\b", r"\bcss3?\b", r"\btailwind\b", r"\bbootstrap\b", r"\bsass\b"],
        "resource": {
            "title": "MDN Web Docs: Learn Web Development",
            "url": "https://developer.mozilla.org/en-US/docs/Learn",
            "platform": "Mozilla Developer Network",
            "type": "Comprehensive Guides",
            "estimated_time": "2 weeks"
        }
    },
    "RESTful APIs": {
        "category": "Web Development",
        "aliases": [r"\brest\b", r"\brestful\b", r"\brest\s+apis?\b", r"\bapi\s+design\b", r"\bgraphql\b"],
        "resource": {
            "title": "REST API Design Best Practices",
            "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design",
            "platform": "Microsoft Architecture Guide",
            "type": "Architectural Guide",
            "estimated_time": "1 week"
        }
    },
    "Next.js": {
        "category": "Web Development",
        "aliases": [r"\bnext\.?js\b", r"\bnextjs\b"],
        "resource": {
            "title": "Next.js Learn Course",
            "url": "https://nextjs.org/learn",
            "platform": "Next.js / Vercel",
            "type": "Interactive Course",
            "estimated_time": "1-2 weeks"
        }
    },

    # ----------------- Cloud & DevOps -----------------
    "AWS": {
        "category": "Cloud & DevOps",
        "aliases": [r"\baws\b", r"\bamazon\s+web\s+services\b", r"\bec2\b", r"\bs3\b", r"\blambda\b"],
        "resource": {
            "title": "AWS Skill Builder & Cloud Practitioner Path",
            "url": "https://explore.skillbuilder.aws/learn",
            "platform": "AWS Official",
            "type": "Hands-on Labs & Courses",
            "estimated_time": "3-4 weeks"
        }
    },
    "Azure": {
        "category": "Cloud & DevOps",
        "aliases": [r"\bazure\b", r"\bmicrosoft\s+azure\b"],
        "resource": {
            "title": "Microsoft Azure Fundamentals (AZ-900)",
            "url": "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-az-900/",
            "platform": "Microsoft Learn",
            "type": "Free Interactive Modules",
            "estimated_time": "2-3 weeks"
        }
    },
    "Google Cloud (GCP)": {
        "category": "Cloud & DevOps",
        "aliases": [r"\bgcp\b", r"\bgoogle\s+cloud\b", r"\bgoogle\s+cloud\s+platform\b"],
        "resource": {
            "title": "Google Cloud Skills Boost",
            "url": "https://www.cloudskillsboost.google/",
            "platform": "Google Cloud",
            "type": "Hands-on Labs",
            "estimated_time": "2-3 weeks"
        }
    },
    "Docker": {
        "category": "Cloud & DevOps",
        "aliases": [r"\bdocker\b", r"\bcontainerization\b", r"\bdockerfile\b", r"\bdocker-compose\b"],
        "resource": {
            "title": "Docker 101 Tutorial & Documentation",
            "url": "https://docs.docker.com/get-started/",
            "platform": "Docker Official",
            "type": "Hands-on Walkthrough",
            "estimated_time": "1 week"
        }
    },
    "Kubernetes": {
        "category": "Cloud & DevOps",
        "aliases": [r"\bkubernetes\b", r"\bk8s\b"],
        "resource": {
            "title": "Kubernetes Basics Tutorial",
            "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
            "platform": "Kubernetes Official",
            "type": "Interactive Scenario",
            "estimated_time": "2-3 weeks"
        }
    },
    "CI/CD": {
        "category": "Cloud & DevOps",
        "aliases": [r"\bci/cd\b", r"\bcontinuous\s+integration\b", r"\bjenkins\b", r"\bgithub\s+actions\b", r"\bgitlab\s+ci\b"],
        "resource": {
            "title": "GitHub Actions Documentation & Quickstart",
            "url": "https://docs.github.com/en/actions/quickstart",
            "platform": "GitHub Docs",
            "type": "Hands-on Guide",
            "estimated_time": "1 week"
        }
    },
    "Linux": {
        "category": "Cloud & DevOps",
        "aliases": [r"\blinux\b", r"\bubuntu\b", r"\bcentos\b", r"\bredhat\b", r"\bdebian\b"],
        "resource": {
            "title": "Linux Journey",
            "url": "https://linuxjourney.com/",
            "platform": "Linux Journey",
            "type": "Interactive Modules",
            "estimated_time": "1-2 weeks"
        }
    },

    # ----------------- Software Engineering & Methodologies -----------------
    "Git & GitHub": {
        "category": "Tools & Methodologies",
        "aliases": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b", r"\bversion\s+control\b"],
        "resource": {
            "title": "Pro Git Book (Scott Chacon & Ben Straub)",
            "url": "https://git-scm.com/book/en/v2",
            "platform": "Git Official",
            "type": "Free Complete Book",
            "estimated_time": "1 week"
        }
    },
    "Agile / Scrum": {
        "category": "Tools & Methodologies",
        "aliases": [r"\bagile\b", r"\bscrum\b", r"\bkanban\b", r"\bsprint\b", r"\bjira\b"],
        "resource": {
            "title": "The Scrum Guide",
            "url": "https://scrumguides.org/scrum-guide.html",
            "platform": "ScrumGuides.org",
            "type": "Standard Guide",
            "estimated_time": "3-4 days"
        }
    },
    "Data Structures & Algorithms": {
        "category": "Tools & Methodologies",
        "aliases": [r"\bdsa\b", r"\bdata\s+structures?\b", r"\balgorithms?\b", r"\bleetcode\b"],
        "resource": {
            "title": "NeetCode Roadmap & Algorithms",
            "url": "https://neetcode.io/roadmap",
            "platform": "NeetCode",
            "type": "Curated Coding Practice",
            "estimated_time": "4-8 weeks"
        }
    },
    "Unit Testing": {
        "category": "Tools & Methodologies",
        "aliases": [r"\bunit\s+testing\b", r"\bpytest\b", r"\bunittest\b", r"\btest\s+driven\s+development\b", r"\btdd\b"],
        "resource": {
            "title": "Effective Python Testing with PyTest",
            "url": "https://docs.pytest.org/en/stable/",
            "platform": "pytest.org",
            "type": "Official Tutorial",
            "estimated_time": "1 week"
        }
    },
    "Streamlit": {
        "category": "Tools & Methodologies",
        "aliases": [r"\bstreamlit\b"],
        "resource": {
            "title": "Streamlit Get Started & Tutorials",
            "url": "https://docs.streamlit.io/get-started",
            "platform": "Streamlit Docs",
            "type": "Hands-on Framework Guide",
            "estimated_time": "3-5 days"
        }
    },

    # ----------------- Soft Skills -----------------
    "Communication": {
        "category": "Soft Skills",
        "aliases": [r"\bcommunication\b", r"\bverbal\s+communication\b", r"\bwritten\s+communication\b", r"\bpresentation\s+skills\b"],
        "resource": {
            "title": "Effective Communication for Technical Professionals",
            "url": "https://www.coursera.org/learn/wharton-communication-skills",
            "platform": "Coursera / Wharton",
            "type": "Course",
            "estimated_time": "1-2 weeks"
        }
    },
    "Problem Solving": {
        "category": "Soft Skills",
        "aliases": [r"\bproblem\s+solving\b", r"\bcritical\s+thinking\b", r"\banalytical\s+thinking\b"],
        "resource": {
            "title": "Structured Problem Solving & Critical Thinking",
            "url": "https://www.mindtools.com/pages/article/newTMC_5-1.htm",
            "platform": "Mind Tools",
            "type": "Methodology Guide",
            "estimated_time": "1 week"
        }
    },
    "Leadership & Mentorship": {
        "category": "Soft Skills",
        "aliases": [r"\bleadership\b", r"\bmentoring\b", r"\bteam\s+leadership\b", r"\bcollaboration\b", r"\bteamwork\b"],
        "resource": {
            "title": "Engineering Management & Leadership Basics",
            "url": "https://www.coursera.org/learn/leading-teams",
            "platform": "Coursera",
            "type": "Course",
            "estimated_time": "2 weeks"
        }
    }
}


def get_default_recommendation(skill_name: str) -> Dict[str, str]:
    """Generates a structured recommendation for skills not explicitly mapped in taxonomy."""
    clean_name = skill_name.strip()
    return {
        "title": f"Mastering {clean_name}: Fundamentals & Practical Projects",
        "url": f"https://www.google.com/search?q={clean_name}+tutorial+documentation+roadmap",
        "platform": "Curated Web & Documentation",
        "type": "Tutorial & Hands-on Practice",
        "estimated_time": "1-2 weeks"
    }
