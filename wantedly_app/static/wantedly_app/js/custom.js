$(document).ready(function(){

  // Fade-out effect
  $(window).scroll(function() {
    var scrolled = $(window).scrollTop();
    var backgroundContainer = '.background2 > .responsive-img';
    $('.hero').each(function(index, element) {
      // var initY = $(this).offset().top
      var initY = 0;
      var height = $(this).height();
      var width = $(this).width();
      var endY  = initY + $(this).height();

      // Check if the element is in the viewport.
      var visible = isInViewport(this);
      if(visible) {
        var diff = scrolled - initY;
        var ratio = (1 - (diff / height) * 1.5);
          $(backgroundContainer).css('opacity', ratio);
      }
    });
  });
  function isInViewport(node) {
    var rect = node.getBoundingClientRect();
    return (
      (rect.height > 0 || rect.width > 0) &&
      rect.bottom >= 0 &&
      rect.right >= 0 &&
      rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  // Add option-tag to select form.
  var today = new Date();
  var thisYear = today.getFullYear();
  var limitYear = thisYear - 100;
  var selectYear = $('#selectYear');
  var selectMonth = $('#selectMonth');
  var selectDay = $('#selectDay');
  for (year = thisYear; year > limitYear; year--) {
    selectYear.append('<option>' + year + '</option>');
  }
  for ( month = 1; month < 13; month++) {
    selectMonth.append('<option>' + month + '</option>');
  }
  for ( date = 1; date < 32; date++) {
    selectDay.append('<option>' + date + '</option>');
  }

})// document ready end
