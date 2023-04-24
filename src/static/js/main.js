
let products;
document.addEventListener('DOMContentLoaded', async function() {
    const data = await window.fetch('/products/get_products')
    products = await data.json();
});



document.querySelector('.salespoint-main-content-searchbar').addEventListener('keyup', function(e) {

    const search = this.value;
    if(search.length < 1) {
        document.querySelector('.product-list').innerHTML='';
        return;
    }
    const filteredProducts = products.products.filter(product => {
        return product[1].toLowerCase().includes(search.toLowerCase())
    });
    document.querySelector('.product-list').innerHTML=`
    ${filteredProducts.map(product => '<li class="list-item">' + product[1] +" "+"<span> $MXN: " +product[3]+"</span>" +'</li>').join('')}`
})
