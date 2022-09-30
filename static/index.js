let xhr = new XMLHttpRequest();
xhr.open('GET', '/articles/get-recent');
xhr.send();
xhr.onload = function() {
  var data=JSON.parse(xhr.response)
  var recent=data.recent;
  for(a of recent){
    document.getElementById("3-recent-articles").innerHTML+=`<div><a href="/articles/read?name=${a.name}&category=${a.category}"><h3>${a.name}</h3></a><h4>${a.author}</h4><p>${a.snippet}</p></div>`
  }
};
