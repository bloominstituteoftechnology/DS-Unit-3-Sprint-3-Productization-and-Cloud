function Search(e) {
    e.preventDefault();
    form = $('#search');

    $.ajax({
        url: 'search',
        type: 'post',
        dataType: 'json',
        data: form.serialize(),
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}