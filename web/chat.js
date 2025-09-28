async function send() {
  const el = document.getElementById('text');
  const text = el.value.trim();
  if (!text) return;
  add('me', text);
  el.value = '';

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });
    const data = await res.json();
    add('bot', data.reply || '(no reply)');
    if (data.data) {
      const pre = document.createElement('pre');
      pre.textContent = JSON.stringify(data.data, null, 2);
      document.getElementById('chat').appendChild(pre);
    }
    scrollBottom();
  } catch (e) {
    add('bot', 'เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์');
  }
}

// เพิ่ม: ฟังก์ชัน helper
function handleSubmit(e){
  e.preventDefault();   // กันรีเฟรชหน้า
  send();
}

async function send() {
  const el = document.getElementById('text');
  const text = el.value.trim();
  if (!text) return;
  add('me', text);
  el.value = '';

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });
    const data = await res.json();
    add('bot', data.reply || '(no reply)');
    if (data.data) {
      const pre = document.createElement('pre');
      pre.textContent = JSON.stringify(data.data, null, 2);
      document.getElementById('chat').appendChild(pre);
    }
    scrollBottom();
  } catch (e) {
    add('bot', 'เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์');
  }
}
async function uploadFile(e){
  e.preventDefault();
  const f = document.getElementById('file').files[0];
  if(!f) return;
  const fd = new FormData();
  fd.append('file', f);
  add('me', `อัปโหลดไฟล์: ${f.name}`);
  const res = await fetch('/ingest/po', { method: 'POST', body: fd });
  const data = await res.json();
  add('bot', data.ok ? 'สร้าง PO จากไฟล์สำเร็จ' : 'ไม่สำเร็จ');
  if (data.data){
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(data.data, null, 2);
    document.getElementById('chat').appendChild(pre);
  }
  scrollBottom();
}
window.addEventListener('DOMContentLoaded', ()=>{
  document.getElementById('upload-form').addEventListener('submit', uploadFile);
});

function add(who, text){
  const div = document.createElement('div');
  div.className = 'msg ' + who;
  div.textContent = text;
  document.getElementById('chat').appendChild(div);
  scrollBottom();
}

function scrollBottom(){
  const c = document.getElementById('chat');
  c.scrollTop = c.scrollHeight;
}

// เพิ่ม: bind form submit + โฟกัสช่องพิมพ์
window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('chat-form').addEventListener('submit', handleSubmit);
  document.getElementById('text').focus();
});

async function submitPO(e){
  e.preventDefault();
  const body = {
    quantity: parseInt(document.getElementById('qty').value, 10),
    material_code: document.getElementById('mat').value.trim(),
    unit_price: parseFloat(document.getElementById('price').value),
    vendor_code: document.getElementById('vendor').value.trim(),
    currency: document.getElementById('ccy').value
  };
  add('me', `สร้าง PO (ฟอร์ม): ${body.quantity} ${body.material_code} ${body.unit_price} ${body.vendor_code}`);
  const res = await fetch('/po', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body)
  });
  const data = await res.json();
  add('bot', data.reply || 'สร้างไม่สำเร็จ');
  if (data.data){
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(data.data, null, 2);
    document.getElementById('chat').appendChild(pre);
  }
  scrollBottom();
}
window.addEventListener('DOMContentLoaded', ()=>{
  document.getElementById('po-form')?.addEventListener('submit', submitPO);
});

add('bot', 'สวัสดี! พิมพ์ "help" เพื่อดูสิ่งที่ฉันทำได้');

