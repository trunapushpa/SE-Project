$(document).ready(function () {
    $('#advanced-search').hide();
    $('#advanced-image-search').hide();
});

$('#show-adv-search').click(function () {
    $('#advanced-search').show();
    $('#normal-search').hide();
    // $('#search-card').toggleClass('small-card');
});

$('#hide-adv-search').click(function () {
    $('#advanced-search').hide();
    $('#normal-search').show();
    // $('#search-card').toggleClass('small-card');
});

$('#show-adv-image-search').click(function () {
    $('#advanced-image-search').show();
    $('#normal-image-search').hide();
    // $('#search-card').toggleClass('small-card');
});

$('#hide-adv-image-search').click(function () {
    $('#advanced-image-search').hide();
    $('#normal-image-search').show();
    // $('#search-card').toggleClass('small-card');
});

$('input[type="file"]').change(function (e) {
    let fileName = e.target.files[0].name;
    $('.custom-file-label').html(fileName);
});