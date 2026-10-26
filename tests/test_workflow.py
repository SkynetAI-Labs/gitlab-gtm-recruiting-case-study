from datetime import date
import pytest
from core import seed_pipeline,metrics,move,priorities,ote,ROLES,profiles,AS_OF

def test_funnel_and_single_seat_consistency():
    rows=seed_pipeline();m=metrics(rows)
    assert len(profiles())==40 and len(rows)==25
    assert (m['Offer'],m['Accepted'],m['Declined'],m['Pending'],m['Open'])==(6,3,1,2,2)
    for role in ROLES:
        assert not (any(x['role']==role and x['stage']=='Accepted' for x in rows) and any(x['role']==role and x['stage']=='Offer' for x in rows))
    assert m['Applied']>=m['Screen']>=m['Interview']>=m['Offer']>=m['Accepted']

def review(rows,aid,target,note='Specific interview evidence reviewed'):
    return move(rows,aid,target,note,'Recruiter',date(2026,10,28),'Update candidate')

def test_acceptance_updates_open_seat_without_changing_offer_count():
    original=seed_pipeline();changed=review(original,'APP-017','Accepted')
    assert metrics(changed)['Open']==1
    assert metrics(changed)['Offer']==6 and metrics(changed)['Accepted']==4
    assert original[16]['stage']=='Offer'
    assert changed[16]['history'][0]['to']=='Accepted'
    assert changed[16]['entered']==AS_OF.isoformat()

@pytest.mark.parametrize('target',['Offer','Accepted','Declined'])
def test_no_skipped_stages(target):
    with pytest.raises(ValueError):review(seed_pipeline(),'APP-005',target)

def test_no_blank_decision_and_no_past_followup():
    with pytest.raises(ValueError):review(seed_pipeline(),'APP-005','Screen','  ')
    with pytest.raises(ValueError):move(seed_pipeline(),'APP-005','Screen','Evidence','Recruiter',date(2026,10,1),'Call')

def test_single_seat_blocks_second_acceptance():
    rows=seed_pipeline()
    rows=review(rows,'APP-002','Offer')
    with pytest.raises(ValueError):review(rows,'APP-002','Accepted')

def test_closed_case_and_overdue_action():
    rows=seed_pipeline()
    with pytest.raises(ValueError):review(rows,'APP-001','Interview')
    assert len(priorities(rows))==5
    updated=review(rows,'APP-003','Interview')
    assert len(priorities(updated))==4

def test_visitors_are_independent():
    first=review(seed_pipeline(),'APP-005','Screen')
    second=seed_pipeline()
    assert first[4]['stage']=='Screen' and second[4]['stage']=='Applied'

@pytest.mark.parametrize('attainment,total',[(0,80000),(75,140000),(100,160000),(200,240000)])
def test_ote_examples(attainment,total):assert ote(80000,80000,attainment)==total

def test_every_role_has_a_distinct_interview_kit():
    assert len({tuple(x['questions']) for x in ROLES.values()})==5
    assert all(len(x['competencies'])==4 and len(x['questions'])==3 for x in ROLES.values())
