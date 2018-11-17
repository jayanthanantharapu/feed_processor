function readURL(input) {
  if (input.files && input.files[0]) {
    $('.image-upload-wrap').hide();

    $('.file-upload-image').attr('src', 'https://cdn3.iconfinder.com/data/icons/ikooni-outline-file-formats/128/files2-19-512.png');
    $('.file-upload-content').show();

    $('.image-title').html(input.files[0].name);
  } else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});

$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});