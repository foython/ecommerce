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
    document.querySelectorAll('.qty-minus').forEach(function(item){
        item.onclick = ()=>{ 
            var counter = item.dataset.counter;  
            var effect = document.getElementById(`qty${counter}`); 
            var qty = effect.value;      
            if( !isNaN( qty ) && qty > 0 ){
            effect.value--; 
            } 
            var productId = item.dataset.product;            
            var action = 'minus';
            var data = {productId: productId, action: action};
            updateReq(data)
        }
    })

})


document.addEventListener('DOMContentLoaded', ()=>{ 
    document.querySelectorAll('.qty-plus').forEach(function(item){
        item.onclick = ()=>{ 
            var counter = item.dataset.counter;
            var effect = document.getElementById(`qty${counter}`); 
            var qty = effect.value;      
            if( !isNaN( qty )){
            effect.value++;
            }                
            var productId = item.dataset.product;            
            var action = 'add';
            console.log(productId)
            var data = {productId: productId, action: action};
            updateReq(data)
             
        }
    })

})





function updateReq(data){
    var url = 'http://127.0.0.1:8000/update/cart/';

    fetch(url, {
        method: 'POST',
        headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken, //Necessary to work with request.is_ajax()          
        },

        body: JSON.stringify(data) 
    })
    .then((response)=>{       
        return response.json()
    })
    .then(data => {        
        console.log('Success:', data);        
        console.log(Object.values(data));
        console.log(data);
        document.querySelectorAll('.cart-item').forEach(function(item){
           qty = item.querySelector('.qty-text').value;
           if(qty == 0){
            item.style.setProperty("display", "none", "important");
           }
        })
                
    });
}