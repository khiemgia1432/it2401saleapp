function addToCart(id,name,price){
    fetch('/api/carts',{
        method:'post',
        body: JSON.stringify({
            'id' :id,
            'name': name,
            'price':price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data =>{
        console.info(data);
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;
    })
}

function updateCart(id){
fetch(`/api/carts/${id}`,{
        method:'put',
        body: JSON.stringify({
            'quantity': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data =>{
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;
    })
}