from copy import deepcopy
from datetime import date
AS_OF=date(2026,10,26)
STAGES=['Applied','Screen','Interview','Offer','Accepted']
ROLES={
'Account Executive':{
'scope':'Enterprise · UK & Ireland · new business',
'outcome':'Build pipeline and lead complex enterprise opportunities.',
'intake':'Agree territory maturity, named accounts, quota definition, ramp treatment, sales cycle and specialist support.',
'competencies':['Commercial discovery','Deal ownership','Forecast discipline','Technical partnership'],
'questions':['Walk me through a complex deal you personally won. Who controlled budget, what changed during procurement and what was your contribution?','Compare your last two quota years. How did territory, ramp and inherited accounts affect the result?','Tell me about a deal you removed from forecast. What evidence changed your view?'],
'sourcing':'Enterprise software sellers; extend to cloud, security and infrastructure. Test developer-tool familiarity through examples.',
'exercise':'Map the buying group for a fictional customer with fragmented development and security tools.'},
'Solutions Architect':{
'scope':'Enterprise · EMEA · pre-sales',
'outcome':'Translate discovery into a credible customer evaluation.',
'intake':'Agree discovery ownership, technical depth, evaluation success criteria, travel and interviewer responsibilities.',
'competencies':['Technical discovery','Evaluation design','Security awareness','Commercial partnership'],
'questions':['Describe an evaluation where the initial requirement was not the real customer problem. What changed?','How did you agree success criteria, owners and a decision date for a proof of value?','When did you advise a seller that the proposed solution was not ready for the customer?'],
'sourcing':'Pre-sales talent across CI/CD, cloud, application security and infrastructure; consider practitioners with customer-facing evidence.',
'exercise':'Scope an evaluation with a technical interviewer, explaining assumptions and acceptance criteria.'},
'Customer Success':{
'scope':'Enterprise · EMEA · adoption and retention',
'outcome':'Connect adoption to value and surface renewal risk early.',
'intake':'Clarify adoption versus renewal ownership, account load, customer maturity and partnership with account executives.',
'competencies':['Success planning','Risk diagnosis','Stakeholder engagement','Value communication'],
'questions':['Walk me through an at-risk account. Which signals appeared first and what action did you own?','How did you connect adoption to an outcome the customer valued?','Describe a difficult renewal. What belonged to you and what belonged to the account executive?'],
'sourcing':'Enterprise SaaS success and technical account management; investigate measurable contribution rather than title alone.',
'exercise':'Write a recovery plan for low adoption before renewal, separating facts from hypotheses.'},
'Sales Development':{
'scope':'Commercial · UK & Ireland · outbound',
'outcome':'Create relevant, qualified conversations and accurate handoffs.',
'intake':'Agree inbound/outbound split, accepted-opportunity definition, target accounts, coaching and ramp expectations.',
'competencies':['Account research','Relevant outreach','Qualification','Learning agility'],
'questions':['How would you research an account and turn that into a short relevant message?','Tell me about a meeting an AE rejected. What did you learn about qualification?','Which change improved accepted opportunities, and how did you distinguish quality from activity?'],
'sourcing':'Software SDRs and adjacent B2B prospecting; accept demonstrable research and learning in place of a narrow employer pedigree.',
'exercise':'Prepare one message and a handoff note from a fictional account brief; offer an accessible format.'},
'Sales Operations':{
'scope':'GTM operations · EMEA · reporting and process',
'outcome':'Improve reporting trust and remove a measurable process friction.',
'intake':'Agree systems scope, data access, territory versus compensation responsibilities and change ownership.',
'competencies':['Data quality','Process diagnosis','Stakeholder influence','Change control'],
'questions':['Describe a reporting discrepancy. How did you trace its cause and restore trust?','Tell me about a territory or process change sales leaders resisted. How did you influence it?','How would you validate a dashboard before leaders used it for decisions?'],
'sourcing':'Sales/revenue operations in software and adjacent analytical operations; verify CRM literacy and business impact.',
'exercise':'Investigate a fictional CRM extract and recommend one controlled improvement.'}}

def profiles():
    channels=['Targeted outreach','Applicant','Referral','Internal mobility','Talent community']
    return [{'id':f'GL-{r*8+i+1:03}','role':role,'background':['Developer tools','Cloud infrastructure','Security software','Adjacent B2B services'][i%4],'region':['UK & Ireland','DACH','Southern Europe','Northern Europe'][i%4],'channel':channels[(r+i)%5]} for r,role in enumerate(ROLES) for i in range(8)]

def seed_pipeline():
    rows=[]
    people=profiles()
    for r,role in enumerate(ROLES):
        for i in range(5):
            stage=['Accepted','Offer','Interview','Screen','Applied'][i]
            if i==1:stage='Offer' if r in (3,4) else 'Interview'
            if i==0 and r==3:stage='Declined'
            if i==0 and r==4:stage='Interview'
            reached=STAGES[:STAGES.index(stage)+1] if stage in STAGES else STAGES[:4]
            rows.append({'id':f'APP-{r*5+i+1:03}','candidate':people[r*8+i]['id'],'role':role,'stage':stage,'reached':reached,'source':people[r*8+i]['channel'],'entered':'2026-10-20' if i==2 else '2026-10-24','due':'2026-10-23' if i==2 else '2026-10-28','owner':'Hiring manager' if i==2 else 'Recruiter','action':'Submit competency feedback' if i==2 else 'Confirm next step with candidate','note':'','history':[]})
    return rows

def metrics(rows):
    return {**{s:sum(s in x['reached'] for x in rows) for s in STAGES},'Declined':sum(x['stage']=='Declined' for x in rows),'Pending':sum(x['stage']=='Offer' for x in rows),'Open':len(ROLES)-len({x['role'] for x in rows if x['stage']=='Accepted'})}

def move(rows,aid,target,note,owner,due,action):
    result=deepcopy(rows)
    row=next(x for x in result if x['id']==aid)
    if not note.strip() or not owner.strip() or not action.strip():raise ValueError('Record evidence, an owner and a next action before saving.')
    if not isinstance(due,date) or due<AS_OF:raise ValueError('Choose a next-action date on or after the scenario date.')
    current=row['stage']
    if current not in STAGES[:-1]:raise ValueError('This application is closed; reopening needs a separate reviewed process.')
    allowed=['Withdrawn','Rejected']+([STAGES[STAGES.index(current)+1]] if current!='Offer' else ['Accepted','Declined'])
    if target!=current and target not in allowed:raise ValueError('Move one stage at a time, or record a reviewed closure.')
    if target=='Accepted' and any(x['role']==row['role'] and x['stage']=='Accepted' for x in result):raise ValueError('This single-seat search already has an accepted offer.')
    row['history'].append({'from':current,'to':target,'evidence':note.strip(),'date':AS_OF.isoformat()})
    row.update(stage=target,note=note.strip(),owner=owner.strip(),due=due.isoformat(),action=action.strip())
    if target!=current:row['entered']=AS_OF.isoformat()
    if target in STAGES and target not in row['reached']:row['reached'].append(target)
    return result

def ote(base,variable,attainment):
    if base<0 or variable<0 or not 0<=attainment<=200:raise ValueError('Invalid illustrative compensation inputs.')
    return base+variable*attainment/100

def priorities(rows):
    return [dict(x,days_in_stage=(AS_OF-date.fromisoformat(x['entered'])).days) for x in rows if x['stage'] in STAGES[:-1] and date.fromisoformat(x['due'])<AS_OF]

