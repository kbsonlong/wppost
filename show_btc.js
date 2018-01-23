function show_btc (data) {
    var packJson = data;
    var lists = packJson.data.list;
    for(var i = 0,j=1; i < lists.length; i++,j++){
        //将数据追加到id为hq的p标签
        if (lists[i].zhName==""){
            $("table").append("<tbody id='btc'><tr>" +
           "<td>" + j +"</td>" +
           "<td>" + lists[i].symbol + "-" + lists[i].name + "</td>" +
           "<td>" + lists[i].price +"</td>" +
           "<td>" + lists[i].change1h +"</td>" +
           "<td>" + lists[i].change1d +"</td>" +
           "<td>" + lists[i].volume_ex +"</td>" +
           "<td>" + lists[i].marketCap +"</td>" +
           "<td>" + lists[i].change7d +"</td>" +
           "<td>" + lists[i].change7d +"</td>" +
           "</tr></tbody>");}
        else {
           $("table").append("<tbody id='btc'><tr>" +
               "<td>" + j +"</td>" +
               "<td>" + lists[i].symbol + "-" + lists[i].zhName + "</td>" +
               "<td>" + lists[i].price +"</td>" +
               "<td>" + lists[i].change1h +"</td>" +
               "<td>" + lists[i].change1d +"</td>" +
               "<td>" + lists[i].volume_ex +"</td>" +
               "<td>" + lists[i].marketCap +"</td>" +
               "<td>" + lists[i].change7d +"</td>" +
               "</tr></tbody>");}
    }
}