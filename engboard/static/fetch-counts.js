$(".card").each(function(index){
    var proddel = $(this).data("proddel");
    var card = $(this);
    $.get("/api/v1/proddel/" + proddel + "/counts", function(data) {
        console.log(data)
        card.find(".card-issue-count")[0].innerText = "(" + data['total_issues'] + ")";
        card.find(".progress_percent")[0].innerText = data['percent_complete'] + "%";
        $(card.find(".progress_bar")[0]).width("" + data['percent_complete'] + "%");
    });
});

