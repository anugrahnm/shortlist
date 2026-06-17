import httpx

jd = """About the job

About Avyn

Avyn is the AI analyst for private markets.


Every fund is hunting for the deal that matters, but finding it means reading the entire market rather than a shortlist, which no human analyst has the hours to do. Avyn reads every company, ranks them against your thesis, surfaces who you already know and who can make the warm intro, then drafts outreach in your voice. The aim is less a tool you operate and more an analyst that handles the work end to end.


An early-stage London team with product-market fit, fast-growing revenue, and a right to win. Two engineers build the core platform today, shipping fast with agentic workflows.


The Role

You'd be our next dedicated product hire, owning features end to end and working directly with the CTO and CEO on decisions that shape the product for years. The technical surface is wide. In a given week you might build a lead-generation pipeline, ship a CRM integration, design a network-visualisation interface, or improve our agentic dev flows. The backend is Python (FastAPI, Postgres) on GCP, and you'll be hands-on with deployments, CI/CD, and infrastructure.


What we're looking for

    2–4 years' experience, backend-leaning full stack
    Strong Python and SQL fundamentals
    A power user of the latest AI tools, obsessed with automating manual work
    Comfortable with CI/CD, container deployments, and cloud services (GCP a plus)
    You ship clean code quickly and take full ownership
    You care about the product as much as the tech"""
    




response = httpx.post("http://127.0.0.1:8000/analyze", json={"text": jd})
print(response.json())

