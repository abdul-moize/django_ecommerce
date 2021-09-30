function remove_div(id){
    var elements = document.getElementsByClassName("cart-item-box");
    for(let element of elements){
        if (element.getElementsByTagName("input")[1].value == id)
        {
            element.remove();
        }
    }
}
