var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i<updateBtns.length; i++){
   updateBtns[i].addEventListener('click' , function(){
       const productId = this.dataset.product;
       var action = this.dataset.action;
       console.log('product:' , productId, 'action:' , action )
       console.log('USER' , user)
       if(user == 'AnonymousUser'){
           console.log('not logged in')
       }else{
           updateUserOrder(productId , action )
       }
   })
   }
   function updateUserOrder(productId , action ){
      console.log("User is athenticated , sending data...");
        // var url = '/update-item/';
        fetch ('/update-item/', {
            method :'POST',
            headers :{
                'Content-Type': 'application/json',
                'X-CSRFToken' : csrftoken , 
            },
            body:JSON.stringify({'productId':productId , 'action':action})
        })
        
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log('data',data)
            location.reload()       
        } )
    }