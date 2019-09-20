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

$(document).ready(function() {
    $.ajax({
        url: 'https://api.openaq.org/v1/countries',
        type: 'get',
        success: function (response) {
            console.log(response);
            response['results'].forEach(function(country) {
                $('#country').append('<option value="'+country['code']+'">'+country['name']+'</option>')
            })
        },
        error: function (error) {
            console.log(error);
        }
    });

    $('#country').on('change',function() {
        $('#city').empty();
        $.ajax({
            url: 'https://api.openaq.org/v1/cities?country='+this.value,
            type: 'get',
            success: function (response) {
                console.log(response);
                response['results'].forEach(function(city) {
                    $('#city').append('<option value="'+city['city']+'">'+city['city']+' ('+city['count']+' tests)</option>')
                })
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('#city').on('change',function() {
        form = $('#search');
        data = {'country_name':country = document.getElementById('country').value,'city_name':this.value}
        $('#error').empty();
        $('.records').empty()

        $.ajax({
            url: 'search',
            type: 'post',
            dataType: 'json',
            data: data,
            success: function (response) {
                console.log(response);
                if(response['response'] == 0) {
                    $('#error').html(response['message'])
                }else {
                    $('.records').append('<h2>Air Pollution</h2>');
                    response['message'].forEach(function(result) {
                        date = new Date(result['date']['utc'])
                        $('.records').append('<p>'+ result['value']+' '+result['unit'] +' on '+date.getMonth()+'/'+date.getDay()+'/'+date.getYear()+'</p>');
                    })
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});