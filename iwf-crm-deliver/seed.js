// Seeds demo leads so the dashboard looks alive on first run.
process.env.PORT = '4056';
require('./src/server.js');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const BASE = 'http://localhost:4056';

const demo = [
  { name:'Ravi Kumar', phone:'9876543210', email:'ravi@example.com', service:'Private Limited Company', source:'website', message:'Want to register a Pvt Ltd for my SaaS' },
  { name:'Sneha Patel', phone:'9123456780', email:'sneha@example.com', service:'GST Registration', source:'referral' },
  { name:'Arjun Mehta', phone:'9988776655', service:'Trademark Registration', source:'ad', message:'Brand name protection' },
  { name:'Fatima Sheikh', phone:'9001122334', email:'fatima@example.com', service:'ITR Filing (Business)', source:'website' },
  { name:'Karthik Iyer', phone:'9555666777', service:'LLP Registration', source:'whatsapp' },
  { name:'Divya Reddy', phone:'9444333222', email:'divya@example.com', service:'FSSAI License', source:'website' },
  { name:'Mohit Singh', phone:'9333444555', service:'Company Annual Filing', source:'referral' },
  { name:'Ananya Bose', phone:'9222111000', email:'ananya@example.com', service:'Copyright Registration', source:'website' },
];

async function main(){
  await sleep(2500);
  // login
  const lr = await fetch(BASE+'/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:process.env.ADMIN_EMAIL||'admin@indiawisefiling.com',password:process.env.ADMIN_PASSWORD||'changeme123'})}).then(x=>x.json());
  const H={'Content-Type':'application/json','Authorization':'Bearer '+lr.token};
  const ids=[];
  for(const d of demo){
    const r=await fetch(BASE+'/api/leads/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(x=>x.json());
    ids.push(r.lead_id);
  }
  // move some through the pipeline
  const moves=[
    [ids[0],'contacted',7999],[ids[1],'quoted',1499],[ids[2],'quoted',4999],
    [ids[3],'paid',2499],[ids[4],'in_progress',5999],[ids[5],'completed',1999],
    [ids[6],'lost',0],
  ];
  for(const [id,status,value] of moves){
    if(value)await fetch(BASE+`/api/leads/${id}`,{method:'PATCH',headers:H,body:JSON.stringify({value})});
    await fetch(BASE+`/api/leads/${id}/status`,{method:'PATCH',headers:H,body:JSON.stringify({status})});
  }
  await fetch(BASE+`/api/leads/${ids[0]}/activities`,{method:'POST',headers:H,body:JSON.stringify({type:'call',content:'Spoke for 10 min, sending quote tomorrow'})});
  await sleep(400); // let final debounced flush write to disk
  require('./src/db').flushNow();
  console.log('\n  Seeded '+demo.length+' demo leads.\n');
  process.exit(0);
}
main().catch(e=>{console.error(e);process.exit(1);});
