$(document).ready(function () {
    $('#loading-description').hide();
});

$(function() {
    $('#uploadform').submit(function() {
        $('#file', this).prop('disabled', true);
        return true;
    });
});

$('input[type=radio][name=type]').change(function() {
    if(this.value === 'lost' || this.value === 'found') {
        $('#date-time-picker').show();
    } else {
        $('#date-time-picker').hide();
    }
});

let startLoading = function() {
    $('#loading-description').show();
    $('#description-and-submit').hide();
};

let stopLoading = function() {
    $('#loading-description').hide();
    $('#description-and-submit').show();
};


$('input[type="file"]').change(function (e) {
    let fileName = e.target.files[0].name;
    $('.custom-file-label').html(fileName);

    startLoading();

    let fd = new FormData();
    let files = e.target.files[0];
    fd.append('file', files);

    $.ajax({
        url: '/get_item_description',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        success: function (data, textStatus, jQxhr) {
            $('#item-description')[0].innerText = data.description;
            $('#filename')[0].value = data.filename;
            $('#f_vector')[0].value = data.f_vector;
            stopLoading();
            // $('#messages').append("<div class=\"alert alert-dismissable alert-success\">\n" +
            //     "                        <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>\n" +
            //     "                        Successfully received image description" +
            //     "                    </div>");
        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(jqXhr);
            stopLoading();
            $('#messages').append("<div class=\"alert alert-dismissable alert-danger\">\n" +
                "                        <button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>\n" +
                "                        <strong>Error: </strong>" + jqXhr.responseText +
                "                    </div>");
        }
    });
});