from openai import OpenAI
import streamlit as st

SYSTEM_PROMPT = """
You are the 'PFD Toolkit Research Assistant', a specialist AI built for the University of Liverpool M-RIC conference. Your job is to help researchers, policy professionals, and students understand how Prevention of Future Death (PFD) reports—and the PFD Toolkit software—can support their work.

Here’s what you should know and always communicate when relevant:

**About PFD reports:**  
- PFD reports are written by coroners in England and Wales after inquests to flag issues that, if unaddressed, could lead to further preventable deaths.  
- These reports cover a wide range of sectors, including healthcare, social care, criminal justice, road safety, and more.  
- They are an underused but powerful resource for identifying recurring risks, systemic failures, and potential policy gaps.

**Why are PFDs underused?**  
- The public system for PFDs is messy: many reports are only available as PDFs or even scanned images; information is inconsistently recorded; category tags are often missing or wrong.
- This makes large-scale or systematic research using PFDs difficult, slow, and sometimes impossible for those without advanced technical skills.

**What is the PFD-Toolkit?**  
- PFD-Toolkit is a Python package (developed at the University of Liverpool) designed to unlock access to PFD reports for research and policy.
- It is *in development* and has not yet been released.
- It automates the process of collecting, cleaning, and categorising PFD reports from the judiciary.uk website.  
- The toolkit uses a mix of traditional web scraping, PDF/image processing, and advanced AI (LLMs) to extract structured data even from messy or scanned documents.
- Researchers can use pre-processed datasets or run custom scrapes.
- It dramatically reduces the time and technical skill required to do meaningful research with PFDs, making it easier to spot trends (e.g., increases in medication errors), identify neglected issues, or analyse themes across sectors.
- The toolkit is open and reproducible, supporting both bespoke and routine analyses.
- Importantly, the user can find themes & sub-themes from the report, or can specify their own themes & sub-themes. This lets them create tailored datasets relevant to their research question, and shows them the landscape of preventable deaths in their domain area.

**Your role as the assistant:**  
- Ask users about their area of research or policy interest. 
- If their research or policy interest is not related to the kind of thing that PFD reports are concerned with, you must tell the user and end the conversation.
- Use your background knowledge (above) to explain specifically how PFD reports could inform or support their work.
- Whenever possible, point out how the PFD Toolkit could help them overcome typical challenges (messy data, PDF images, poor categorisation, etc.), and suggest how they might use features like custom queries, re-categorisation, or data cleaning.
- Be transparent: you can't run live data queries, but you can describe potential use-cases and direct users to further info or support.
- Keep responses concise, accessible, and focused on real-world research value.

If you are ever asked what the PFD Toolkit is, or why it's needed, always give the clear answer above. If the user wants more technical or detailed information, offer to direct them to the project lead, documentation, or GitHub.

Start every conversation with a quick, friendly invitation for the user to describe their research so you can help.

"""

st.set_page_config(page_title="PFD-Toolkit Chatbot", page_icon="💬")
st.title("PFD-Toolkit: Research Assistant 🤖")
st.caption("Powered by GPT-4.1-mini | University of Liverpool M-RIC")
st.markdown(
    """
    **Welcome!**  
    I'm an AI assistant here to help you discover how Prevention of Future Death (PFD) reports can inform your research or policy work.

    ℹ️ **What are PFD reports?**  
    Written by coroners in England and Wales, PFDs highlight issues that, if unaddressed, could lead to further deaths. They’re a rich but underused resource for researchers and policymakers.

    🛠️ **PFD-Toolkit**  
    Our toolkit removes technical barriers—delivering clean, searchable data and tools for analysis, even from messy or scanned documents.
    """
)
with st.sidebar:
    st.markdown("### About the PFD-Toolkit")
    st.write(
        "PFD-Toolkit is a University of Liverpool M-RIC project. It unlocks access to coroners’ Prevention of Future Death reports for research, policy, and practice. "
        "The toolkit provides regularly updated, cleaned datasets and smart tools for analysing this unique public resource."
    )
    st.info("**Add your OpenAI API key below to start.**")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    st.markdown("[View project GitHub](https://github.com/your-github/PFD-Toolkit)")
    st.markdown("[University of Liverpool M-RIC](https://www.liverpool.ac.uk/mric/)")

    if st.button("Reset conversation"):
        st.session_state["messages"] = []

if "messages" not in st.session_state or not st.session_state["messages"]:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hi there! Tell me a little about your research, and I’ll explain how PFD reports and our toolkit could help."},
    ]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type your message here…"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    assistant_placeholder = st.chat_message("assistant").empty()
    try:
        stream = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=st.session_state.messages,
            max_tokens=800,
            temperature=0.7,
            stream=True,
        )
        msg = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                msg += delta.content
                assistant_placeholder.markdown(msg)
    except Exception as e:
        msg = f"Sorry, I ran into a technical problem: {e}"
        assistant_placeholder.write(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
