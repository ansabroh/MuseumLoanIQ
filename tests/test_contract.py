import copy
import hashlib
import json
import pytest

URL = 'https://raw.githubusercontent.com/ansabroh/MuseumLoanIQ/' + 'a'*40 + '/evidence/sample.json'

def terms(borrower):
    return dict(artifact_id='ML-001',title='Study ceramic bowl',lender='Demo Museum (synthetic)',borrower='0x'+borrower.hex(),handling='Upright sealed climate-controlled crate; courier supervision required.',start=1000,end=1120,max_gap_seconds=60,temp_min_c100=1800,temp_max_c100=2200,rh_min_pct100=4500,rh_max_pct100=5500)

def packet():
    return dict(loan_id='demo',artifact_id='ML-001',before_report='Rim intact. Stable glaze crazing documented at dispatch.',after_report='Rim intact. Stable glaze crazing unchanged on return.',transport_report='Upright sealed climate-controlled crate under courier supervision throughout transit.',sources=[dict(issuer='Demo Museum (synthetic)',reference='Synthetic condition and logger fixture')],readings=[dict(time=t,temp_c100=2000,rh_pct100=5000) for t in [1000,1060,1120]])

def review(p,condition='UNCHANGED',transport='SATISFIED'):
    return json.dumps(dict(condition=condition,transport=transport,before_quote=p['before_report'],after_quote=p['after_report'],transport_quote=p['transport_report'],reason='Reports document the same condition and required transport.'))

@pytest.fixture
def setup(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy('contracts/museum_loan_iq.py')
    direct_vm.sender=direct_alice
    c.register_loan('demo',json.dumps(terms(direct_bob)))
    h=json.loads(c.get_loan('demo'))['terms_hash']
    direct_vm.sender=direct_bob
    c.accept_loan('demo',h)
    direct_vm.sender=direct_alice
    return c,direct_vm

def submit(c,vm,p,model=None):
    body=json.dumps(p)
    c.submit_evidence('demo',URL,hashlib.sha256(body.encode()).hexdigest(),'Fixture evaluation')
    vm.mock_web(r'raw\.githubusercontent\.com',dict(status=200,body=body))
    vm.mock_llm(r'You are reviewing',model or review(p))
    c.assess('demo')
    return json.loads(c.get_loan('demo'))['assessments'][-1]

@pytest.mark.parametrize('condition,transport,expected',[('UNCHANGED','SATISFIED','COMPLIANT'),('CHANGED','SATISFIED','REVIEW_REQUIRED'),('UNCERTAIN','SATISFIED','INCONCLUSIVE'),('UNCHANGED','VIOLATED','NONCOMPLIANT'),('UNCHANGED','UNCERTAIN','INCONCLUSIVE')])
def test_semantics(setup,condition,transport,expected):
    c,vm=setup;p=packet();r=submit(c,vm,p,review(p,condition,transport));assert r['outcome']==expected, r['error']

@pytest.mark.parametrize('field,value',[('temp_c100',2201),('rh_pct100',5501),('temp_c100',1799),('rh_pct100',4499)])
def test_breaches_override_ai(setup,field,value):
    c,vm=setup;p=packet();p['readings'][1][field]=value
    assert submit(c,vm,p)['outcome']=='NONCOMPLIANT'

def test_gap_fails_closed(setup):
    c,vm=setup;p=packet();p['readings'].pop(1);assert submit(c,vm,p)['outcome']=='INCONCLUSIVE'

def test_invalid_quote_fails_closed(setup):
    c,vm=setup;p=packet();r=json.loads(review(p));r['after_quote']='Invented condition quotation';assert submit(c,vm,p,json.dumps(r))['outcome']=='INCONCLUSIVE'

def test_dissent(setup):
    c,vm=setup;p=packet();submit(c,vm,p);vm.clear_mocks();vm.mock_llm(r'You are reviewing',review(p,'CHANGED'));assert vm.run_validator() is False

def test_grounded_agreement(setup):
    c,vm=setup;p=packet();submit(c,vm,p);assert vm.run_validator() is True

def test_access_control(setup,direct_charlie):
    c,vm=setup;vm.sender=direct_charlie
    with vm.expect_revert('Loan parties only'):c.submit_evidence('demo',URL,'a'*64,'Test')
    with vm.expect_revert('Borrower only'):c.accept_loan('demo','a'*64)

def test_immutable_terms(setup,direct_bob):
    c,vm=setup
    with vm.expect_revert('Loan already exists'):c.register_loan('demo',json.dumps(terms(direct_bob)))

def test_unpinned_url(setup):
    c,vm=setup
    with vm.expect_revert('commit-pinned'):c.submit_evidence('demo',URL.replace('a'*40,'main'),'a'*64,'Test')

def test_hash_mismatch(setup):
    c,vm=setup;c.submit_evidence('demo',URL,'a'*64,'Test');vm.mock_web('.*',dict(status=200,body=json.dumps(packet())))
    with pytest.raises(Exception):c.assess('demo')
    assert len(json.loads(c.get_loan('demo'))['assessments'])==0

@pytest.mark.parametrize('mutation',[lambda p:p.update(artifact_id='wrong'),lambda p:p['readings'].reverse(),lambda p:p['readings'][0].update(temp_c100=True)])
def test_invalid_packet(setup,mutation):
    c,vm=setup;p=packet();mutation(p)
    with pytest.raises(Exception):submit(c,vm,p)

def test_append_only_chain(setup):
    c,vm=setup;p=packet();a=submit(c,vm,p);vm.clear_mocks();p['after_report']+=' Additional inspection pending.';b=submit(c,vm,p,review(p,'UNCERTAIN'))
    assert b['previous_hash']==a['receipt_hash'];assert b['version']==2
    state=json.loads(c.get_loan('demo'));assert state['assessments'][0]==a
