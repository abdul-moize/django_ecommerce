function remove_div(id){
    var elements = document.getElementsByClassName("cart-item-box");
    for(let element of elements){
        if (element.getElementsByTagName("input")[0].value == id)
        {
            element.remove();
        }
    }
}
