 (function(){
     const i = document.querySelector('#djdt-flamegraph-iframe');
     const tpl = document.querySelector('#djdt-flamegraph-tpl');
     i.contentWindow.document.write(tpl.innerHTML);
 }())
