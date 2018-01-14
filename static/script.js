$(function() {
    var myDropzone = new Dropzone("#dz"); // this will create instance of Dropzone on the #dz element
    myDropzone.on("success", function(file) {
        location.href = '/resume?filename=' + file.name; // this will redirect you when the file is added to dropzone
    });
});