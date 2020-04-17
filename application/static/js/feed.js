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


// Replicate navigation of image and normal search

$('#t-1').click(function () {
    $('#t-2').addClass('active');
    $('#i-2').removeClass('active');
});

$('#i-1').click(function () {
    $('#i-2').addClass('active');
    $('#t-2').removeClass('active');
});

$('#t-2').click(function () {
    $('#t-1').addClass('active');
    $('#i-1').removeClass('active');
});

$('#i-2').click(function () {
    $('#i-1').addClass('active');
    $('#t-1').removeClass('active');
});