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

function NoAuthUser(event, num) {
    const navpage = document.querySelector(`.ordered-list-${num}`).getAttribute('data-cnt');
    // const navpage = String(navbtn.getAttribute('data-cnt'));

    toastr.options.preventDuplicates = true;

    if (navpage === 'jobs-available') {
      toastr.error("Please login to access available jobs.");
    }
    else if (navpage === 'track-application') {
      toastr.error("Please login to track applications.");
    }
    else if (navpage === 'documents') {
      toastr.error("Please login to access documents.");
    }
    else if (navpage === 'profile') {
      toastr.error("Please login to access profile.");
    }
    else if (navpage === 'settings') {
      toastr.error("Please login to access settings.");
    }
    else{
      toastr.error("Please login to access this page");
    }
    event.preventDefault();
}
