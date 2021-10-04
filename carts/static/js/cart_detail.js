function my_checkout(a=1){
    document.getElementById("checkout").value = "True";
    document.getElementById("form").submit();
}
function update_cart(max_quantity){
    if (document.getElementsByClassName("quantity-field")[0].value < max_quantity)
    {
        document.getElementById("checkout").value = "False";
        document.getElementById("form").submit();
    }

}
function remove_div(id){
    var elements = document.getElementsByClassName("cart-item-box");
    for(let element of elements){
        if (element.getElementsByTagName("input")[0].value == id)
        {
            element.remove();
        }
    }
    document.getElementById("checkout").value = "False";
    document.getElementById("form").submit();
}
