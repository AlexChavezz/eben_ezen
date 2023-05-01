
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
    ${filteredProducts.map(product => '<li class="list-item" data-id='+ product[0] +'>' + product[1] +" "+"<span> $MXN: " +product[3]+"</span>" +'</li>').join('')}`
})


const total = document.querySelector('.main-content-sales-view-buttons-total');

document.addEventListener('click', function({target}) {
    // let totalprice = parseInt(document.querySelector(''));
    if(target.classList.contains('list-item')) {
        const productArray = products.products.find(product => product[0] == target.getAttribute('data-id'));
        const currentProduct = {
            id: productArray[0],
            name: productArray[1],
            marca: productArray[2],
            price: productArray[3],
            stock: productArray[4],
            description: productArray[5]
        }

        document.querySelector('.main-content-sales-view-products-container-table-tbody').innerHTML += `
        <tr class="main-content-sales-view-products-container-table-tbody-tr" data-id=${target.getAttribute('data-id')}>
            <td class="main-content-sales-view-products-container-table-tbody-tr-td">${currentProduct.name}</td>
            <td class="main-content-sales-view-products-container-table-tbody-tr-td">${currentProduct.stock}</td>
            <td class="main-content-sales-view-products-container-table-tbody-tr-td">$ ${currentProduct.price}
            </td>
            <td>
                <button class="btn btn-danger remove-list-element">
                    <img src="static/images/delete_FILL0_wght400_GRAD0_opsz48.svg" alt="remove-icon" class="remove-list-element-img"/>
                </button>
            </td>
        </tr>
        <li class="main-content-sales-view-products-container-list-item" data-id=${target.getAttribute('data-id')}></li>`;
        let currentPrice = parseInt(total.textContent)
        sume = currentPrice = currentPrice + parseInt(currentProduct.price);
        total.innerHTML = sume;
    }else if(target.classList.contains('remove-list-element') || target.classList.contains('remove-list-element-img')) {
        let currentPrice;
        if(target.classList.contains('remove-list-element-img')) {
            currentPrice = parseInt(target.parentElement.parentElement.previousElementSibling.textContent.slice(1));
            target.parentElement.parentElement.parentElement.remove()
        }
        if(target.classList.contains('remove-list-element')) {
            currentPrice = parseInt(target.parentElement.previousElementSibling.textContent.slice(1));
            target.parentElement.parentElement.remove()
        }
        total.textContent = parseInt(total.textContent) - parseInt(currentPrice);
    }

})

document.querySelector('.main-content-sales-view-buttons-salebutton').addEventListener('click', async function() {
    const products = document.querySelectorAll('.main-content-sales-view-products-container-table-tbody-tr');
    let productsArray = [];
    products.forEach(product => {
        productsArray = [...productsArray, {
            product_id: product.getAttribute('data-id'),
            name: product.children[0].textContent,
            stock: parseInt(product.children[1].textContent),
            price: parseInt(product.children[2].textContent.slice(1)),
        }]
    })
    let currentSale = {
        products: productsArray,
        total: parseInt(total.textContent),
        saleDate: dateString = new Date().toISOString().slice(0, 10)
    }
    let data = await window.fetch('/sales/add_sale', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(currentSale)
    });
        data = await data.json();
        console.log(data);
})