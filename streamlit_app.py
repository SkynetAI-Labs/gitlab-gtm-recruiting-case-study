from datetime import date
import base64
import pandas as pd
import altair as alt
import streamlit as st
from core import ROLES,AS_OF,STAGES,profiles,seed_pipeline,metrics,move,ote,priorities
LOGO_SVG='<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><title>SkynetAI-Labs logo</title><path d="M48 5 85 26v44L48 91 11 70V26Z" fill="#221e38" stroke="#a78bfa" stroke-width="2.5"/><path d="M64 29H37l-8 9 8 10h22l8 10-8 9H32" fill="none" stroke="#fc9c73" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M48 7v12M85 48H74M22 48H11M48 77v12" fill="none" stroke="#a78bfa" stroke-width="2.5"/><circle cx="48" cy="7" r="4" fill="#a78bfa"/><circle cx="85" cy="48" r="4" fill="#a78bfa"/><circle cx="11" cy="48" r="4" fill="#a78bfa"/><circle cx="48" cy="89" r="4" fill="#a78bfa"/></svg>'
LOGO_URI='data:image/svg+xml;base64,'+base64.b64encode(LOGO_SVG.encode()).decode()
st.set_page_config(page_title='GTM Recruiting Case Study | SkynetAI-Labs',page_icon='◆',layout='wide')
st.markdown('''<style>.block-container{max-width:1420px;padding-top:3.5rem}h1{letter-spacing:-1.3px}h2{letter-spacing:-.5px}[data-testid="stMetric"]{background:#221e38;border:1px solid #494064;padding:16px;border-radius:14px}.eyebrow{letter-spacing:3px;font-size:12px;color:#fca779;font-weight:700}.lead{font-size:20px;color:#d1c9e8}section[data-testid="stSidebar"]{border-right:1px solid #494064}#MainMenu,footer,[data-testid="stAppDeployButton"]{display:none!important}</style>''',unsafe_allow_html=True)
if 'pipeline' not in st.session_state:st.session_state.pipeline=seed_pipeline()
rows=st.session_state.pipeline
report=metrics(rows)
people=profiles()
pages=['Start here','Part 1 · Intake & strategy','Part 2 · Talent sourcing','Part 3 · Structured assessment','Part 4 · Pipeline & candidate care','Part 5 · Closing & first 90 days']
with st.sidebar:
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin:8px 0 20px"><img src="{LOGO_URI}" alt="SkynetAI-Labs logo" width="58" height="58"><span style="font-size:18px;font-weight:750;letter-spacing:1px">SKYNETAI-LABS</span></div>',unsafe_allow_html=True)
    st.caption('Case study for GitLab™’s GTM Recruiter role')
    st.caption('By Adam Baig · SkynetAI-Labs')
    page=st.radio('Case study',pages)
    st.divider()
    st.caption(f'{report["Open"]} open of 5 hypothetical searches · 40 mapped prospects')
    st.link_button('Adam Baig · LinkedIn','https://www.linkedin.com/in/adambaiguk')
    st.caption('Scenario date · 26 October 2026')
st.markdown(f'<div style="display:flex;align-items:center;gap:18px;margin-bottom:22px"><img src="{LOGO_URI}" alt="SkynetAI-Labs logo" width="78" height="78"><div><div style="font-size:27px;font-weight:800;letter-spacing:2px">SKYNETAI-LABS</div><div class="eyebrow">RECRUITING INTELLIGENCE</div></div></div>',unsafe_allow_html=True)
st.markdown('**Case study for GitLab™’s GTM Recruiter role**')
st.caption('GITLAB is a trademark of GitLab Inc. in the United States and other countries and regions.')
st.title(page)
if page==pages[0]:
    st.markdown('<p class="lead">From a clear hiring brief to a well-informed acceptance.</p>',unsafe_allow_html=True)
    st.write('**By Adam Baig** · 20+ years in recruitment, applied to GitLab’s GTM Recruiter challenge.')
    st.caption('Independent, AI-assisted portfolio demonstration. Candidate records, search briefs, pay examples and pipeline outcomes are fictional.')
    a,b=st.columns(2)
    with a:
        st.subheader('The hiring problem')
        st.write('Hiring across sales and technical-commercial teams requires more than matching job titles. Territory, buying complexity, personal contribution and customer outcomes change what good evidence looks like.')
    with b:
        st.subheader('My approach')
        st.write('Agree the brief, widen the search thoughtfully, test evidence through structured conversations and keep every next step owned. Write decisions clearly enough that a colleague in another time zone can act on them.')
    st.info('The worked example: one seller achieved 126% in an established territory; another achieved 91% while building a new patch. Part 3 shows what I would investigate before recommending either.')
    for col,title,body in zip(st.columns(3),['Calibrate','Build','Refine'],['Agree five role briefs, evidence standards and realistic timelines.','Map direct and adjacent talent; test outreach and candidate experience.','Use stage ageing, feedback and offer insight to improve the search.']):
        with col:st.markdown('### '+title);st.write(body)
    st.write('**The demonstration:** 40 mapped prospects → 25 applications → 6 offers → 3 acceptances, 1 decline and 2 pending decisions across five searches.')
    st.link_button('The role this case study addresses','https://job-boards.greenhouse.io/gitlab/jobs/8869149002')
    st.link_button('My GitLab DevSecOps project','https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline')
elif page==pages[1]:
    st.markdown('<p class="lead">Five distinct briefs. One consistent standard of evidence.</p>',unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([{'Role':r,'Illustrative scope':v['scope'],'Hiring outcome':v['outcome']} for r,v in ROLES.items()]),hide_index=True,width='stretch')
    role=st.selectbox('Open a hiring brief',list(ROLES));spec=ROLES[role]
    a,b=st.columns(2)
    with a:st.subheader('What I would settle at intake');st.write(spec['intake'])
    with b:st.subheader('Where I would search');st.write(spec['sourcing'])
    st.markdown('**Operating sequence:** Intake → agree evidence → map market → engage → assess → close → review.')
    with st.expander('Interview plan and search risks'):
        st.dataframe(pd.DataFrame([{'Conversation':'Recruiter screen','Purpose':'Motivation, scope, contribution and expectations','Owner':'Recruiter'},{'Conversation':'Hiring manager','Purpose':'Role outcomes and competency evidence','Owner':'Hiring manager'},{'Conversation':'Work example','Purpose':spec['exercise'],'Owner':'Functional partner'},{'Conversation':'Debrief','Purpose':'Compare evidence, resolve disagreement and agree next steps','Owner':'Hiring manager with recruiter'}]),hide_index=True,width='stretch')
        st.write('**Early escalation:** conflicting briefs, unrealistic territory assumptions, delayed feedback or compensation misalignment. Agree a decision owner and next action before adding interviews.')
        st.write('**Candidate care:** explain stages and preparation, ask about accommodations, avoid duplicate assessments and agree communication dates. Keep work examples proportionate; do not request unpaid customer work.')
elif page==pages[2]:
    st.markdown('<p class="lead">Widen the market without lowering the evidence standard.</p>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    role=a.selectbox('Role family',['All roles']+list(ROLES));channel=b.selectbox('Route to talent',['All channels']+sorted({x['channel'] for x in people}));query=c.text_input('Search background or region',placeholder='e.g. security or DACH')
    selected=[x for x in people if (role=='All roles' or x['role']==role) and (channel=='All channels' or x['channel']==channel) and query.casefold() in (x['background']+' '+x['region']).casefold()]
    st.metric('Mapped prospects in view',len(selected))
    st.dataframe(pd.DataFrame(selected,columns=['id','role','background','region','channel']),hide_index=True,width='stretch')
    st.subheader('A balanced sourcing plan')
    st.dataframe(pd.DataFrame([{'Route':'Applicants','Recruiter action':'Review competencies; separate essential evidence from employer pedigree.'},{'Route':'Targeted outreach','Recruiter action':'Compare direct developer-tool talent with cloud, security and adjacent B2B experience.'},{'Route':'Referrals','Recruiter action':'Apply the same standards; avoid allowing one network to dominate the shortlist.'},{'Route':'Internal mobility','Recruiter action':'Explore transferable skills and readiness through the appropriate process.'},{'Route':'Talent community','Recruiter action':'Re-engage with appropriate permission, relevant context and a clear proposition.'}]),hide_index=True,width='stretch')
    with st.expander('Market hypotheses and inclusion in practice'):
        st.write('Developer tools may offer closer buyer familiarity; cloud and security may offer comparable buying complexity. These are sourcing hypotheses to test, not evidence of individual proficiency.')
        st.write('Advertise outcomes clearly, offer accessible interviews and examine where the process loses people. Do not infer demographic characteristics from names, locations or employers. Use appropriately governed aggregate data for any real representation analysis.')
        st.write('Validate customer coverage, language and location requirements with the hiring team. Remote working does not make every role location-independent.')
elif page==pages[3]:
    st.markdown('<p class="lead">A quota percentage starts a conversation. It does not finish one.</p>',unsafe_allow_html=True)
    example,kit=st.tabs(['AE judgment example','Role-specific interview kit'])
    with example:
        st.caption('Standalone comparison before screening; separate from the pipeline simulation.')
        a,b=st.columns(2)
        with a:
            st.subheader('Seller A · 126% attainment')
            st.write('Established territory; 70% of revenue from inherited accounts; three years in seat.')
            st.markdown('**Investigate:** separate renewal and expansion contribution from personally generated new business. Confirm quota definition and deal ownership.')
        with b:
            st.subheader('Seller B · 91% attainment')
            st.write('New territory; first full quota year; built a new executive buying group.')
            st.markdown('**Investigate:** validate closed revenue, pipeline quality, ramp treatment and repeatability against the territory plan.')
        st.success('My next step: screen both against the same brief. Test new-business ownership, territory conditions and repeatability before recommending either to the hiring manager.')
        st.write('**What could change my view:** the 126% seller may demonstrate substantial new-logo ownership; the 91% seller may show weak qualification despite a difficult patch. Neither interpretation is established by the headline number.')
        st.text_area('Recruiter working note',value='Both candidates merit a structured screen. Verify the quota period and definition, ramp treatment, inherited accounts, personally owned deals and buying-group complexity. Compare the evidence against the agreed role outcomes.',height=125)
    with kit:
        role=st.selectbox('Choose a role scorecard',list(ROLES));spec=ROLES[role]
        st.dataframe(pd.DataFrame([{'Competency':c,'Evidence standard':'Specific example, personal contribution, outcome and context'} for c in spec['competencies']]),hide_index=True,width='stretch')
        st.subheader('Questions I would ask')
        for q in spec['questions']:st.markdown('- '+q)
        st.write('**Work example:** '+spec['exercise'])
        st.write('**Debrief rubric:** Not yet evidenced · Partial evidence · Clear evidence · Strong evidence. Record the example and uncertainty alongside the rating; resolve follow-up in the debrief.')
        st.download_button('Download interview kit',data='\n\n'.join([role,spec['intake'],*spec['competencies'],*spec['questions'],spec['exercise']]),file_name='interview-kit.txt')
    with st.expander('Responsible AI workflow'):
        st.write('I would use AI to draft a search plan or improve a fictional interview kit, then check relevance, assumptions and factual claims myself. This demonstration sends no candidate records to a language model. A recruiter owns each recorded stage change.')
elif page==pages[4]:
    st.markdown('<p class="lead">Every candidate has a next step. Every blocker has an owner.</p>',unsafe_allow_html=True)
    for c,label,value in zip(st.columns(4),['Open searches','Applications','Offers made','Accepted offers'],[report['Open'],report['Applied'],report['Offer'],report['Accepted']]):c.metric(label,value)
    health,workbench=st.tabs(['Pipeline health','Recruiter workbench'])
    with health:
        st.altair_chart(alt.Chart(pd.DataFrame({'Stage':STAGES,'Reached stage':[report[s] for s in STAGES]})).mark_bar(color='#fc9c73').encode(x=alt.X('Stage:N',sort=STAGES,title=None),y=alt.Y('Reached stage:Q',title='Applications'),tooltip=['Stage','Reached stage']),width='stretch')
        st.caption(f"Cumulative stages · {report['Accepted']} accepted · {report['Declined']} declined · {report['Pending']} pending. Mapped prospects are distinct from applications.")
        overdue=priorities(rows)
        st.subheader('Actions requiring attention')
        if overdue:st.dataframe(pd.DataFrame([{k:x[k] for k in ['id','role','stage','days_in_stage','owner','due','action']} for x in overdue]),hide_index=True,width='stretch')
        else:st.success('No overdue open actions in this session.')
        st.write('**My intervention:** request missing competency feedback with an owner and due date; tell the candidate when they will next hear from us. Escalate a recurring delay rather than leaving candidates in an unexplained holding pattern.')
        st.subheader('Asynchronous hiring-manager update')
        st.write(f"**26 October:** {report['Open']} searches remain open; {report['Pending']} offers await decisions. {len(overdue)} open actions are overdue. **Decision needed:** resolve missing feedback before adding interviews. **Owner:** hiring manager for assessment; recruiter for candidate communication. **Next review:** 28 October.")
    with workbench:
        st.dataframe(pd.DataFrame([{k:x[k] for k in ['id','candidate','role','source','stage','owner','due']} for x in rows]),hide_index=True,width='stretch')
        aid=st.selectbox('Application to review',[x['id'] for x in rows],index=16);current=next(x for x in rows if x['id']==aid)
        st.write(f"**{current['candidate']} · {current['role']} · {current['stage']}**")
        with st.form('review'):
            choices=STAGES+['Declined','Withdrawn','Rejected']
            target=st.selectbox('Record stage',choices,index=choices.index(current['stage']))
            note=st.text_area('Evidence and reason for this decision',value=current['note'])
            a,b=st.columns(2);owner=a.text_input('Next-action owner',current['owner']);due=b.date_input('Next-action date',value=max(AS_OF,date.fromisoformat(current['due'])))
            action=st.text_input('Next action',current['action']);saved=st.form_submit_button('Save recruiter review')
        if saved:
            try:st.session_state.pipeline=move(rows,aid,target,note,owner,due,action);st.rerun()
            except ValueError as e:st.error(str(e))
        if current['history']:st.dataframe(pd.DataFrame(current['history']),hide_index=True,width='stretch')
        st.caption('Changes stay in your visitor session. This is an ATS-style example, with no Greenhouse connection.')
        st.download_button('Download application notes',data=pd.DataFrame([{k:x[k] for k in ['id','candidate','role','source','stage','owner','due','action','note']} for x in rows]).to_csv(index=False),file_name='fictional-application-notes.csv')
else:
    st.markdown('<p class="lead">Clear expectations support a better-informed offer decision.</p>',unsafe_allow_html=True)
    closing,executive=st.tabs(['Offer conversation','Executive case study'])
    with closing:
        st.subheader('Illustrative compensation conversation')
        st.caption('Fictional GBP sales examples; these are not GitLab salary bands or an actual incentive plan.')
        a,b,c=st.columns(3);base=a.number_input('Annual base (£)',min_value=0,value=80000,step=5000);variable=b.number_input('Target annual variable (£)',min_value=0,value=80000,step=5000);attainment=c.slider('Illustrative attainment (%)',0,200,75,5)
        a,b=st.columns(2);a.metric('OTE at 100% target',f'£{base+variable:,.0f}');b.metric('Illustrative total at selected attainment',f'£{ote(base,variable,attainment):,.0f}')
        st.write('This simple example assumes linear variable pay. Actual payouts depend on the written plan, eligibility, crediting, thresholds, accelerators, caps and payment timing. OTE is not guaranteed earnings.')
        st.markdown('**Before an offer:** clarify base and variable, quota definition, territory, ramp treatment, plan documents and candidate priorities. Agree who will explain specialist detail.')
        st.markdown('**Candidate message example:** “Before you decide, I would like to walk through the written package and the assumptions behind target earnings. Which parts of the territory, ramp or incentive plan would you like us to clarify? Let’s agree a useful follow-up time.”')
    with executive:
        st.subheader('My case for the role')
        st.write('I bring 20+ years of full-cycle recruitment, international hiring and business development. Recruiting sales managers, sales engineers and business development professionals for industrial and energy clients gives me a practical starting point for technical-commercial hiring.')
        st.write('I would apply that experience through disciplined intake, transferable talent research and evidence-led conversations, while learning GitLab’s sales segments, customer needs and operating practices. I am interested in the hands-on work: owning searches, maintaining clear records and following through with candidates and hiring teams.')
        st.table(pd.DataFrame([{'Period':'Days 1–30','Focus':'Learn segments; calibrate briefs, scorecards, ATS expectations and communication routines.','Evidence':'Agreed briefs and a credible baseline.'},{'Period':'Days 31–60','Focus':'Run balanced searches, structured screens and written risk updates.','Evidence':'Useful evidence and timely hiring-team decisions.'},{'Period':'Days 61–90','Focus':'Review source quality, stage delays, offer questions and candidate feedback.','Evidence':'A documented improvement and a reusable resource.'}]))
        st.markdown('**Next step:** pressure-test the AE comparison and one live hiring brief with the GTM recruiting team in week one.')
    with st.expander('Research and sources'):
        st.write('This is my proposed workflow, informed by the vacancy and public communication guidance.')
        st.markdown('- [Recruiter, GTM · official vacancy](https://job-boards.greenhouse.io/gitlab/jobs/8869149002)\n- [GitLab communication handbook](https://handbook.gitlab.com/handbook/communication/)\n- [All-remote meeting guidance](https://handbook.gitlab.com/handbook/company/culture/all-remote/meetings/)')
        st.caption('Reviewed 26 October 2026. The advertised US recruiter salary range is not a UK sales pay benchmark. Third-party LinkedIn headcount estimates were not used as established facts.')
st.divider()
st.caption('Independent case study · Fictional data and simulated results · Human decisions throughout · No GitLab affiliation or endorsement')

