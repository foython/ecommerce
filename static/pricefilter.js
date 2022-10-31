function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', ()=>{

  document.querySelectorAll("span.ui-slider-handle, div.slider-range-price").forEach(function(span) {
    span.onclick = function(){
      var range = document.querySelector(".range-price").innerHTML;
      if (range != null){
        var ar = range.split(' ');
        var newar = [];
        for(i = 0; i < ar.length; i++){
            if(ar[i].startsWith('$')){
            var item = ar[i].substring(1);
              newar.push(item);
            }
        var minValue = newar[0];
        var maxValue = newar[1];
        
      }
      }
      
      
      console.log(minValue);
      console.log(maxValue);
      var rangedata = {min: minValue, max: maxValue};
      var url = 'filter';

      fetch(url, {
        method: 'POST',
        headers:{
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken, //Necessary to work with request.is_ajax()
          
        },
        body: JSON.stringify(rangedata) 
      })
      .then((response)=>{
        return response.json()
    })
      .then(data => {
        console.log('Success:', data);
        console.log(Object.values(data));
      });
      
    }
    
  });
});