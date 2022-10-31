console.log('hello world');
document.addEventListener('DOMContentLoaded', ()=>{

  document.querySelectorAll("span.ui-slider-handle, div.slider-range-price").forEach(function(span) {
    span.onclick = function(){
      var range = document.querySelector(".range-price").innerHTML;
      var ar = range.split(' ');
      var newar = [];
      for(i = 0; i < ar.length; i++){
          if(ar[i].startsWith('$')){
          var item = ar[i].substring(1);
            newar.push(Number(item));
          }
      }
      
      console.log(newar);
      console.log(typeof(newar[0]));
    }
    
  });
});