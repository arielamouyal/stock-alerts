
const tbody = document.querySelector("#stocksTable tbody");
const API = "/api/stocks";
async function fetchAndRender(){
    try{
        const res = await fetch(API);
        const data = await res.json();
        tbody.innerHTML = "";
        for(const s of data.stocks){
            const tr = document.createElement("tr");
            tr.innerHTML = `<td><strong>${s.ticker}</strong></td><td>${s.price===null?'N/A':(s.price==='N/A'?'N/A':('$'+s.price))}</td><td>${s.change_percent==='N/A'?'N/A':(s.change_percent===null?'N/A':s.change_percent+'%')}</td><td></td><td><button class="btn remove" data-t="${s.ticker}">Remove</button></td>`;
            tbody.appendChild(tr);
            const newsTd = tr.querySelector("td:nth-child(4)");
            if(s.news && s.news.length){
                s.news.forEach(n=>{
                    const d = document.createElement("div");
                    d.className = "news";
                    d.innerHTML = `<a href="${n.url}" target="_blank">${n.title}</a><div class="small">${n.source} • ${new Date(n.publishedAt).toLocaleString()}</div>`;
                    newsTd.appendChild(d);
                });
            } else {
                newsTd.innerHTML = "<div class='small'>No impactful news</div>";
            }
        }
        document.querySelectorAll(".remove").forEach(b=>b.onclick=removeTicker);
    }catch(e){
        console.error(e);
    }
}
async function removeTicker(e){
    const t = e.currentTarget.dataset.t;
    await fetch(`/remove/${t}`,{method:"POST"});
    fetchAndRender();
}
document.getElementById("addForm").onsubmit = async function(ev){
    ev.preventDefault();
    const t = document.getElementById("tickerInput").value.trim().toUpperCase();
    if(!t) return;
    const fd = new FormData();
    fd.append("ticker",t);
    await fetch("/add",{method:"POST",body:fd});
    document.getElementById("tickerInput").value = "";
    fetchAndRender();
}
fetchAndRender();
setInterval(fetchAndRender, 10000); // update every 10s
