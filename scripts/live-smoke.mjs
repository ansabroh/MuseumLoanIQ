import {createClient,createAccount} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {readFileSync,writeFileSync} from 'node:fs';import {createHash} from 'node:crypto';
import {follow} from '../src/lifecycle.js';
const config=JSON.parse(readFileSync('public/deployment.json'));
const lender=createAccount('0x'+'11'.repeat(32)),borrower=createAccount('0x'+'22'.repeat(32));
let client=createClient({chain:studionet,account:lender});
const id=config.demoLoan,receipts=[];
async function write(name,args){const hash=await client.writeContract({address:config.address,functionName:name,args});console.log(name,hash);const tx=await follow(client,hash,s=>{}, {attempts:180,delay:2000});receipts.push({method:name,hash,status:tx.statusName||tx.status_name||tx.status,execution:tx.consensus_data.leader_receipt[0].execution_result});writeFileSync('evidence/live-transactions.json',JSON.stringify(receipts,null,2));}
const terms={artifact_id:'ML-001',title:'Study ceramic bowl · synthetic demonstration',lender:'Demo Museum (synthetic)',borrower:borrower.address,handling:'Upright sealed climate-controlled crate; courier supervision required.',start:1000,end:1120,max_gap_seconds:60,temp_min_c100:1800,temp_max_c100:2200,rh_min_pct100:4500,rh_max_pct100:5500};
await write('register_loan',[id,JSON.stringify(terms)]);
let loan=JSON.parse(await client.readContract({address:config.address,functionName:'get_loan',args:[id]}));
client=createClient({chain:studionet,account:borrower});await write('accept_loan',[id,loan.terms_hash]);client=createClient({chain:studionet,account:lender});
for(const file of ['sample-packet','changed-packet','breach-packet']){
 const body=readFileSync(`evidence/${file}.json`);const sha=createHash('sha256').update(body).digest('hex');const url=`https://raw.githubusercontent.com/ansabroh/MuseumLoanIQ/b0b6c58a724b7ba2730faa52f9f394252cc58688/evidence/${file}.json`;
 await write('submit_evidence',[id,url,sha,'Synthetic live lifecycle test: '+file]);await write('assess',[id]);
 loan=JSON.parse(await client.readContract({address:config.address,functionName:'get_loan',args:[id]}));writeFileSync('evidence/live-loan.json',JSON.stringify(loan,null,2));console.log('Outcome',loan.assessments.at(-1).outcome);
}
