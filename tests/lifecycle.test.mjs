import {test} from 'node:test';import assert from 'node:assert/strict';import {terminal,follow} from '../src/lifecycle.js';
test('accepted execution is not final',()=>assert.equal(terminal({status:'ACCEPTED',consensus_data:{leader_receipt:{execution_result:'SUCCESS'}}}).done,false));
test('finalized revert does not succeed',()=>assert.equal(terminal({status:'FINALIZED',consensus_data:{leader_receipt:{execution_result:'ERROR'}}}).ok,false));
test('finality requires successful execution',()=>assert.equal(terminal({status:'FINALIZED',consensus_data:{leader_receipt:{execution_result:'SUCCESS'}}}).ok,true));
test('unknown final result fails closed',()=>assert.equal(terminal({status:'FINALIZED'}).ok,false));
test('undetermined is terminal',()=>assert.equal(terminal({status:'UNDETERMINED'}).ok,false));
test('timeout never submits a duplicate',async()=>{let reads=0;await assert.rejects(follow({getTransaction:async()=>{reads++;return {status:'PENDING'}}},'hash',()=>{},{attempts:2,pause:async()=>{}}),/Resume tracking/);assert.equal(reads,2)});
test('real Studio receipt shape',()=>assert.equal(terminal({status:7,status_name:'FINALIZED',consensus_data:{leader_receipt:[{execution_result:'SUCCESS'}]}}).ok,true));
test('numeric Studio final status',()=>assert.equal(terminal({status:7,consensus_data:{leader_receipt:[{execution_result:'SUCCESS'}]}}).ok,true));
