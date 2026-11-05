export function terminal(tx) {
  const names=['UNINITIALIZED','PENDING','PROPOSING','COMMITTING','REVEALING','ACCEPTED','UNDETERMINED','FINALIZED','CANCELED','APPEAL_REVEALING','APPEAL_COMMITTING','READY_TO_FINALIZE','VALIDATORS_TIMEOUT','LEADER_TIMEOUT'];
  const status=String(tx.statusName??tx.status_name??(typeof tx.status==='number'?names[tx.status]:tx.status)??'').toUpperCase();
  if (['CANCELED','CANCELLED','UNDETERMINED','LEADER_TIMEOUT','VALIDATORS_TIMEOUT'].includes(status)) return {done:true,ok:false,status};
  if(status==='FINALIZED'){
    const leader=tx.consensus_data?.leader_receipt;
    const result=String(tx.txExecutionResultName??(Array.isArray(leader)?leader[0]?.execution_result:leader?.execution_result)??tx.execution_result??'').toUpperCase();
    return {done:true,ok:['SUCCESS','0'].includes(result),status,result};
  }
  return {done:false,ok:false,status:status||'PENDING'};
}
export async function follow(client,hash,onUpdate,{attempts=120,delay=1500,pause=ms=>new Promise(r=>setTimeout(r,ms))}={}){
  for(let i=0;i<attempts;i++){
    const tx=await client.getTransaction({hash});const state=terminal(tx);onUpdate(state,tx);
    if(state.done){if(!state.ok)throw new Error(`Transaction ${state.status}: ${state.result||'consensus failed'}`);return tx;}
    await pause(delay);
  }
  throw new Error('Finality is still pending. Resume tracking this transaction; do not resubmit.');
}
