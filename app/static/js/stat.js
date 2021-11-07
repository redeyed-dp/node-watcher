$(document).ready(function() {
// Загружаем состояние каждой ноды
    $(".node-stat").each(function() {
        var div = $(this)
        var id = $(this).attr('id');
        load(id, div);
    });
// Обновляем состояние одной ноды
    $(document).on("click", ".btn-renew", function() {
        var id = $(this).data("id");
        var div = $('#' + id);
        var ldiv = document.createElement('div');
        var img = document.createElement('img');
        $(img).attr("src", "/static/img/load.gif");
        $(ldiv).html(img).addClass("text-center");
        div.html(ldiv);
        load(id, div);
    });
});

function load(id, div) {
    $.get('/stat/' + id, {
    }).done(function(response) {
        div.html('');
        parse(response, div);
    }).fail(function() {
        div.html("Ошибка! Невозможно подключиться к серверу.");
    });
}

function parse(response, div) {
    if (response["error"]) {
        div.html(response["error"]).addClass("text-danger text-center");
    }
    else {
        $.each(response, function(key, value) {
            var container = document.createElement('div');
            var header = document.createElement('div');
            $(header).html(key).appendTo(container);
            var content = document.createElement('code');
            $(content).html(value).appendTo(container);
            div.append(container);
        });
    }
}