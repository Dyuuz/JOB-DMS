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
  "showMethod": "slideDown",
  "hideMethod": "fadeOut",
};

function NoAuthUser(event, id) {
    const navpage = document.querySelector(`.ordered-list-${id}`).getAttribute('data-cnt');
    toastr.options.preventDuplicates = true;
    toastr.clear();
    // toastr.options.progressBar = true;


    if (navpage === 'jobs-available') {
      toastr.error("Please login to access available jobs.");
    }
    else if (navpage === 'workplace') {
      toastr.error("Please login to access workplace.");
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
