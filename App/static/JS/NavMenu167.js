toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "3000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
};

function NoAuthUser(event) {
    const navbtn = document.querySelector('.ordered-list');
    // alert('Please login to access this page');
    toastr.options.preventDuplicates = true;
    toastr.error("Please login to access this page");
    event.preventDefault();
}
